import traceback
from http.server import SimpleHTTPRequestHandler

import settings
from errors import MethodNotAllowed
from errors import NotFound
from utils import normalize_path
from utils import to_bytes
from utils import read_static


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = normalize_path(self.path)

        handlers = {
            "/": self.handle_root,
            "/hello/": self.handle_hello,
            "/style/": self.handle_style,
            "/ima/": self.handle_image,
            "/ave/": self.handle_ima,
            "/0/": self.handle_zde,
        }

        try:
            handler = handlers[path]
            handler()
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()


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

    def handle_zde(self):
        x = 1 / 0

    def handle_404(self):
        msg = """PAGE NOT FOUND!!!!!!"""

        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        self.respond(traceback.format_exc(), code=500, content_type="text/plain")

    def handle_image(self):
        img_file = settings.PROJECT_DIR / "images" / "ima.jpg"
        if not img_file.exists():
            return self.handle_404()

        with img_file.open("rb") as fp:
            img = fp.read()

        self.respond(img, content_type="image/jpg")

    def handle_ima(self):
        image_file = settings.PROJECT_DIR / "images" / "ave.jpg"
        if not image_file.exists():
            return self.handle_404()

        with image_file.open("rb") as fp:
            img = fp.read()

        self.respond(img, content_type="image/jpg")

    def handle_style(self):
        css_file = settings.PROJECT_DIR / "styles" / "style.css"
        if not css_file.exists():
            return self.handle_404()

        with css_file.open("r") as fp:
            css = fp.read()

        self.respond(css, content_type="text/css")

    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)


