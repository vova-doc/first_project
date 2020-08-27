import mimetypes
from typing import AnyStr

import settings
from errors import NotFound


def to_bytes(text: AnyStr) -> bytes:
    """
    Safely converts any string to bytes
    :param text: any string
    :return: bytes
    """
    if isinstance(text, bytes):
        return text
    if not isinstance(text, str):
        err_msg = f"cannot convert {type(text)} to bytes"
        raise ValueError(err_msg)

    result = text.encode()
    return result

def read_static(path: str) -> bytes:
    """
         Reads and returns the content of static file.
         If there is no file, then NotFound exception is raised.
         :param path: path to static content
         :return: bytes of content
         """

    static_obj = settings.STATIC_DIR / path
    if not static_obj.is_file():
        static_path = static_obj.resolve().as_posix()
        err_msg = f"file <{static_path}> not found"
        raise NotFound(err_msg)

    with static_obj.open("rb") as src:
        content = src.read()

    return content


def get_content_type(file_path: str) -> str:
    if not file_path:
        return "text/html"
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type

def get_name_from_qs(qs: str) -> str:
    if not qs:
        return "world"

    pairs = qs.split("&")

    for pair in pairs:
        if "=" not in pair:
            continue
        key, value = pair.split("=")
        if key == "xxx":
            return value

    return "world"

def get_age_from_qs(qs: str) -> str:
    if not qs:
        return ""

    pairs = qs.split("&")

    for pair in pairs:
        if "=" not in pair:
            continue
        key, value = pair.split("=")
        if key == "yyy":
            return value

    return ""