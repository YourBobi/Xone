from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path("accounts/register/", views.register_request, name="register"),
    path("accounts/login/", views.login_request, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("made/urls/", views.url, name="url"),
    path("user/", views.account, name="account"),
    path('url/<str:short_url>', views.open_long_url, name='long_url'),
]