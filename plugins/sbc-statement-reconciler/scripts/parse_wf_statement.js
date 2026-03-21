#!/usr/bin/env node
/**
 * parse_wf_statement.js
 *
 * Parse a Wells Fargo bank statement PDF and extract transactions,
 * daily totals, and summary information.
 *
 * Compiled from: parsers/bank-statement-parser.ts (Electron app)
 *
 * Usage:
 *   node parse_wf_statement.js <pdf-path>
 *   node parse_wf_statement.js "/path/to/WF Jan 26 3163 Pt 1.pdf"
 *
 * Output: JSON to stdout with transactions, daily totals, and summary
 *
 * TODO: Replace this stub with compiled TypeScript from bank-statement-parser.ts
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.error('Usage: node parse_wf_statement.js <pdf-path> [<pdf-path-2> ...]');
  console.error('');
  console.error('Parse Wells Fargo bank statement PDF(s) and extract transactions.');
  console.error('Multiple PDF paths can be provided for multi-part statements.');
  console.error('Output: JSON to stdout');
  process.exit(args[0] === '--help' ? 0 : 1);
}

async function parsePdf(pdfPath) {
  const pdfParse = require('pdf-parse');
  const dataBuffer = fs.readFileSync(pdfPath);
  const data = await pdfParse(dataBuffer);
  return data.text;
}

async function parseWellsFargoStatement(pdfPaths) {
  let allText = '';

  for (const pdfPath of pdfPaths) {
    if (!fs.existsSync(pdfPath)) {
      console.error(`File not found: ${pdfPath}`);
      process.exit(1);
    }
    const text = await parsePdf(pdfPath);
    allText += '\n' + text;
  }

  // TODO: Replace with compiled bank-statement-parser.ts logic
  // The compiled TypeScript will contain the battle-tested regex patterns
  // for extracting WF transactions, dates, amounts, and daily totals.

  // Stub output structure:
  const result = {
    bank: 'wells-fargo',
    accountNumber: '',
    periodStart: '',
    periodEnd: '',
    openingBalance: 0,
    closingBalance: 0,
    totalDebits: 0,
    totalCredits: 0,
    transactionCount: 0,
    transactions: [],
    dailyTotals: {},
    rawTextLength: allText.length,
    partsProcessed: pdfPaths.length,
    _stub: true,
    _message: 'This is a stub. Replace with compiled bank-statement-parser.ts'
  };

  return result;
}

(async () => {
  try {
    const result = await parseWellsFargoStatement(args);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(`Error parsing statement: ${err.message}`);
    process.exit(1);
  }
})();
