#!/usr/bin/env node
/**
 * export_excel.js
 *
 * Generate Excel workbook from reconciliation data with multiple worksheets.
 *
 * Compiled from: excel-exporter.ts (Electron app)
 *
 * Usage:
 *   node export_excel.js --input <reconciliation.json> --output <path.xlsx>
 *
 * Output: Excel file with Summary, Daily Comparison, Discrepancies,
 *         Statement Transactions, and HTTP Transactions worksheets.
 *
 * TODO: Replace this stub with compiled TypeScript from excel-exporter.ts
 */

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 2) {
    const key = argv[i].replace(/^--/, '');
    args[key] = argv[i + 1];
  }
  return args;
}

const args = parseArgs(process.argv);

if (!args.input || !args.output || args.input === '--help') {
  console.error('Usage: node export_excel.js --input <reconciliation.json> --output <path.xlsx>');
  console.error('');
  console.error('Generate Excel workbook from reconciliation data.');
  console.error('');
  console.error('Arguments:');
  console.error('  --input   Path to reconciliation JSON data');
  console.error('  --output  Path for output .xlsx file');
  process.exit(args.input === '--help' ? 0 : 1);
}

async function exportExcel(inputPath, outputPath) {
  const ExcelJS = require('exceljs');

  if (!fs.existsSync(inputPath)) {
    console.error(`Input file not found: ${inputPath}`);
    process.exit(1);
  }

  const data = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
  const workbook = new ExcelJS.Workbook();

  // TODO: Replace with compiled excel-exporter.ts logic
  // The compiled TypeScript will create:
  // 1. Summary worksheet - overall status, period, account info
  // 2. Daily Comparison worksheet - side-by-side statement vs HTTP
  // 3. Discrepancies worksheet - only dates with differences
  // 4. Statement Transactions worksheet - full transaction listing
  // 5. HTTP Transactions worksheet - full HTTP listing

  // Stub: Create a basic summary sheet
  const summary = workbook.addWorksheet('Summary');
  summary.columns = [
    { header: 'Field', key: 'field', width: 25 },
    { header: 'Value', key: 'value', width: 40 }
  ];
  summary.addRow({ field: 'Department', value: data.department || 'N/A' });
  summary.addRow({ field: 'Bank', value: data.bank || 'N/A' });
  summary.addRow({ field: 'Status', value: data.status || 'N/A' });
  summary.addRow({ field: 'Period', value: `${data.periodStart || ''} to ${data.periodEnd || ''}` });
  summary.addRow({ field: 'Note', value: 'STUB - Replace with compiled excel-exporter.ts' });

  // Ensure output directory exists
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  await workbook.xlsx.writeFile(outputPath);
  console.error(`Excel report written to: ${outputPath}`);

  return { outputPath, worksheets: workbook.worksheets.map(ws => ws.name) };
}

(async () => {
  try {
    const result = await exportExcel(args.input, args.output);
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error(`Error exporting Excel: ${err.message}`);
    process.exit(1);
  }
})();
