#!/usr/bin/env node
/**
 * reconcile.js
 *
 * Core reconciliation logic: compare statement data vs HTTP data,
 * identify discrepancies, classify them, and generate text report.
 *
 * Compiled from: reconciliation-saver.ts (Electron app)
 *
 * Usage:
 *   node reconcile.js --statement <json> --http <json> --bank <type> --output <dir>
 *
 * Arguments:
 *   --statement  Path to statement parser JSON output
 *   --http       Path to HTTP parser JSON output
 *   --bank       Bank type: "wells-fargo" or "bofa"
 *   --output     Directory to write report files
 *   --department Optional department name for report headers
 *
 * Output: JSON reconciliation result to stdout + text report file
 *
 * TODO: Replace this stub with compiled TypeScript from reconciliation-saver.ts
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

if (!args.statement || !args.http || args.statement === '--help') {
  console.error('Usage: node reconcile.js --statement <json> --http <json> --bank <type> --output <dir>');
  console.error('');
  console.error('Compare statement data against HTTP data and generate reconciliation report.');
  console.error('');
  console.error('Arguments:');
  console.error('  --statement   Path to statement parser JSON output');
  console.error('  --http        Path to HTTP parser JSON output');
  console.error('  --bank        Bank type: "wells-fargo" or "bofa"');
  console.error('  --output      Directory to write report files');
  console.error('  --department  Optional department name for report headers');
  process.exit(args.statement === '--help' ? 0 : 1);
}

function loadJson(filePath) {
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function reconcile(statementData, httpData, bankType, department) {
  // TODO: Replace with compiled reconciliation-saver.ts logic
  // This will contain the full comparison engine:
  // - Wells Fargo: daily debit total comparison
  // - BofA: ending balance comparison with date shift
  // - Exception handling for ACH Returns, ZBA, etc.

  const result = {
    department: department || 'UNKNOWN',
    bank: bankType,
    accountNumber: statementData.accountNumber || '',
    periodStart: statementData.periodStart || '',
    periodEnd: statementData.periodEnd || '',
    status: 'NEEDS_REVIEW',
    comparisons: [],
    discrepancies: [],
    summary: {
      totalDates: 0,
      matchedDates: 0,
      discrepancyDates: 0,
      totalDiscrepancyAmount: 0
    },
    _stub: true,
    _message: 'This is a stub. Replace with compiled reconciliation-saver.ts'
  };

  return result;
}

function generateTextReport(reconciliation, outputDir) {
  const status = reconciliation.status;
  const dept = reconciliation.department;
  const account = reconciliation.accountNumber;
  const date = new Date().toISOString().split('T')[0];

  const filename = `${dept} ${account} Reconciliation ${status} ${date}.txt`;
  const outputPath = path.join(outputDir, filename);

  let report = '';
  report += `${'='.repeat(60)}\n`;
  report += `RECONCILIATION REPORT\n`;
  report += `${'='.repeat(60)}\n`;
  report += `Department: ${dept}\n`;
  report += `Bank: ${reconciliation.bank}\n`;
  report += `Account: ${account}\n`;
  report += `Period: ${reconciliation.periodStart} to ${reconciliation.periodEnd}\n`;
  report += `Status: ${status}\n`;
  report += `Date: ${date}\n`;
  report += `${'='.repeat(60)}\n\n`;

  if (reconciliation.discrepancies.length > 0) {
    report += `DISCREPANCIES:\n`;
    report += `${'-'.repeat(40)}\n`;
    for (const d of reconciliation.discrepancies) {
      report += `  ${d.date}: Statement=${d.statementValue} HTTP=${d.httpValue} Diff=${d.difference}\n`;
    }
    report += '\n';
  }

  report += `SUMMARY:\n`;
  report += `  Dates compared: ${reconciliation.summary.totalDates}\n`;
  report += `  Dates matched: ${reconciliation.summary.matchedDates}\n`;
  report += `  Discrepancies: ${reconciliation.summary.discrepancyDates}\n`;

  if (outputDir) {
    fs.mkdirSync(outputDir, { recursive: true });
    fs.writeFileSync(outputPath, report);
    console.error(`Report written to: ${outputPath}`);
  }

  return { report, outputPath: outputDir ? outputPath : null };
}

try {
  const statementData = loadJson(args.statement);
  const httpData = loadJson(args.http);
  const bankType = args.bank || statementData.bank || 'unknown';
  const department = args.department || '';

  const result = reconcile(statementData, httpData, bankType, department);

  if (args.output) {
    const { outputPath } = generateTextReport(result, args.output);
    result.reportPath = outputPath;
  }

  console.log(JSON.stringify(result, null, 2));
} catch (err) {
  console.error(`Error during reconciliation: ${err.message}`);
  process.exit(1);
}
