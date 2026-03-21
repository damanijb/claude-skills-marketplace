#!/usr/bin/env node
/**
 * scan_directories.js
 *
 * Scan a network share directory for bank statement folders and report
 * which departments are ready for processing, already reconciled, or missing files.
 *
 * Compiled from: directory-scanner.ts (Electron app)
 *
 * Usage:
 *   node scan_directories.js [month-filter]
 *   node scan_directories.js "January 2026"
 *   node scan_directories.js --path "/custom/path" "January 2026"
 *
 * The script auto-detects the base path based on OS:
 *   macOS:   /Volumes/Shared/Banking/Bank Statements/
 *   Windows: T:/Data/Shared/Banking/Bank Statements/
 *
 * Output: JSON array to stdout
 *
 * TODO: Replace stub parsing logic with compiled TypeScript from directory-scanner.ts
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// ============================================================
// Default base paths by platform
// ============================================================
const DEFAULT_PATHS = {
  darwin: '/Volumes/Shared/Banking/Bank Statements',    // macOS
  win32:  'T:/Data/Shared/Banking/Bank Statements',     // Windows
  linux:  '/Volumes/Shared/Banking/Bank Statements'     // Linux/Cowork VM (same as Mac mount)
};

// ============================================================
// Argument parsing
// ============================================================
const args = process.argv.slice(2);
let customPath = null;
let monthFilter = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--help') {
    console.error('Usage: node scan_directories.js [month-filter]');
    console.error('       node scan_directories.js --path <custom-path> [month-filter]');
    console.error('');
    console.error('Scans the bank statements directory for department folders.');
    console.error('Auto-detects the base path by OS:');
    console.error(`  macOS:   ${DEFAULT_PATHS.darwin}`);
    console.error(`  Windows: ${DEFAULT_PATHS.win32}`);
    console.error('');
    console.error('Options:');
    console.error('  --path <dir>   Override the default base path');
    console.error('  month-filter   e.g. "January 2026" — scan only that month');
    console.error('');
    console.error('Output: JSON array with department status objects.');
    process.exit(0);
  } else if (args[i] === '--path' && args[i + 1]) {
    customPath = args[i + 1];
    i++; // skip next arg
  } else {
    monthFilter = args[i];
  }
}

// Resolve the base path
function resolveBasePath() {
  if (customPath) return customPath;

  const platform = os.platform();
  const defaultPath = DEFAULT_PATHS[platform] || DEFAULT_PATHS.darwin;

  // Try the default path first
  if (fs.existsSync(defaultPath)) return defaultPath;

  // Fallback: check all known paths in case of mount differences
  for (const p of Object.values(DEFAULT_PATHS)) {
    if (fs.existsSync(p)) return p;
  }

  console.error('Bank statements directory not found. Tried:');
  for (const [plat, p] of Object.entries(DEFAULT_PATHS)) {
    console.error(`  ${plat}: ${p}`);
  }
  console.error('');
  console.error('Use --path <dir> to specify the location manually.');
  process.exit(1);
}

const basePath = resolveBasePath();

// ============================================================
// Scanner logic
// ============================================================
function detectBankType(files) {
  for (const f of files) {
    const lower = f.toLowerCase();
    if (lower.includes('wf') && !lower.includes('http')) return 'wells-fargo';
    if (lower.includes('bofa') || lower.includes('50090')) return 'bofa';
  }
  return 'unknown';
}

function scanDepartmentFolder(deptPath, deptName) {
  const files = fs.readdirSync(deptPath);
  const pdfFiles = files.filter(f => f.toLowerCase().endsWith('.pdf'));
  const reportFiles = files.filter(f =>
    f.toLowerCase().includes('reconciliation') &&
    (f.endsWith('.txt') || f.endsWith('.xlsx'))
  );

  const statementPdfs = pdfFiles.filter(f => !f.toLowerCase().includes('http'));
  const httpDocs = pdfFiles.filter(f => f.toLowerCase().includes('http'));

  const bank = detectBankType(pdfFiles);

  let status = 'ready';
  if (reportFiles.length > 0) {
    status = 'already-reconciled';
  } else if (statementPdfs.length === 0 || httpDocs.length === 0) {
    status = 'missing-files';
  }

  return {
    department: deptName,
    bank: bank,
    statementPdf: statementPdfs.length > 0 ? statementPdfs.map(f => path.join(deptPath, f)) : null,
    httpDocument: httpDocs.length > 0 ? path.join(deptPath, httpDocs[0]) : null,
    existingReports: reportFiles.map(f => path.join(deptPath, f)),
    status: status,
    allFiles: files
  };
}

function scan(rootDir, month) {
  let searchDir = rootDir;

  // If month is provided, look for it as a subdirectory
  if (month) {
    const yearMatch = month.match(/\d{4}/);
    if (yearMatch) {
      // Try: basePath/2026/January 2026
      const yearPath = path.join(rootDir, yearMatch[0], month);
      if (fs.existsSync(yearPath)) {
        searchDir = yearPath;
      } else {
        // Try: basePath/January 2026
        const directPath = path.join(rootDir, month);
        if (fs.existsSync(directPath)) {
          searchDir = directPath;
        } else {
          console.error(`Month directory not found. Tried:`);
          console.error(`  ${yearPath}`);
          console.error(`  ${directPath}`);
          process.exit(1);
        }
      }
    }
  }

  if (!fs.existsSync(searchDir)) {
    console.error(`Directory not found: ${searchDir}`);
    process.exit(1);
  }

  const entries = fs.readdirSync(searchDir, { withFileTypes: true });
  const departments = entries
    .filter(e => e.isDirectory())
    .map(e => scanDepartmentFolder(path.join(searchDir, e.name), e.name));

  return { basePath: rootDir, scanPath: searchDir, departments };
}

// ============================================================
// Main
// ============================================================
try {
  console.error(`Base path: ${basePath}`);
  if (monthFilter) console.error(`Month filter: ${monthFilter}`);

  const results = scan(basePath, monthFilter);
  console.log(JSON.stringify(results, null, 2));
} catch (err) {
  console.error(`Error scanning directories: ${err.message}`);
  process.exit(1);
}
