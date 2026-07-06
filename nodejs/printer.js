'use strict';
const net = require('net');

const PRINTER_IP = '192.168.1.149';
const PRINTER_PORT = 9100;

/**
 * Send ZPL label to Zebra printer over network.
 */
function printLabel(zpl, copies = 1, ip = PRINTER_IP, port = PRINTER_PORT) {
  return new Promise((resolve, reject) => {
    const client = net.createConnection(port, ip, () => {
      for (let i = 0; i < copies; i++) client.write(zpl);
      client.end();
      resolve();
    });
    client.setTimeout(5000, () => { client.destroy(); reject(new Error('Timeout')); });
    client.on('error', reject);
  });
}

/**
 * Build a ZPL label string.
 */
function makeLabel({ line1 = '', line2 = '', line3 = '', line4 = '', barcode = '', qr = '' } = {}) {
  let zpl = '^XA\n^PW800\n^LL300\n';
  const positions = [50, 100, 150, 200];
  [line1, line2, line3, line4].forEach((text, i) => {
    if (text) zpl += `^FO50,${positions[i]}^ADN,36,18^FD${text}^FS\n`;
  });
  if (barcode) zpl += `^FO50,220^BY2^BCN,60,Y,N,N^FD${barcode}^FS\n`;
  if (qr) zpl += `^FO600,30^BQN,2,5^FDMA,${qr}^FS\n`;
  zpl += '^XZ';
  return zpl;
}

module.exports = { printLabel, makeLabel };

// ── Quick test ───────────────────────────────────────────────────────────────
if (require.main === module) {
  const zpl = makeLabel({ line1: 'Jena Industries', line2: 'Waterdown, ON' });
  printLabel(zpl, 1).then(() => console.log('Printed!')).catch(console.error);
}
