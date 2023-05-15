from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime

from .forms import UserRegisterForm, OtherRegistrationForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


def register(request):

    """View for registering a student at the beginning ."""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            fs = form.save()
            login(request, fs)
            return redirect('home')

            # If form is valid do something at here

    form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def login_user(request):

    """Login view """
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user/login.html', {'msg': True,
                                                       'err': f"Account for {request.POST['email']} not found!"})
    return render(request, 'user/login.html')


@login_required
def logout_user(request):

    """Logs out a user"""

    logout(request)
    return redirect('login')


def give_role(role, user):
    if role == 'System Admin':
        user.is_SYSADMIN = True
        user.is_staff = True
        user.save()
    elif role == 'Executive Committee of the National Economic Council':
        user.is_ECNEC = True
        user.save()
    elif role == 'Ministry of Planning':
        user.is_MOP = True
    elif role == 'Executing Agency':
        user.is_EXEC = True
        user.save()


@login_required
def register_other_roles(request):

    """Registers other users including another system admin too."""

    if request.user.is_SYSADMIN:
        if request.method == 'POST':

            form = OtherRegistrationForm(request.POST)
            if form.is_valid():
                fs = form.save()
                give_role(request.POST['user_role'], fs)

                form.save()
                return render(request, 'user/register_other_roles_refresh.html', {'msg': ' User Created user Successfully !'})

        form = OtherRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'user/register_other_roles.html', context=context)
    return redirect('admin-page')


def refresh(request):
    if request.method == 'POST':
        return render(request, 'user/refresh.html')
