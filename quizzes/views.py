from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Quiz

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
