from django.forms import ModelForm, Select, TextInput, Textarea
from django_summernote.widgets import SummernoteWidget

from .models import *


class AdvertForm(ModelForm):

    class Meta:
        model = Advert
        fields = ['title', 'content', 'category']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок объявления'
            }),
            'content': SummernoteWidget(),
            'category': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать...'
            }),
        }


class ReplyForm(ModelForm):

    class Meta:
        model = AdvertReply
        fields = ['content']

        widgets = {
            'content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e-mail'
            }),
        }
