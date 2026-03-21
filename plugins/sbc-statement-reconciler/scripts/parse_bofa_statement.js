#!/usr/bin/env node
/**
 * parse_bofa_statement.js
 *
 * Parse a Bank of America statement PDF and extract transactions,
 * daily balances, and summary information.
 *
 * Compiled from: parsers/bofa-statement-parser.ts (Electron app)
 *
 * Usage:
 *   node parse_bofa_statement.js <pdf-path>
 *   node parse_bofa_statement.js "/path/to/BofA 50090 Jan 26.pdf"
 *
 * Output: JSON to stdout with transactions, daily balances, and summary
 *
 * TODO: Replace this stub with compiled TypeScript from bofa-statement-parser.ts
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.error('Usage: node parse_bofa_statement.js <pdf-path>');
  console.error('');
  console.error('Parse Bank of America statement PDF and extract transactions.');
  console.error('Output: JSON to stdout');
  process.exit(args[0] === '--help' ? 0 : 1);
}

async function parsePdf(pdfPath) {
  const pdfParse = require('pdf-parse');
  const dataBuffer = fs.readFileSync(pdfPath);
  const data = await pdfParse(dataBuffer);
  return data.text;
}

async function parseBofAStatement(pdfPath) {
  if (!fs.existsSync(pdfPath)) {
    console.error(`File not found: ${pdfPath}`);
    process.exit(1);
  }

  const text = await parsePdf(pdfPath);

  // TODO: Replace with compiled bofa-statement-parser.ts logic

  const result = {
    bank: 'bofa',
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
    rawTextLength: text.length,
    _stub: true,
    _message: 'This is a stub. Replace with compiled bofa-statement-parser.ts'
  };

  return result;
}

(async () => {
  try {
    const result = await parseBofAStatement(args[0]);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(`Error parsing statement: ${err.message}`);
    process.exit(1);
  }
})();
