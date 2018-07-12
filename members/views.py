from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.forms import UserChangeForm

# Create your views here.
from members.models import Member
from members.forms import MemberForm, UserLoginForm, CustomUserCreationForm


def profile(request, slug):
    member_to_view = get_object_or_404(Member, slug=slug)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if request.user == member_to_view.user or request.user.is_staff:
        return render(request, "user_profile.html", {"slug": slug,
                                                     "member": member_to_view})
    else:
        raise PermissionDenied


def save_account(request):
    if request.user.is_authenticated or request.user.is_superuser:
        user_edit_form = CustomUserCreationForm(request.POST or None, request.FILES or None, instance=request.user)
        member_edit_form = MemberForm(request.POST or None, request.FILES or None, instance=request.user.member)

        if request.method == 'POST':
            if user_edit_form.is_valid() and member_edit_form.is_valid():
                saved_user = user_edit_form.save()
                member_edit_form.save()

                login(request, saved_user)

                return HttpResponseRedirect(reverse('members:default_account'))

        return render(request, "edit_account.html", {"user_form": user_edit_form,
                                                     "member_form": member_edit_form})

    else:
        raise PermissionDenied


def register(request):
    if not request.user.is_authenticated or request.user.is_superuser:
        user_form = CustomUserCreationForm(request.POST or None, request.FILES or None)
        member_form = MemberForm(request.POST or None, request.FILES or None)

        if request.method == 'POST':
            if user_form.is_valid() and member_form.is_valid():
                new_user = user_form.save()

                new_member = member_form.save(commit=False)
                new_member.user = new_user
                new_member.save()

                return HttpResponseRedirect(reverse('books:home'))

        return render(request, "create_account.html", {"user_form": user_form,
                                                       "member_form": member_form})

    else:
        return HttpResponseRedirect(reverse('books:home'))


def activate_user(request, slug):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('books:home'))
    elif not slug:
        raise PermissionDenied
    else:
        member = get_object_or_404(Member, slug=slug)

        entered_code = request.POST.get('code')

        if member.activated:
            return HttpResponseRedirect(reverse('members:login'))
        elif entered_code == member.hex_code:
            member.activated = True
            member.save()
            login(request, member.user)
            return HttpResponseRedirect(reverse('books:home'))
        elif entered_code != member.hex_code and entered_code is not None:
            return render(request, "activate.html", {"error": "Invalid Code"})
        else:
            return render(request, "activate.html", {})


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

            if user is None or not user.is_active:
                raise PermissionDenied  # placeholder for actual error
            elif user.member.activated:
                login(request, user)
                return HttpResponseRedirect(reverse('books:home'))
            else:
                return HttpResponseRedirect(reverse("members:activate", kwargs={'slug': user.member.slug}))

        return render(request, "login.html", {"user_form": user_form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('books:home'))


def daily_newsletter():
    members = Member.objects.all().filter(receive_newsletter=True)
    emails = []

    for member in members:
        emails.append(member.user.email)

    send_mail("Dog Ear Bookstore Daily Newsletter",
              "Dog Ear Bookstore\n\nDaily Promotional Code for X% Off: XXXXXX",
              "dogearbookstore@gmail.com",
              emails,
              fail_silently=False)
