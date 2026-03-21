#!/bin/bash
# Setup script for sbc-statement-reconciler plugin
# Installs Node.js dependencies required by the compiled TypeScript scripts

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== SBC Statement Reconciler - Setup ==="
echo "Installing Node.js dependencies..."

# Check Node.js is available
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is required but not found."
    echo "Please install Node.js 18+ to use this plugin."
    exit 1
fi

echo "Node.js version: $(node --version)"

# Initialize package.json if not present
if [ ! -f "$SCRIPT_DIR/package.json" ]; then
    cd "$SCRIPT_DIR"
    cat > package.json << 'EOF'
{
  "name": "sbc-statement-reconciler-scripts",
  "version": "0.1.0",
  "private": true,
  "description": "Scripts for SBC Statement Reconciler plugin",
  "type": "commonjs",
  "dependencies": {
    "pdf-parse": "^1.1.1",
    "exceljs": "^4.4.0",
    "mssql": "^10.0.2"
  }
}
EOF
fi

# Install dependencies
cd "$SCRIPT_DIR"
npm install --production

echo ""
echo "=== Setup Complete ==="
echo "Dependencies installed successfully."
echo ""
echo "Verify installation:"
echo "  node $SCRIPT_DIR/parse_wf_statement.js --help"
