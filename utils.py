import mimetypes
from typing import AnyStr
from urllib.parse import parse_qs

import settings
from errors import NotFound


def to_bytes(text: AnyStr) -> bytes:

    if isinstance(text, bytes):
        return text
    if not isinstance(text, str):
        err_msg = f"cannot convert {type(text)} to bytes"
        raise ValueError(err_msg)

    result = text.encode()
    return result

def read_static(path: str) -> bytes:

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


def get_user_data(query: str):

    from custom_types import User
    anonymous = User.default()

    try:
        key_value_pairs = parse_qs(query, strict_parsing=True)

    except ValueError:
        return anonymous

    name_values = key_value_pairs.get("name", [anonymous.name])
    name = name_values[0]
    age_values = key_value_pairs.get("age", [anonymous.age])
    age = age_values[0]

    if isinstance(age, str) and age.isdecimal():
        age = int(age)

    return User(name=name, age=age)

# def get_user_data(qs: str) -> User:
#     qp = parse_qs(qs)
#
#     default_list_of_names = ["World"]
#     default_list_of_ages = [0]
#
#     list_of_names = qp.get("name", default_list_of_names)
#     list_of_ages = qp.get("age", default_list_of_ages)
#
#     name = list_of_names[0]
#     age = int(list_of_ages[0])
#
#     return User(name=name, age=age)
