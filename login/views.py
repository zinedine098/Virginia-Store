# app_login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('halaman_kasir')  # ganti dengan halaman utama
        else:
            messages.error(request, 'Username atau password salah')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.nama = request.POST.get('nama', profile.nama)
        profile.status = request.POST.get('status', profile.status)
        profile.slogan = request.POST.get('slogan', profile.slogan)
        profile.alamat = request.POST.get('alamat', profile.alamat)
        profile.no_telephon = request.POST.get('no_telepon', profile.no_telephon)
        if 'foto_profile' in request.FILES:
            profile.foto_profile = request.FILES['foto_profile']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'profile.html', {'profile': profile})
