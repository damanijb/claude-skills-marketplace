#!/usr/bin/env node
/**
 * Bloomberg BQL MCP Server
 *
 * Exposes Bloomberg Terminal data via the Model Context Protocol.
 * Spawns bqnt-3 Python as a subprocess for actual BQL queries.
 */

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} = require("@modelcontextprotocol/sdk/types.js");
const { execFile } = require("child_process");
const path = require("path");

// Bloomberg Python path — configurable via env or defaults to standard location
const BLOOMBERG_PYTHON =
  process.env.BLOOMBERG_PYTHON ||
  "C:\\blp\\bqnt\\environments\\bqnt-3\\python.exe";

const WORKER_SCRIPT = path.join(__dirname, "bql_worker.py");

// ─── BQL Examples by Domain ───────────────────────────────────────────

const EXAMPLES = {
  equity: [
    "get(px_last, pe_ratio, cur_mkt_cap) for('AAPL US Equity')",
    "get(name, px_last, pe_ratio) for(top(members('INDU Index'), 10, cur_mkt_cap))",
    "get(px_last(dates=range(-30D,0D))) for('AAPL US Equity')",
    "get(is_eps(fa_period_type=A, fa_period_offset=range(-4,2))) for('AAPL US Equity')",
    "get(groupavg(pe_ratio, gics_sector_name)) for(members('SPX Index'))",
  ],
  "fixed-income": [
    "get(name, cpn, maturity, yield(yield_type=YTW), duration(duration_type=modified), spread(spread_type=OAS)) for('EH469710 Corp')",
    "get(name, cpn, maturity) for(bonds('AAPL US Equity'))",
    "get(name, yield(yield_type=YTW), rating(source=SP)) for(top(bondsuniv(Active), 10, cpn))",
    "IMPORTANT: bondsuniv must be lowercase. Use yield_type=, duration_type=, spread_type= (NOT type=)",
    "IMPORTANT: Rating filter uses .source_scale numeric: 1=AAA, 2=AA+, 3=AA, 4=AA-, ..., 10=BBB-",
  ],
  credit: [
    "get(rating(source=SP)) for('EH469710 Corp')",
    "get(rating(source=MOODY)) for('EH469710 Corp')",
    "get(rating(source=BBG)) for('EH469710 Corp')",
  ],
  cds: [
    "get(cds_spread) for(cds('JPM US Equity', tenor=5Y))",
    "get(cds_spread(dates=range(-30D,0D))) for(cds('JPM US Equity', tenor=5Y))",
  ],
  curves: [
    "get(id) for(curveMembers(['YCGT0025 Index']))",
    "get(id().tenor, rate(side=Mid).value) for(curveMembers(['YCGT0025 Index'], tenors='5Y'))",
  ],
  funds: [
    "get(count(group(id, fund_typ))) for(fundsUniv(['Primary','Active']))",
  ],
  returns: [
    "get(total_return(calc_interval=range(-1M,0D))) for('AAPL US Equity')",
    "get(return_series(calc_interval=range(-1M,0D), per=W)) for('AAPL US Equity')",
  ],
};

// ─── Helper: run BQL via Python subprocess ────────────────────────────

function runBQL(query, timeout = 60) {
  return new Promise((resolve, reject) => {
    const reqJson = JSON.stringify({ query, timeout });
    const child = execFile(
      BLOOMBERG_PYTHON,
      [WORKER_SCRIPT, reqJson],
      { timeout: (timeout + 10) * 1000, maxBuffer: 10 * 1024 * 1024 },
      (error, stdout, stderr) => {
        if (error && !stdout) {
          reject(new Error(`Bloomberg Python error: ${error.message}`));
          return;
        }
        try {
          // Find the JSON line in stdout (skip any warnings on stderr)
          const lines = stdout.trim().split("\n");
          const jsonLine = lines[lines.length - 1];
          const result = JSON.parse(jsonLine);
          if (result.error) {
            const hints = result.hints ? "\n" + result.hints.map(h => `HINT: ${h}`).join("\n") : "";
            reject(new Error(`BQL Error: ${result.error}${hints}`));
          } else {
            resolve(result);
          }
        } catch (parseErr) {
          reject(new Error(`Failed to parse BQL response: ${stdout}`));
        }
      }
    );
  });
}

// ─── MCP Server ───────────────────────────────────────────────────────

const server = new Server(
  { name: "bloomberg-bql", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "bql_query",
      description:
        "Run a BQL query against a live Bloomberg Terminal. Returns JSON. " +
        "IMPORTANT: Use yield_type=YTW (not type=ytw), duration_type=modified, spread_type=OAS. " +
        "Rating filters use .source_scale (1=AAA...10=BBB-). bondsuniv must be lowercase.",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "BQL query string, e.g. get(px_last) for('AAPL US Equity')",
          },
          timeout: {
            type: "integer",
            description: "Timeout in seconds (default: 60, max: 300)",
            default: 60,
          },
        },
        required: ["query"],
      },
    },
    {
      name: "bql_examples",
      description:
        "Get example BQL queries for a domain. Use this BEFORE writing queries to learn correct syntax. " +
        "Domains: equity, fixed-income, credit, cds, curves, funds, returns.",
      inputSchema: {
        type: "object",
        properties: {
          domain: {
            type: "string",
            description: "Domain: equity, fixed-income, credit, cds, curves, funds, returns",
            enum: Object.keys(EXAMPLES),
          },
        },
        required: ["domain"],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "bql_query") {
    const query = (args.query || "").trim();
    if (!query) {
      return {
        content: [{ type: "text", text: "Error: query is required" }],
        isError: true,
      };
    }
    const timeout = Math.min(args.timeout || 60, 300);

    try {
      const result = await runBQL(query, timeout);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result.data, null, 2),
          },
        ],
      };
    } catch (e) {
      return {
        content: [{ type: "text", text: e.message }],
        isError: true,
      };
    }
  }

  if (name === "bql_examples") {
    const domain = args.domain || "equity";
    const examples = EXAMPLES[domain];
    if (!examples) {
      return {
        content: [
          {
            type: "text",
            text: `Unknown domain "${domain}". Available: ${Object.keys(EXAMPLES).join(", ")}`,
          },
        ],
        isError: true,
      };
    }
    const text = `BQL Examples — ${domain}\n${"=".repeat(40)}\n\n${examples.map((e) => `  ${e}`).join("\n\n")}`;
    return { content: [{ type: "text", text }] };
  }

  return {
    content: [{ type: "text", text: `Unknown tool: ${name}` }],
    isError: true,
  };
});

// ─── Start ────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Bloomberg BQL MCP server started");
}

main().catch((e) => {
  console.error("Fatal:", e);
  process.exit(1);
});
