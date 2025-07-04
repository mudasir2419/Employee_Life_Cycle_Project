from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    return redirect('login')