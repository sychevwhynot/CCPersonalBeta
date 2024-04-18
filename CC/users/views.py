from django.shortcuts import render, redirect
from .forms import VerificationCodeForm
from .bot_telegram import CoffeeUsers
from .bot_telegram import delete_telegram_code
from .bot_email import CoffeeUsers
from .bot_email import delete_email_code
from django.contrib import messages
from .bot_email import *
from .bot_telegram import *
from .forms import *
from .backends import *
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import authenticate, login
from django.urls import reverse
from urllib.parse import urlparse
from django.views.generic import FormView
from .backends import CustomAuthenticationBackend
from django.contrib.auth import logout

def username_email_view(request):
    if request.method == 'POST':
        form = UsernameEmailForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            try:
                user = CoffeeUsers.objects.get(email=username_or_email)
                code = save_email_code(username_or_email)
                send_email_message(username_or_email, code)
            except CoffeeUsers.DoesNotExist:
                try:
                    user = CoffeeUsers.objects.get(username=username_or_email)
                    save_telegram_code_and_send_message(username_or_email)
                except CoffeeUsers.DoesNotExist:
                    messages.error(request, "Пользователь не найден.")
                    return render(request, 'users/login.html', {'form': form})
            
            request.session['username_or_email'] = username_or_email  # Сохраняем в сессии username или email
            return redirect('verification')  # Перенаправляем на страницу ввода кода подтверждения
        else:
            messages.error(request, "Форма заполнена некорректно.")
    else:
        form = UsernameEmailForm()
    return render(request, 'users/login.html', {'form': form})


def enter_verification_code(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']
            username_or_email = request.session.get('username_or_email')
            backend = CustomAuthenticationBackend()  # Используем ваш собственный бэкенд
            user = backend.authenticate(request, username=username_or_email, verification_code=verification_code)

            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Укажите стандартный бэкенд
                request.session['user_id'] = user.id
                return redirect('feed:feedlist')
            else:
                messages.error(request, "Неправильный код подтверждения.")
        else:
            messages.error(request, "Форма заполнена некорректно.")
    else:
        form = VerificationCodeForm()
    return render(request, 'users/verification.html', {'form': form})



def logout_view(request):
    backend = CustomAuthenticationBackend()
    backend.logout(request)
    return redirect('login')
