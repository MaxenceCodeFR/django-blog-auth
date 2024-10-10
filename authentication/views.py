from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from . import forms

def sign_up(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect(settings.LOGIN_URL)
    return render(request, 'authentication/sign_up.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('login')

@login_required
def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user)
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        return redirect('blog')
    return render(request, 'authentication/upload_profile_photo.html', {'form': form})


