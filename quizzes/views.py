from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Quiz
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm

def home(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes,
        'page_title': 'Home Page',
    }
    return render(request, 'quizzes/home.html', context)

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        'quiz': quiz,
        'page_title': f'Вікторина: {quiz.title}',
    }

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your acount ferificated')

            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'quizzes/register.html', {'form': form})

def user_login(request):
    """Вхід користувача в систему"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Вітаємо, {username}! Ви успішно увійшли.')
            return redirect('home')  # ПОВЕРТАЄМО redirect, а не рядок
        else:
            messages.error(request, 'Неправильне ім\'я користувача або пароль')
            return render(request, 'quizzes/login.html')  # ПОВЕРТАЄМО render, а не рядок
    
    # Для GET запиту
    return render(request, 'quizzes/login.html')  # ПОВЕРТАЄМО render, а не рядок

def user_logout(request):
    logout(request)
    messages.info(request, 'You logout')
    return redirect('home')