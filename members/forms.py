from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from members.models import Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
            "profile_picture",
            "birth_date",
            "primary_address",
            "receive_newsletter",
        ]


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=120)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username",
                  "email",
                  "first_name",
                  "last_name",
                  "password1",
                  "password2"]

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user
