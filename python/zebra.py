"""
Zebra Printer Toolkit - Python Library
Send ZPL labels to Zebra printers over network or USB.
"""

import socket
import os


class ZebraPrinter:
    def __init__(self, host=None, port=9100, usb_device=None):
        """
        host: IP address for network printing
        port: TCP port (default 9100)
        usb_device: path to USB device e.g. '/dev/usb/lp0'
        """
        self.host = host
        self.port = port
        self.usb_device = usb_device

    def print_zpl(self, zpl: str):
        if self.usb_device:
            self._print_usb(zpl)
        elif self.host:
            self._print_network(zpl)
        else:
            raise ValueError("No host or USB device specified")

    def _print_network(self, zpl: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((self.host, self.port))
            s.sendall(zpl.encode('utf-8'))

    def _print_usb(self, zpl: str):
        with open(self.usb_device, 'wb') as f:
            f.write(zpl.encode('utf-8'))

    def print_text_label(self, lines: list, copies=1):
        """Print a simple multi-line text label."""
        fields = ""
        y = 50
        for line in lines:
            text = line.get("text", "")
            size = line.get("size", 30)
            bold = line.get("bold", False)
            font = "^AEN" if bold else "^ADN"
            fields += f"^FO50,{y}{font},{size},{int(size*0.6)}^FD{text}^FS\n"
            y += size + 20
        zpl = f"^XA\n^PQ{copies}\n{fields}^XZ"
        self.print_zpl(zpl)

    def print_shipping_label(self, to_name, to_address, to_city, tracking, copies=1):
        """Print a shipping label with Code 128 barcode."""
        zpl = f"""^XA
^PW800
^LL600
^FO30,30^ADN,40,20^FD{to_name}^FS
^FO30,80^ADN,28,15^FD{to_address}^FS
^FO30,120^ADN,28,15^FD{to_city}^FS
^FO30,180^BY3^BCN,100,Y,N,N^FD{tracking}^FS
^GB740,2,3^FS
^FO30,310^ADN,22,12^FDTRACKING: {tracking}^FS
^PQ{copies}
^XZ"""
        self.print_zpl(zpl)

    def print_qr_label(self, data, label_text="", copies=1):
        """Print a QR code label."""
        zpl = f"""^XA
^PW400
^LL400
^FO50,30^BQN,2,6^FDMA,{data}^FS
^FO50,310^ADN,28,15^FD{label_text}^FS
^PQ{copies}
^XZ"""
        self.print_zpl(zpl)

    def print_asset_tag(self, asset_id, description, location="", copies=1):
        """Print an asset/inventory tag."""
        zpl = f"""^XA
^PW600
^LL300
^GB598,298,3^FS
^FO20,20^AEN,40,20^FDASSET TAG^FS
^FO20,80^ADN,30,15^FD{description}^FS
^FO20,120^ADN,24,12^FDLocation: {location}^FS
^FO20,160^BY2^BCN,80,Y,N,N^FD{asset_id}^FS
^PQ{copies}
^XZ"""
        self.print_zpl(zpl)

    def print_name_badge(self, name, title, company="", copies=1):
        """Print a name badge."""
        zpl = f"""^XA
^PW600
^LL400
^GB598,398,3^FS
^FO30,40^AEN,60,30^FD{name}^FS
^FO30,120^ADN,36,18^FD{title}^FS
^FO30,170^ADN,28,14^FD{company}^FS
^GB598,4,4^FS
^PQ{copies}
^XZ"""
        self.print_zpl(zpl)


if __name__ == "__main__":
    # Example usage
    printer = ZebraPrinter(host="192.168.1.100")

    # Simple text
    printer.print_text_label([
        {"text": "Jena Industries", "size": 40, "bold": True},
        {"text": "Part #12345", "size": 28},
        {"text": "Waterdown, ON", "size": 24},
    ])

    # QR code
    printer.print_qr_label("https://jenaindustries.com", "Jena Industries")

    # Asset tag
    printer.print_asset_tag("ASSET-001", "Powder Coat Oven", "Shop Floor")
