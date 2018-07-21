import operator
import random
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse

from books.models import PromotionCodes
from members.forms import CustomUserCreationForm, \
    MemberForm, \
    PasswordResetForm, \
    PasswordResetRequestForm, \
    UserLoginForm
# Create your views here.
from members.models import Address, Member


def profile(request, slug):
    member_to_view = get_object_or_404(Member, slug=slug)

    if not request.user.is_authenticated:
        raise PermissionDenied
    if request.user == member_to_view.user or request.user.is_staff:
        orders = member_to_view.orders.all().order_by('date')

        items_owned = []
        for order in orders:
            items_owned.extend(order.items.all())

        books_owned = []
        for item in items_owned:
            books_owned.append(item.book)
        books_owned = sorted(list(set(books_owned)), key=operator.attrgetter('name'))

        return render(request, "user_profile.html", {"slug":        slug,
                                                     "member":      member_to_view,
                                                     "books_owned": books_owned,
                                                     "orders":      orders})
    else:
        raise PermissionDenied


def save_account(request):
    if request.user.is_authenticated or request.user.is_superuser:
        user_edit_form = CustomUserCreationForm(request.POST or None, request.FILES or None, instance=request.user)
        member_edit_form = MemberForm(request.POST or None, request.FILES or None, instance=request.user.member)

        if request.method == 'POST':
            if user_edit_form.is_valid() and member_edit_form.is_valid():
                user_edit_form.save()

                member = member_edit_form.save(commit=False)
                member.primary_address, created = Address.objects. \
                    get_or_create(location=member_edit_form.cleaned_data["primary_address"])
                member.save()
                return HttpResponseRedirect(reverse('members:default_account'))

        return render(request, "edit_account.html", {"user_form":   user_edit_form,
                                                     "member_form": member_edit_form})

    else:
        raise PermissionDenied


def reset_password_request(request):
    reset_form = PasswordResetRequestForm(request.POST or None)

    if request.method == 'POST':
        if reset_form.is_valid():
            user = User.objects.all().filter(email=reset_form.cleaned_data['email']).first()

            if request.user.is_authenticated:
                if user != request.user:
                    raise PermissionDenied

            if user:
                user.member.hex_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                user.member.save()

                send_mail(
                    'Password Reset',

                    'Please follow the link below to reset your password:'
                    + '\n\nlocalhost:8000/account/reset-password/'
                    + user.member.slug + "/"
                    + user.member.hex_code,

                    'thedogearbookstore@example.com',
                    [user.email],
                    fail_silently=True,
                )

                messages.success(request, "A password reset link has been sent to your email.")
            else:
                messages.warning(request, "No account with that email could be found.")

    return render(request, "reset_password_request.html", {"reset_request_form": reset_form})


def reset_password(request, slug, hex_code):
    member = get_object_or_404(Member, slug=slug, hex_code=hex_code)

    if not member.hex_code:
        raise PermissionDenied
    else:
        if member.hex_code == hex_code:
            password_reset = PasswordResetForm(request.POST or None, instance=member.user)

            if request.method == 'POST':
                if password_reset.is_valid():
                    password_reset.save()
                    member.hex_code = ""
                    member.save()

                    messages.success(request, "Password successfully reset.")

                    return HttpResponseRedirect(reverse("members:login"))

            return render(request, "reset_password.html", {"password_reset_form": password_reset})


def delete_account(request):
    confirmation = request.POST.get('confirmation')

    if confirmation == "Yes, I want to delete my account.":
        request.user.is_active = False
        request.user.save()
        logout(request)
        return HttpResponseRedirect(reverse('books:home'))
    else:
        return render(request, "delete_account.html", {})


def register(request):
    if not request.user.is_authenticated or request.user.is_superuser:
        user_form = CustomUserCreationForm(request.POST or None, request.FILES or None, label_suffix='')
        member_form = MemberForm(request.POST or None, request.FILES or None, label_suffix='')

        if request.method == 'POST':
            if user_form.is_valid() and member_form.is_valid():
                new_user = user_form.save()

                new_member = member_form.save(commit=False)
                new_member.user = new_user
                new_member.primary_address, created = Address.objects.\
                    get_or_create(location=member_form.cleaned_data["primary_address"])
                new_member.save()

                return HttpResponseRedirect(reverse('members:activate', kwargs={"slug": new_member.slug}))

        return render(request, "register.html", {"user_form":   user_form,
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
            member.hex_code = ""
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
        user_form = UserLoginForm(request.POST or None, request.FILES or None, label_suffix='')

        if user_form.is_valid():
            username = user_form.cleaned_data['username'].strip()
            password = user_form.cleaned_data['password'].strip()

            user = authenticate(request, username=username, password=password)

            if user is None or not user.is_active:
                messages.warning(request, "Username or Password is incorrect.")
                return render(request, "login.html", {"user_form": user_form})  # placeholder for actual error
            elif user.member.activated:
                login(request, user)
                return HttpResponseRedirect(reverse('books:home'))
            else:
                return HttpResponseRedirect(reverse("members:activate", kwargs={'slug': user.member.slug}))

        return render(request, "login.html", {"user_form": user_form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('books:home'))


def daily_newsletter(code):
    new_promotion = PromotionCodes.objects.all().filter(code=code).first()

    discounted_genres = ""

    for genre in new_promotion.genres:
        discounted_genres = genre.subjects + ", "

    members = Member.objects.all().filter(receive_newsletter=True)
    emails = []

    for member in members:
        emails.append(member.user.email)

    send_mail("Dog Ear Bookstore Daily Newsletter",
              "Dog Ear Bookstore" + "\n\n"
              + "Daily Promotional Code for " + str(float(new_promotion.discount) * 100) + "% Off:"
              + new_promotion.code + "\n\n"
              + "Discount applies to select genre(s): " + discounted_genres[:-2],
              "dogearbookstore@gmail.com",
              emails,
              fail_silently=True)
