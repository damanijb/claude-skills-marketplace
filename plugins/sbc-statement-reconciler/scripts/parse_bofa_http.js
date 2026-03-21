#!/usr/bin/env node
/**
 * parse_bofa_http.js
 *
 * Parse a Bank of America HTTP reconciliation document (post-OCR markdown/HTML).
 *
 * Compiled from: parsers/bofa-http-parser.ts (Electron app)
 *
 * Usage:
 *   node parse_bofa_http.js <file-path>
 *   node parse_bofa_http.js "/path/to/ocr-output.md"
 *   cat ocr-output.md | node parse_bofa_http.js --stdin
 *
 * Output: JSON to stdout with daily balances from HTTP document
 *
 * TODO: Replace this stub with compiled TypeScript from bofa-http-parser.ts
 */

const fs = require('fs');

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.error('Usage: node parse_bofa_http.js <file-path>');
  console.error('       cat file.md | node parse_bofa_http.js --stdin');
  console.error('');
  console.error('Parse Bank of America HTTP reconciliation document (post-OCR).');
  console.error('Output: JSON to stdout');
  process.exit(args[0] === '--help' ? 0 : 1);
}

async function readInput() {
  if (args[0] === '--stdin') {
    return new Promise((resolve, reject) => {
      let data = '';
      process.stdin.setEncoding('utf8');
      process.stdin.on('data', chunk => data += chunk);
      process.stdin.on('end', () => resolve(data));
      process.stdin.on('error', reject);
    });
  } else {
    if (!fs.existsSync(args[0])) {
      console.error(`File not found: ${args[0]}`);
      process.exit(1);
    }
    return fs.readFileSync(args[0], 'utf8');
  }
}

(async () => {
  try {
    const content = await readInput();

    // TODO: Replace with compiled bofa-http-parser.ts logic

    const result = {
      bank: 'bofa',
      source: 'http-document',
      dailyBalances: {},
      rawContentLength: content.length,
      _stub: true,
      _message: 'This is a stub. Replace with compiled bofa-http-parser.ts'
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(`Error parsing HTTP document: ${err.message}`);
    process.exit(1);
  }
})();
