import traceback
from http.server import SimpleHTTPRequestHandler

import settings
from custom_types import Endpoint
from errors import MethodNotAllowed
from errors import NotFound
from utils import get_content_type
from utils import get_name_from_qs
from utils import get_age_from_qs
from utils import to_bytes
from utils import read_static


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        endpoint = Endpoint.from_path(self.path)
        content_type = get_content_type(endpoint.file_name)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/0/": [self.handle_zde, []],
            "/hello/": [self.handle_hello, [endpoint]],
            "/i/": [self.handle_static, [f"images/{endpoint.file_name}", content_type]],
            "/s/": [self.handle_static, [f"styles/{endpoint.file_name}", content_type]],
        }

        try:
            handler, args = endpoints[endpoint.normal]
            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    def handle_static(self, file_path, content_type):
        content = read_static(file_path)
        self.respond(content, content_type=content_type)

    def handle_hello(self, endpoint):
        name = get_name_from_qs(endpoint.query_string)
        age = get_age_from_qs(endpoint.query_string)

        content = f"""
                <html>
                <head><title>Hello Page</title></head>
                <body>
                <p><a href="/"><span>"Home" Avengers</span></a></p>
                <h1>Hello {name}!</h1>
                <p>you are "{age}" yers old</p>
                <p>path: {self.path}</p>

                <form>
                <label for="xxx-id">Your name:</label>
                <input type="text" name="xxx" id="xxx-id">
                <label for="yyy-id">Your age:</label>
                <input type="text" name="yyy" id="yyy-id">
                <button type="submit">Great</button>
                </form>
                <p><img src="/i/end.jpg" alt="Avengers" align="" width="" height=""></p>
                </body>
                </html>
                """

        self.respond(content)

    def handle_zde(self):
        x = 1 / 0
        print(x)

    def handle_404(self):
        msg = """PAGE NOT FOUND!!!!!!"""
        self.respond(msg, code=404, content_type="text/plain")

    def handle_405(self):
        self.respond("", code=405, content_type="text/plain")

    def handle_500(self):
        msg = traceback.format_exc()
        self.respond(msg, code=500, content_type="text/plain")

    def respond(self, message, code=200, content_type="text/html"):
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header("Cache-control", f"max-age={settings.CACHE_AGE}")
        self.end_headers()
        self.wfile.write(payload)


