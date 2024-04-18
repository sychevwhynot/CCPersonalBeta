from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UsernameEmailForm(forms.Form):
    username_or_email = forms.CharField(label='Username or Email')

class VerificationCodeForm(forms.Form):
    verification_code = forms.CharField(label='Verification Code')