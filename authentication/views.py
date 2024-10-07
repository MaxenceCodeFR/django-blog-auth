from django.shortcuts import render, redirect
from pyexpat.errors import messages
from . import forms
from django.contrib.auth import authenticate, login, logout

def login_page(request):
    form = forms.LoginForm()
    message = ''

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('blog')
        message = 'Identifiants invalides !'

    return render(request,'authentication/login.html', {'form': form, 'message': message})

def logout_page(request):
    logout(request)
    return redirect('login')

