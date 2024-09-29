from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("post/", views.post, name="post"),
    path("search/", views.search_users, name="search_users"),
    path("myprofile/", views.profile, name="myprofile"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("accounts/login/", views.redirect1, name="redirect1"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("profile/<str:username>/follow/", views.follow_unfollow, name="follow_unfollow"),
    path("direct/<str:username>/", views.direct, name="direct"),
]
