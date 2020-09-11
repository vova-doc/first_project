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

    errors = {}

    if not name_valid(name):
        errors["name"] = "name not valid"
    if not age_valid(age):
        errors["age"] = "age not valid"
    if errors:
        raise ValueError(errors)

    if isinstance(age, str) and age.isdecimal():
        age = int(age)


    return User(name=name, age=age)

def name_valid(value: str) -> bool:
    not_empty = bool(value)
    has_letters = not value.isdecimal()
    normal_length = 3 <= len(value) <= 20
    ok = all([not_empty, has_letters, normal_length])
    return ok

def age_valid(value: str) -> bool:
    if not value:
        return False
    if not value.isdecimal():
        return False
    value = int(value)
    if value > 0:
        return False
    else:
        return True

def to_str(text: AnyStr) -> str:
    result = text

    if not isinstance(text, (str, bytes)):
        result = str(text)

    if isinstance(result, bytes):
        result = result.decode()

    return result
    #Внизу такой же код
    # ok = all([value, value.isdecimal(), int(value)])
    # return ok







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
