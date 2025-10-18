# app_login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
