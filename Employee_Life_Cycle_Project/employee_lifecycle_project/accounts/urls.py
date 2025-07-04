

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from .views import custom_logout_view
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=LoginForm,template_name='accounts/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),

]






