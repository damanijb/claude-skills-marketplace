#!/usr/bin/env node
/**
 * ocr_webhook.js
 *
 * Send a PDF to the marker-pdf OCR webhook and return parsed content.
 * This is a NEW script (no TypeScript equivalent in the Electron app).
 *
 * Usage:
 *   node ocr_webhook.js <pdf-path> [webhook-url]
 *
 * Arguments:
 *   pdf-path     Path to the PDF file to OCR
 *   webhook-url  Optional webhook URL (defaults to marker-pdf on Tailscale)
 *
 * Output: OCR'd content (markdown) to stdout
 *
 * Environment:
 *   OCR_WEBHOOK_URL  Override the default webhook URL
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.error('Usage: node ocr_webhook.js <pdf-path> [webhook-url]');
  console.error('');
  console.error('Send PDF to marker-pdf OCR webhook and return parsed content.');
  console.error('');
  console.error('Environment:');
  console.error('  OCR_WEBHOOK_URL  Override the default webhook URL');
  process.exit(args[0] === '--help' ? 0 : 1);
}

const pdfPath = args[0];
const webhookUrl = args[1]
  || process.env.OCR_WEBHOOK_URL
  || 'https://samaritan.tail8478e1.ts.net/webhook/marker-pdf';

if (!fs.existsSync(pdfPath)) {
  console.error(`File not found: ${pdfPath}`);
  process.exit(1);
}

async function sendToOcr(filePath, url) {
  const fileBuffer = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);
  const boundary = '----FormBoundary' + Math.random().toString(36).slice(2);

  const header = [
    `--${boundary}`,
    `Content-Disposition: form-data; name="file"; filename="${fileName}"`,
    'Content-Type: application/pdf',
    '',
    ''
  ].join('\r\n');

  const footer = `\r\n--${boundary}--\r\n`;

  const headerBuffer = Buffer.from(header, 'utf8');
  const footerBuffer = Buffer.from(footer, 'utf8');
  const body = Buffer.concat([headerBuffer, fileBuffer, footerBuffer]);

  const parsedUrl = new URL(url);
  const transport = parsedUrl.protocol === 'https:' ? https : http;

  return new Promise((resolve, reject) => {
    const options = {
      hostname: parsedUrl.hostname,
      port: parsedUrl.port,
      path: parsedUrl.pathname,
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length
      },
      timeout: 120000
    };

    const req = transport.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(`OCR webhook returned status ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('OCR webhook timed out after 120 seconds'));
    });

    req.on('error', (err) => {
      reject(new Error(`OCR webhook connection error: ${err.message}`));
    });

    req.write(body);
    req.end();
  });
}

(async () => {
  try {
    console.error(`Sending ${path.basename(pdfPath)} to OCR webhook...`);
    console.error(`Webhook: ${webhookUrl}`);

    const result = await sendToOcr(pdfPath, webhookUrl);

    // Output the OCR content to stdout
    console.log(result);

    console.error('OCR processing complete.');
  } catch (err) {
    console.error(`OCR Error: ${err.message}`);
    console.error('');
    console.error('Troubleshooting:');
    console.error('  - Verify Tailscale VPN is connected');
    console.error('  - Check webhook URL is correct');
    console.error('  - Ensure marker-pdf service is running');
    console.error('  - Try setting OCR_WEBHOOK_URL environment variable');
    process.exit(1);
  }
})();
