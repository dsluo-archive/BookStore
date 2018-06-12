from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

# Create your views here.

from members.models import Member
from members.forms import UserForm, MemberForm


def profile(request, slug):
    member_to_view = get_object_or_404(Member, slug=slug)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if request.user == member_to_view.user or member_to_view.public_account:
        return render(request, "user_profile.html", {"slug": slug,
                                                     "member": member_to_view})
    else:
        raise PermissionDenied


def create(request):
    user_form = UserForm(request.POST or None, request.FILES or None)
    member_form = MemberForm(request.POST or None, request.FILES or None)

    if user_form.is_valid() and member_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.username = new_user.first_name + "_" + new_user.last_name
        new_user.save()

        new_member = member_form.save(commit=False)
        new_member.user = new_user
        new_member.save()

        return render(request, "home_page.html", {})

    return render(request, "create_account.html", {"user_form": user_form,
                                                   "member_form": member_form})


def default_profile(request):
    user = Member.objects.all().filter(user=request.user).first()

    if user:
        return profile(request, user.slug)
    else:
        raise PermissionDenied
