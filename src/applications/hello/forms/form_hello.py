from django import forms

from applications.hello.forms.fields import NameField


class HelloForm(forms.Form):
    name = NameField(required=True, help_text="Введите ваше имя")
    age = forms.IntegerField(min_value=0, max_value=110, required=True, help_text="Введите ваш возраст")