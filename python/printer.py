"""
Zebra Printer - Simple scratch code for quick integration
"""
import socket

PRINTER_IP = '192.168.1.180'
PRINTER_PORT = 9100

def print_label(zpl: str, copies: int = 1, ip: str = PRINTER_IP, port: int = PRINTER_PORT):
    """Send ZPL label to Zebra printer over network."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((ip, port))
        for _ in range(copies):
            s.sendall(zpl.encode('utf-8'))

def make_label(line1='', line2='', line3='', line4='', barcode='', qr=''):
    """Build a ZPL label string."""
    fields = '^XA\n^PW800\n^LL300\n'
    positions = [50, 100, 150, 200]
    for i, text in enumerate([line1, line2, line3, line4]):
        if text:
            fields += f'^FO50,{positions[i]}^ADN,36,18^FD{text}^FS\n'
    if barcode:
        fields += f'^FO50,220^BY2^BCN,60,Y,N,N^FD{barcode}^FS\n'
    if qr:
        fields += f'^FO600,30^BQN,2,5^FDMA,{qr}^FS\n'
    fields += '^XZ'
    return fields


# ── Quick test ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    zpl = make_label(
        line1='Jena Industries',
        line2='Waterdown, ON',
    )
    print_label(zpl, copies=1)
    print('Printed!')
