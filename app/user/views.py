from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Core App import
from core.models import Exercise

# @login_required
def user_view(request):
    return (render(request, "user.html", {
        'exercises': enumerate(list(Exercise.objects.all()))
    }))


def login_view(request):
    """Login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('user')
        else:
            return render(request, 'user.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
