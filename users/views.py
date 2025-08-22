from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')  

        if not username or not email or not phone_number or not password1 or not password2:
            messages.error(request, "Barcha maydonlarni to‘ldiring.")
            return render(request, 'register.html')

        if password1 != password2:
            messages.error(request, "Parollar mos emas!")
            return render(request, 'register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon mavjud.")
            return render(request, 'register.html')

        if CustomUser.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Bu telefon raqami allaqachon mavjud.")
            return render(request, 'register.html')

        user = CustomUser.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
            avatar=avatar if avatar else 'avatars/default_avatar.png',
            password=make_password(password1)
        )

        login(request, user)
        return redirect('home') 

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username yoki parol noto‘g‘ri!')

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')