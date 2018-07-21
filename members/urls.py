from django.urls import re_path

from members import views as members_views

app_name = "members"

urlpatterns = [
    re_path(r'^register/$', members_views.register, name='register'),
    re_path(r'^login/$', members_views.login_user, name='login'),
    re_path(r'^reset-password/$', members_views.reset_password_request, name='reset_password_form'),
    re_path(r'^reset-password/(?P<slug>[\w-]+)/(?P<hex_code>[\w-]+)$',
            members_views.reset_password,
            name='reset_password'),
    re_path(r'^logout/$', members_views.logout_user, name='logout'),
    re_path(r'^edit/$', members_views.save_account, name='edit'),
    re_path(r'^edit/delete$', members_views.delete_account, name='delete'),
    re_path(r'^activate/(?P<slug>[\w-]+)/$', members_views.activate_user, name='activate'),
    re_path(r'^(?P<slug>[\w-]+)/$', members_views.profile, name='account'),
    re_path(r'^$', members_views.default_profile, name='default_account'),
    # make / url pattern that redirects to user's own profile
]
