from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    
    # Аутентифікація
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Профіль
    path('profile/', views.profile, name='profile'),
    
    # Створення вікторин
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('my-quizzes/', views.my_quizzes, name='my_quizzes'),
    path('edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('delete-quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('add-questions/<int:quiz_id>/', views.add_questions, name='add_questions'),
    
    # Проходження вікторини
    path('play/<int:quiz_id>/', views.play_quiz, name='play_quiz'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('results/<int:session_id>/', views.quiz_results, name='quiz_results'),
    path('play/<int:quiz_id>/<int:question_index>/', views.play_question, name='play_question'),
]