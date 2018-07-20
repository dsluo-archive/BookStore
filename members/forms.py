from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from members.models import Member


class PasswordResetForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "password1",
            "password2"
        ]


class CustomUserCreationForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username",
                  "email",
                  "first_name",
                  "last_name",
                  ]

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "profile_picture",
            "birth_date",
            "receive_newsletter",
        ]

    primary_address = forms.CharField(max_length=120, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['primary_address'].initial = self.instance.primary_address.location


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=120, widget=forms.PasswordInput)
