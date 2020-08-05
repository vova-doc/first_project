import os
import socketserver
import settings

from http.server import SimpleHTTPRequestHandler


PORT = int(os.getenv("PORT", 8000))
print(PORT)


class MyHandler(SimpleHTTPRequestHandler):
    def handle_root(self):
        return super().do_GET()

    def handle_hello(self):

        content = f"""
                <html>
                <head><title>XXX</title></head>
                <body>
                <h1>Hello World!</h1>
                <p>path: {self.path}</p>
                </body>
                </html>
                """

        self.respond(content)

    def handle_404(self):
        msg = """PAGE NOT FOUND!!!!!!"""

        self.respond(msg, code=404,)

    def handle_style(self):
        css_file = settings.Documents_DIR / "tms" / "first_project" / "style.css"
        if not css_file.exist():
            return self.handle_404()

        with css_file.open("r") as fp:
            css = fp.read()

        self.respond(css, content_type="text/css")

    def respond(self, message, code=200):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(message)))
        self.end_headers()
        if isinstance(message, str)
            message = message.encode()

        self.wfile.write(message.encode())

    def do_GET(self):
        path = self.build_path()

        if path == "/":
            self.handle_root()
        elif path == "/hello/":
            self.handle_hello()
        elif path == "/style/":
            self.handle_style()
        else:
            self.handle_404()


    def build_path(self) -> str:
        result = self.path

        if self.path[-1] != "/":
            result = f"{result}/"

        return result


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)

