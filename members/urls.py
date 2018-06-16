from django.urls import path, re_path

from members import views as members_views

app_name = "members"

urlpatterns = [
    re_path(r'^register/$', members_views.register, name='register'),
    re_path(r'^login/$', members_views.login_user, name='login'),
    re_path(r'^logout/$', members_views.logout_user, name='logout'),
    re_path(r'^(?P<slug>[\w-]+)/$', members_views.profile, name='account'),
    re_path(r'^$', members_views.default_profile, name='default_account'),
    # make / url pattern that redirects to user's own profile
]
