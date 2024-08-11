from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/dash.html', {})
    else:
        messages.error(request, 'You are not logged in!')
        return redirect('login')
