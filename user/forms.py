from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UserRegisterForm(UserCreationForm):

    """Form to register a Normal user/citizen"""

    class Meta:
        model = User
        fields = ['email', 'name', 'password1', 'password2']


class OtherRegistrationForm(UserCreationForm):

    """Form to register other role users"""

    class Meta:
        model = User
        fields = ['name', 'email', 'user_role', 'password1', 'password2']


