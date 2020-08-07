import socketserver
import settings

from utils import normalize_path

from http.server import SimpleHTTPRequestHandler


class MyHandler(SimpleHTTPRequestHandler):



    def do_GET(self):
        path = normalize_path(self.path)

        if path == "/":
            self.handle_root()
        elif path == "/hello/":
            self.handle_hello()
        elif path == "/style/":
            self.handle_style()
        else:
            self.handle_404()

    def handle_root(self):
        return super().do_GET()

    def handle_hello(self):

        content = f"""
                <html>
                <head><title>Hello ma Page</title></head>
                <body>
                <h1>Hello World!</h1>
                <p>path: {self.path}</p>
                </body>
                </html>
                """

        self.respond(content)

    def handle_404(self):
        msg = """PAGE NOT FOUND!!!!!!"""

        self.respond(msg, code=404, content_type="text/plain")

    def handle_style(self):
        css_file = settings.PROJECT_DIR / "styles" / "style.css"
        if not css_file.exists():
            return self.handle_404()

        with css_file.open("r") as fp:
            css = fp.read()

        self.respond(css, content_type="text/css")

    def respond(self, message, code=200, content_type="text/html"):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(message)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()

        if isinstance(message, str):
            message = message.encode()
        self.wfile.write(message)



if __name__ == "__main__":
    with socketserver.TCPServer(("", settings.PORT), MyHandler) as httpd:
        print("it" + " works")
        httpd.serve_forever(poll_interval=1)

