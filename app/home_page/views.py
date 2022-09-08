from django.views.generic import TemplateView
from django.shortcuts import render
import random
from core.models import UserManager


# Function Based View.
def home_view(request):
    """ Home page view method definition """
    data = {'test': random.randrange(1, 100)}
    return(render(request, "home.html", data))
