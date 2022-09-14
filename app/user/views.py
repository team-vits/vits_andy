from django.shortcuts import render

# Core App import
from core.models import Exercise


# User App import
from .forms import UserForm


def user_view(request):
    """ Home page view method definition """
    if request.method == 'POST':
        form = UserForm(request.POST)
    else:
        form = UserForm()

    return (render(request, "user.html", {
        'form': form,
        'exercises': enumerate(list(Exercise.objects.all()))
    }))
