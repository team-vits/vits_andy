from django.forms import ModelForm
from core.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
