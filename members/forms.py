from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from members.models import Member


class PasswordResetForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "password1",
            "password2"
        ]
        widgets = {
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2"
        ]

        widgets = {
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput
        }

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user

    def clean_email(self):
        email = self.cleaned_data['email']

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Account with this email already exists.')
        else:
            return email


class CustomUserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
        ]

    def save(self, commit=True):
        user = super(CustomUserEditForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Account with this email already exists.')
        else:
            return email


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

        if self.instance.primary_address:
            self.fields['primary_address'].initial = self.instance.primary_address.location


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(required=True)


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=120, widget=forms.PasswordInput)


class ActivationForm(forms.Form):
    code = forms.CharField()
