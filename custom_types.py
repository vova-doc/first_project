from itertools import takewhile
from typing import NamedTuple
from typing import Optional
from urllib.parse import urlsplit

from utils import get_content_type


class HttpRequest(NamedTuple):
    original: str
    normal: str
    method: str = "get"
    file_name: Optional[str] = None
    query_string: Optional[str] = None
    content_type: Optional[str] = "text/html"

    @classmethod
    def default(cls):
        return HttpRequest(original="", normal="/")

    @classmethod
    def from_path(cls, path: str, method: Optional[str] = None) -> "HttpRequest":
        if not path:
            return cls.default()

        components = urlsplit(path)

        segments = tuple(filter(bool, components.path.split("/")))
        non_file_segments = takewhile(lambda part: "." not in part, segments)

        compiled = "/".join(non_file_segments)
        normal = f"/{compiled}/" if compiled not in {"", "/"} else "/"

        last = segments[-1] if segments else ""
        file_name = last if "." in last else None

        content_type = get_content_type(file_name)

        return HttpRequest(
            method=method or "get",
            original=path,
            normal=normal,
            file_name=file_name,
            query_string=components.query or None,
            content_type=content_type,
        )


class User(NamedTuple):
    name: str
    age: int

    @classmethod
    def default(cls):
        return User(name="anonymous", age=0)




# from itertools import takewhile
# from typing import NamedTuple
# from typing import Optional
# from urllib.parse import urlsplit
#
# from utils import get_content_type
#
#
# class HttpRequest(NamedTuple):
#     method: str
#     original: str
#     normal: str
#     file_name: Optional[str] = None
#     query_string: Optional[str] = None
#     content_type: Optional[str] = None
#
#     @classmethod
#     def from_path(cls, path: str, method: str) -> "HttpRequest":
#         if not path:
#             from consts import ROOT_REQUEST
#             return ROOT_REQUEST
#         components = urlsplit(path)
#
#     def from_path(cls, path: str) -> "Url":
#         last = segments[-1] if segments else ""
#         file_name = last if "." in last else None
#
#     xxx = path.split("?")
#     if len(xxx) == 2:
#         path, qs = xxx
#     else:
#         path, qs = xxx[0], None
#
#     parts = tuple(filter(bool, path.split("/")))
#     compiled = "/".join(takewhile(lambda part: "." not in part, parts))
#     normal = f"/{compiled}/" if compiled not in ("", "/") else "/"
#
#     last = parts[-1] if parts else ""
#     file_name = last if "." in last else None
#
#     return Endpoint(
#         original=path, normal=normal, file_name=file_name, query_string=qs
#     )
#
#
# class User(NamedTuple):
#     age: int
#     name: str
