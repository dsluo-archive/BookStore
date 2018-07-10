from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect, HttpResponse
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
    if not request.user.is_authenticated or request.user.is_superuser:
        user_form = UserCreateForm(request.POST or None, request.FILES or None)
        member_form = MemberCreateForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            if user_form.is_valid() and member_form.is_valid():
                new_user = User.objects.create_user(**user_form.cleaned_data)
                new_user.is_active = False
                new_user.save()

                new_member = member_form.save(commit=False)
                new_member.user = new_user
                new_member.save()

                return HttpResponseRedirect(reverse('books:home'))

        return render(request, "create_account.html", {"user_form": user_form,
                                                           "member_form": member_form})

    else:
        return HttpResponseRedirect(reverse('books:home'))


def activate_user(request):
    pass


def default_profile(request):
    if request.user.is_authenticated:
        return profile(request, request.user.member.slug)
    else:
        raise PermissionDenied


def login_user(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('books:home'))
    else:
        user_form = UserLoginForm(request.POST or None, request.FILES or None)

        if user_form.is_valid():
            username = user_form.cleaned_data['username'].strip()
            password = user_form.cleaned_data['password'].strip()

            user = authenticate(request, username=username, password=password)

            if user is None:
                raise PermissionDenied # placeholder for actual error
            elif user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('books:home'))
            else:
                return HttpResponse(request, "Please activate your account with the code provided.")
                # Need to make sure authenticate() still returns if is_active is False.

        return render(request, "login.html", {"user_form": user_form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('books:home'))
