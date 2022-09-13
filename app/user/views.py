from django.shortcuts import render

# Core App import
from core.models import Excercises


# User App import
from .forms import UserForm


# @login_required
def user_view(request):
    return (render(request, "user.html", {
        'excercises': enumerate(list(Excercises.objects.all()))
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
