from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm


# Create your views here.
def index(request):
    return render(request, 'website/index.html', {})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'website/login.html', {})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out, see you soon!')
    return redirect('login')


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, 'Rest easy traveler, your credentials have been verified. Welcome to the forge!')
                return redirect('index')
        else:
            form = SignUpForm()
            return render(request, 'website/registration.html', {'form': form})

        return render(request, 'website/registration.html', {'form': form})

