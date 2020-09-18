import traceback
from datetime import date
from http.server import SimpleHTTPRequestHandler
from urllib import parse
from typing import Optional

from jinja2 import Template
#импортим, чтобы в html не хватить много скобок на стилях

from const import USERS_DATA, CSS_CLASS_ERROR
from custom_types import HttpRequest, User
from errors import MethodNotAllowed
from errors import NotFound
from utils import to_str, generate_new_session, build_session_header, \
    load_theme, switch_theme, store_theme, load_profile, store_profile, drop_profile
from utils import to_bytes
from utils import read_static


class MyHttp(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.dispatch("get")

    def do_POST(self):
        self.dispatch("post")

    def dispatch(self, http_method):
        req = HttpRequest.build(self.path, method=http_method, headers=self.headers)

        endpoints = {
            "/": [self.handle_static, ["index.html", "text/html"]],
            "/0/": [self.handle_zde, []],
            "/hello/": [self.handle_hello, [req]],
            "/hello-update/": [self.handle_hello_update, [req]],
            "/hello-reset/": [self.handle_hello_reset, [req]],
            "/i/": [self.handle_static, [f"images/{req.file_name}", req.content_type]],
            "/s/": [self.handle_static, [f"styles/{req.file_name}", req.content_type]],
            "/theme/": [self.handle_theme, [req]]
        }

        try:
            try:
                handler, args = endpoints[req.normal]
            except KeyError:
                raise NotFound

            handler(*args)
        except (NotFound, KeyError):
            self.handle_404()
        except MethodNotAllowed:
            self.handle_405()
        except Exception:
            self.handle_500()

    # def get_session(self) -> str:
    #     cookie = self.headers.get("Cookie", "")
    #     qs = parse.qs(cookie)
    #     session = qs.get("session", "")
    #     return session

    def handle_theme(self, request: HttpRequest) -> None:
        if request.method != "post":
            raise MethodNotAllowed

        response_kwargs = {}
        session = request.session
        if not session:
            session = generate_new_session()
            response_kwargs["session"] = session

        current_theme = load_theme(session)
        new_theme = switch_theme(current_theme)
        store_theme(session, new_theme)

        self.redirect("/hello", **response_kwargs)

    def handle_hello(self, request: HttpRequest) -> None:
        if request.method != "get":
            raise MethodNotAllowed

        profile = load_profile(request.session)
        user = User.build(profile)

        content = self.render_hello_page(request, user, user)
        # session = self.get_session()
        # if not session:
        #     session = self.generate_new_session
        #     user = User.build("")
        #     content = self.render_hello_page(user, user)
        #     self.respond(content, session=session)
        #
        # query = self.load_user_data(session)
        # user = User.build(query)
        #
        # content = self.render_hello_page(user, user)
        self.respond(content)

    def handle_hello_update(self, request: HttpRequest) -> None:
        if request.method != "post":
            raise MethodNotAllowed

        form_data = self.get_form_data()
        new_user = User.build(form_data)

        response_kwargs = {}
        session = request.session
        if not session:
            session = generate_new_session()
            response_kwargs["session"] = session

        if new_user.errors:
            saved_data = load_profile(session)
            saved_user = User.build(saved_data)
            html = self.render_hello_page(new_user, saved_user)
            self.respond(html, **response_kwargs)
        else:
            store_profile(session, form_data)
            self.redirect("/hello", **response_kwargs)

    def handle_hello_reset(self, request: HttpRequest) -> None:
        if request.method != "post":
            raise MethodNotAllowed

        drop_profile(request.session)
        self.redirect("/hello", session="")


    def render_hello_page(self,
        request: HttpRequest,
        new_user: User,
        saved_user: User,
    ) -> str:
        css_class_for_name = css_class_for_age = ""
        label_for_name = "Your name: "
        label_for_age = "Your age: "

        age_new = age_saved = saved_user.age
        name_new = name_saved = saved_user.name

        year = date.today().year - age_saved

        if new_user.errors:
            if "name" in new_user.errors:
                error = new_user.errors["name"]
                label_for_name = f"ERROR: {error}"
                css_class_for_name = CSS_CLASS_ERROR

            if "age" in new_user.errors:
                error = new_user.errors["age"]
                label_for_age = f"ERROR: {error}"
                css_class_for_age = CSS_CLASS_ERROR

            name_new = new_user.name
            age_new = new_user.age

        theme = load_theme(request.session)

        html = read_static("hello.html").decode()
        template = Template(html)

        context = {
            "age_new": age_new or "",
            "label_for_age": label_for_age,
            "label_for_name": label_for_name,
            "name_new": name_new or "",
            "name_saved": name_saved or "",
            "class_for_age": css_class_for_age,
            "class_for_name": css_class_for_name,
            "year": year,
            "theme": theme,
        }

        content = template.render(**context)

        return content


    def handle_static(self, file_path, content_type):
        content = read_static(file_path)
        self.respond(content, content_type=content_type)

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

    def respond(self, message, code=200, content_type="text/html", session: Optional[str] = None) -> None:
        payload = to_bytes(message)

        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Content-length", str(len(payload)))
        self.send_header_session(session)
        self.end_headers()
        self.wfile.write(payload)

    def redirect(self, to, session: Optional[str] = None) -> None:
        self.send_response(302)
        self.send_header("Location", to)
        self.send_header_session(session)
        self.end_headers()

    def send_header_session(self, session: Optional[str]) -> None:
        if session is None:
            return

        if session:
            header = build_session_header(session)
        else:
            header = build_session_header("expires", expires=True)

        self.send_header("Set-Cookie", header)

    def get_form_data(self) -> str:
        content_length_as_str = self.headers.get("content-length", 0)
        content_length = int(content_length_as_str)

        if not content_length:
            return ""

        payload_as_bytes = self.rfile.read(content_length)
        payload = to_str(payload_as_bytes)

        return payload


