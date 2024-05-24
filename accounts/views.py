from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .forms import SignUpForm, LoginForm


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('game:index')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('game:index')

