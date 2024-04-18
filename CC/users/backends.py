from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth import logout

UserModel = get_user_model()

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, verification_code=None, **kwargs):
        if username and verification_code:
            try:
                user = CoffeeUsers.objects.get(username=username)
                if user.telegram_code == verification_code:
                    return user
            except CoffeeUsers.DoesNotExist:
                pass
            
            try:
                user = CoffeeUsers.objects.get(email=username)
                if user.telegram_code == verification_code:
                    return user
            except CoffeeUsers.DoesNotExist:
                pass
        
        return None
    
    def logout(self, request):
        logout(request)