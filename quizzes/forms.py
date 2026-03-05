from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Quiz, Question, Answer

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

class QuizCreateForm(forms.ModelForm):
    """Форма для створення вікторини"""
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'has_time_limit', 'hours', 'minutes', 'seconds']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Назва вікторини'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Опис вікторини'
            }),
            'hours': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'max': 24
            }),
            'minutes': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'max': 59
            }),
            'seconds': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'max': 59
            }),
        }
        labels = {
            'title': 'Назва вікторини',
            'description': 'Опис',
            'has_time_limit': 'Обмежити час',
            'hours': 'Годин',
            'minutes': 'Хвилин',
            'seconds': 'Секунд',
        }

class QuestionForm(forms.ModelForm):
    """Форма для додавання питання"""
    class Meta:
        model = Question
        fields = ['text', 'order']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Текст питання'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0
            }),
        }
        labels = {
            'text': 'Текст питання',
            'order': 'Порядковий номер',
        }

class AnswerForm(forms.ModelForm):
    """Форма для додавання відповіді"""
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Текст відповіді'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'text': 'Текст відповіді',
            'is_correct': 'Правильна відповідь',
        }

from django.forms import inlineformset_factory

# Формсет для відповідей (щоб додавати кілька відповідей до питання)
AnswerFormSet = inlineformset_factory(
    Question, 
    Answer, 
    form=AnswerForm, 
    extra=4,           # Показувати 4 порожніх форми
    min_num=2,         # Мінімум 2 відповіді
    max_num=4,         # Максимум 4 відповіді
    can_delete=True    # Можна видаляти
)