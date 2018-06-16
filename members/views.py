from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
from members.models import Member
from members.forms import UserCreateForm, MemberCreateForm, UserLoginForm


def profile(request, slug):
    member_to_view = get_object_or_404(Member, slug=slug)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if request.user == member_to_view.user or member_to_view.user.is_active or request.user.is_staff:
        return render(request, "user_profile.html", {"slug": slug,
                                                     "member": member_to_view})
    else:
        raise PermissionDenied


def register(request):
    user_form = UserCreateForm(request.POST or None, request.FILES or None)
    member_form = MemberCreateForm(request.POST or None, request.FILES or None)

    if user_form.is_valid() and member_form.is_valid():
        new_user = User.objects.create_user(**user_form.cleaned_data)
        login(request, user=new_user)

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
        raise Http404


def login_user(request):

    if request.user.is_authenticated:
        return render(request, "home_page.html", {})
    else:
        user_form = UserLoginForm(request.POST or None, request.FILES or None)

        if user_form.is_valid():
            username = user_form.cleaned_data['username'].strip()
            password = user_form.cleaned_data['password'].strip()

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, "home_page.html", {})
            else:
                raise PermissionDenied  # placeholder for actual error

        return render(request, "login.html", {"user_form": user_form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('members:login'))
