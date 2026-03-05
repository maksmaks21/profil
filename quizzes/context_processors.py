from .models import Quiz

def global_quiz_data(request):
    """Додає загальні дані для всіх шаблонів"""
    return {
        'total_quizzes_count': Quiz.objects.filter(is_active=True).count(),
        'is_playing': request.session.get('quiz_session_id') is not None,
    }