import os
import socketserver
from http.server import SimpleHTTPRequestHandler


PORT = int(os.getenv("PORT", 8000))
print(PORT)


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        content = """
        <html>
        <head><title>XXX</title></head>
        <body>Hello World!</body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-leght", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode())


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)

