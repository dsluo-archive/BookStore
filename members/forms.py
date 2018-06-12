from django import forms
from django.contrib.auth.models import User

from members.models import Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
            "profile_picture",
            "birth_date",
            "primary_address",
            "recv_newsletter",
            "vendor_auth",
            "vendor_actual",
            "client_auth",
            "client_actual",
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
