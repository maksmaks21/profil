from django.shortcuts import render
from django.http import HttpResponse
from .models import Quiz

def home(request):
    quizzes = Quiz.objects.all()
    context = {
        'quizzes': quizzes,
        'page_title': 'Home Page',
    }
    return render(request, 'quizzes/home.html', context)
