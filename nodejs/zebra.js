'use strict';
const net = require('net');

class ZebraPrinter {
  constructor({ host, port = 9100 } = {}) {
    this.host = host;
    this.port = port;
  }

  printZPL(zpl) {
    return new Promise((resolve, reject) => {
      const client = net.createConnection(this.port, this.host, () => {
        client.write(zpl, 'utf8', () => {
          client.end();
          resolve();
        });
      });
      client.on('error', reject);
      client.setTimeout(5000, () => { client.destroy(); reject(new Error('Timeout')); });
    });
  }

  printTextLabel(lines = [], copies = 1) {
    let fields = '';
    let y = 50;
    for (const line of lines) {
      const { text = '', size = 30, bold = false } = line;
      const font = bold ? '^AEN' : '^ADN';
      fields += `^FO50,${y}${font},${size},${Math.floor(size * 0.6)}^FD${text}^FS\n`;
      y += size + 20;
    }
    return this.printZPL(`^XA\n^PQ${copies}\n${fields}^XZ`);
  }

  printShippingLabel({ toName, toAddress, toCity, tracking, copies = 1 }) {
    const zpl = `^XA
^PW800
^LL600
^FO30,30^ADN,40,20^FD${toName}^FS
^FO30,80^ADN,28,15^FD${toAddress}^FS
^FO30,120^ADN,28,15^FD${toCity}^FS
^FO30,180^BY3^BCN,100,Y,N,N^FD${tracking}^FS
^GB740,2,3^FS
^FO30,310^ADN,22,12^FDTRACKING: ${tracking}^FS
^PQ${copies}
^XZ`;
    return this.printZPL(zpl);
  }

  printQRLabel({ data, labelText = '', copies = 1 }) {
    const zpl = `^XA
^PW400
^LL400
^FO50,30^BQN,2,6^FDMA,${data}^FS
^FO50,310^ADN,28,15^FD${labelText}^FS
^PQ${copies}
^XZ`;
    return this.printZPL(zpl);
  }

  printAssetTag({ assetId, description, location = '', copies = 1 }) {
    const zpl = `^XA
^PW600
^LL300
^GB598,298,3^FS
^FO20,20^AEN,40,20^FDASSET TAG^FS
^FO20,80^ADN,30,15^FD${description}^FS
^FO20,120^ADN,24,12^FDLocation: ${location}^FS
^FO20,160^BY2^BCN,80,Y,N,N^FD${assetId}^FS
^PQ${copies}
^XZ`;
    return this.printZPL(zpl);
  }

  printNameBadge({ name, title, company = '', copies = 1 }) {
    const zpl = `^XA
^PW600
^LL400
^GB598,398,3^FS
^FO30,40^AEN,60,30^FD${name}^FS
^FO30,120^ADN,36,18^FD${title}^FS
^FO30,170^ADN,28,14^FD${company}^FS
^GB598,4,4^FS
^PQ${copies}
^XZ`;
    return this.printZPL(zpl);
  }
}

module.exports = ZebraPrinter;

// Example usage
if (require.main === module) {
  const printer = new ZebraPrinter({ host: '192.168.1.100' });

  printer.printTextLabel([
    { text: 'Jena Industries', size: 40, bold: true },
    { text: 'Part #12345', size: 28 },
  ]).then(() => console.log('Printed!')).catch(console.error);
}
