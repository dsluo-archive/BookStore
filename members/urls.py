from django.urls import path, re_path

from members import views as members_views

app_name = "members"

urlpatterns = [
    re_path(r'^create-account/$', members_views.create, name='create'),
    re_path(r'^(?P<slug>[\w-]+)/$', members_views.profile, name='account'),
    re_path(r'^$', members_views.default_profile, name='default_account'),  # make / url pattern that redirects to user's own profile
]
