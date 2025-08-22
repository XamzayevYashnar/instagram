from django.urls import path
from .views import register_view, login_view, logout

urlpatterns = [
   path('register/', register_view, name='register'),
   path("accounts/login/", login_view, name="login"),
   path('logout/', logout, name='logout')
    ]