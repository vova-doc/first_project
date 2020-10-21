from django.urls import path

from applications.hello.apps import HelloConfig
from applications.hello.views.greet import GreetView
from applications.hello.views.reset import ResetView

app_name = HelloConfig.label

urlpatterns = [
    path("", GreetView.as_view(), name="index"),
    path("update/", GreetView.as_view(), name="update"),
    path("reset/", ResetView.as_view(), name="reset"),
    ]
