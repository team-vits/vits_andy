from django.shortcuts import render

# Core App import
from core.models import Excercises


# User App import
from .forms import UserForm


def user_view(request):
    """ Home page view method definition """
    if request.method == 'POST':
        form = UserForm(request.POST)
    else:
        form = UserForm()
    print(dir(list(Excercises.objects.all())[0]))
    # print(form.fields)
    # [print(item) for item in dir(form)]

    return (render(request, "user.html", {
        'form': form,
        'excercises': enumerate(list(Excercises.objects.all()))
    }))
