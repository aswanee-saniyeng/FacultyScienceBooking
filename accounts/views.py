from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserEditForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def manage_users(request):

    if request.user.role != 'admin':
        return redirect('home')

    users = User.objects.all().order_by('username')

    return render(
        request,
        'accounts/manage_users.html',
        {'users': users}
    )


@login_required
def edit_user(request, user_id):

    if request.user.role != 'admin':
        return redirect('home')

    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)

        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user_obj)

    return render(
        request,
        'accounts/edit_user.html',
        {'form': form, 'user_obj': user_obj}
    )


@login_required
def toggle_user_active(request, user_id):

    if request.user.role != 'admin':
        return redirect('home')

    user_obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user_obj.is_active = not user_obj.is_active
        user_obj.save()

    return redirect('manage_users')

