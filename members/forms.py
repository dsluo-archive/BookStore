from django import forms
from django.contrib.auth.models import User

from members.models import Member


class MemberCreateForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
            "profile_picture",
            "birth_date",
            "primary_address",
            "receive_newsletter",
        ]


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        help_texts = {
            "username": None,
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=120)
