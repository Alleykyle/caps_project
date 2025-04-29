from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    return render(request, 'landing/home.html')

def signin(request):
    return render(request, 'landing/signin.html')

def signup(request):
    return render(request, 'landing/signup.html')


def login(request):
    return render(request, "landing/login.html")

def landing_page(request):
    return render(request, "landing/landing_page.html")

def monitoring_calendar(request):
    return render(request, "landing/monitoring_calendar.html")

def csc_page(request):
    return render(request, "landing/csc_page.html")

def dashboard(request):
    return render(request, 'landing/dashboard.html')

def application_request(request) :
    return render(request, "landing/application_request.html")

def history(request) :
    return render(request, "landing/history.html")

def employees_profile(request) :
    return render(request, "landing/employees_profile.html")

def fold(request) :
    return render(request, "landing/fold.html")

def settings(request) :
    return render(request, "landing/settings.html")


