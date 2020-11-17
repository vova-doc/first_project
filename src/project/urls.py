import json
from pathlib import Path

from django.contrib import admin
from django.http import HttpResponse
from django.http import HttpRequest
from django.urls import path, include


# def styles (request: HttpRequest):
#     style_css = Path(__file__).parent.parent.parent / "static" / "styles" / "style.css"
#     with style_css.open("r") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="text/css")
#
# def theme_dark (request: HttpRequest):
#     style_css = Path(__file__).parent.parent.parent / "static" / "styles" / "theme_dark.css"
#     with style_css.open("r") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="text/css")
#
# def theme_light (request: HttpRequest):
#     style_css = Path(__file__).parent.parent.parent / "static" / "styles" / "theme_light.css"
#     with style_css.open("r") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="text/css")
#
# def images1 (request: HttpRequest):
#     image = Path(__file__).parent.parent.parent / "static" / "images" / "ave.jpg"
#     with image.open("rb") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="image.jpg")
#
# def images2 (request: HttpRequest):
#     image = Path(__file__).parent.parent.parent / "static" / "images" / "ima.jpg"
#     with image.open("rb") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="image.jpg")
#
# def images3 (request: HttpRequest):
#     image = Path(__file__).parent.parent.parent / "static" / "images" / "ima.jpg"
#     with image.open("rb") as f:
#         content = f.read()
#     return HttpResponse(content, content_type="image.jpg")
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def trigger_error(request):
    division_by_zero = 1 / 0

# @csrf_exempt
# def tg_view(requests: HttpRequest, *args, **kwargs):
#     try:
#         js = json.loads(requests.body)
#         print(requests.body)
#     finally:
#         return HttpResponse()
#
# class TgView(View):
#     def post(self, request, *args, **kwargs):
#         return tg_view(self.request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", include("applications.hello.urls")),
    path("b/", include("applications.blog.urls")),
    path("", include("applications.home.urls")),
    path("sentry-debug/", trigger_error),
    path("bots/", include("applications.bots.urls")),
    # path("tg/", TgView.as_view())
    # path("s/style.css/", styles),
    # path("i/ave.jpg/", images1),
    # path("i/ima.jpg/", images2),
    # path("i/end.jpg/", images3),
    # path("s/theme_dark.css/", theme_dark),
    # path("s/theme_light.css/", theme_light),
]

