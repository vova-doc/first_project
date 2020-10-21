from datetime import date

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from applications.hello.forms.form_hello import HelloForm


def hello(request: HttpRequest) -> HttpResponse:
    name_saved = request.session.get("name")
    age_saved = request.session.get("age")

    age_new = ""
    name_new = ""
    year = None

    if age_saved:
        year = date.today().year - int(age_saved)
        age_new = age_saved

    if name_saved:
        name_new = name_saved

    context = {
        "age_new": age_new,
        "age_saved": age_saved,
        "name_new": name_new,
        "name_saved": name_saved or "Avenger",
        "theme": "light",
        "year": year,
        "form": HelloForm,
    }

    resp = render(request, "hello/hello.html", context)
    return resp


