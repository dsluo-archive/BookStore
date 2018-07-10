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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=120)
