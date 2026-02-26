from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Ваш Email') 

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Електронна пошта', 
            'password1': 'Пароль', 
            'password2': 'Підтвердження пароля',  
        }
        help_texts = {  
            'username': 'Обов\'язково. До 150 символів. Тільки літери, цифри та @/./+/-/_', 
        }