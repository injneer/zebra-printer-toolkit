# Zebra Printer Toolkit

A simple, practical toolkit for sending ZPL (Zebra Programming Language) commands to Zebra label printers over a network or USB connection.

## How Zebra Printers Work

Zebra printers use **ZPL (Zebra Programming Language)** — plain text commands sent directly to the printer. No special drivers required for network printing.

- **Network printing**: Send ZPL to port `9100` over TCP
- **USB printing**: Write ZPL to `/dev/usb/lp0` (Linux) or use Windows driver
- **Label size**: Defined in printer settings or per job in ZPL

## Quick Start

### Network Print (Python)
```python
import socket

def print_label(ip, zpl, port=9100):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(zpl.encode())

zpl = """
^XA
^FO50,50^ADN,36,20^FDHello World^FS
^XZ
"""
print_label("192.168.1.100", zpl)
```

### Network Print (Node.js)
```js
const net = require('net');

function printLabel(ip, zpl, port = 9100) {
  const client = net.createConnection(port, ip, () => {
    client.write(zpl);
    client.end();
  });
}

printLabel("192.168.1.100", "^XA^FO50,50^ADN,36,20^FDHello World^FS^XZ");
```

## ZPL Basics

| Command | Description |
|--------|-------------|
| `^XA` | Start of label |
| `^XZ` | End of label |
| `^FO x,y` | Field origin (position) |
| `^FD text ^FS` | Field data (text content) |
| `^AD N,height,width` | Font selection |
| `^BY width` | Barcode default settings |
| `^BC` | Code 128 barcode |
| `^BQ` | QR code |
| `^GB w,h,t` | Graphic box (draw rectangle) |
| `^CF font,size` | Default font |
| `^LL length` | Label length |
| `^PW width` | Print width |
| `^PQ qty` | Print quantity |

## Label Examples

See the [`examples/`](examples/) folder for ready-to-use ZPL templates:

- `simple_text.zpl` — Basic text label
- `shipping_label.zpl` — Shipping label with barcode
- `qr_code.zpl` — QR code label
- `asset_tag.zpl` — Asset/inventory tag
- `name_badge.zpl` — Name badge

## Python Library

See [`python/zebra.py`](python/zebra.py) for a full Python class with:
- Network and USB printing
- Label templates
- Barcode and QR generation
- Print queue support

## Node.js Library

See [`nodejs/zebra.js`](nodejs/zebra.js) for a Node.js module with:
- Promise-based API
- Network printing
- Label builder

## Finding Your Printer IP

```bash
# Linux / Mac
ping zebra.local

# Or scan your network
nmap -p 9100 192.168.1.0/24

# Windows
ping zebra.local
```

Most Zebra printers also have a web interface at `http://<printer-ip>`.

## Tested Printers

- Zebra ZD420
- Zebra ZD620
- Zebra ZT410
- Zebra GK420d
- Zebra GX430t

Should work with any Zebra printer that supports ZPL II.

## License

MIT
