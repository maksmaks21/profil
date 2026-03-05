from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Quiz Title")
    description = models.TextField(max_length=1000, verbose_name="Quiz Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='quizzes')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    
    hours = models.IntegerField(default=0, verbose_name='Годин')
    minutes = models.IntegerField(default=1, verbose_name='Хвилин')
    seconds = models.IntegerField(default=0, verbose_name='Секунд')
    has_time_limit = models.BooleanField(default=True, verbose_name='Має обмеження часу')

    def __str__(self):
        return self.title
    
    def get_total_seconds(self):
        if not self.has_time_limit:
            return None
        return self.hours * 3600 + self.minutes * 60 + self.seconds
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name='Вікторина')
    text = models.TextField(verbose_name='text questions')
    order = models.IntegerField(default=0, verbose_name='Порядок питання')

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"
    
    class Meta:
        ordering = ['order']
        verbose_name = "Питання"
        verbose_name_plural = "Питання"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Питання")
    text = models.CharField(max_length=255, verbose_name="Текст відповіді")
    is_correct = models.BooleanField(default=False, verbose_name="Правильна відповідь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:20]}"


class QuizSession(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='sessions', verbose_name="Вікторина")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions', verbose_name="Користувач")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Початок")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершення")
    score = models.IntegerField(default=0, verbose_name="Бали")
    is_completed = models.BooleanField(default=False, verbose_name="Завершено")

    class Meta:
        verbose_name = "Сесія вікторини"
        verbose_name_plural = "Сесії вікторин"
        unique_together = ['quiz', 'user', 'is_completed']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


class UserAnswer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name='answers', verbose_name="Сесія")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Питання")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name="Відповідь")
    is_correct = models.BooleanField(default=False, verbose_name="Правильно")
    time_spent = models.IntegerField(default=0, verbose_name="Час на відповідь (сек)")
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="Час відповіді")

    class Meta:
        verbose_name = "Відповідь користувача"
        verbose_name_plural = "Відповіді користувачів"
        unique_together = ['session', 'question']

    def __str__(self):
        return f"{self.session.user.username} - {self.question.text[:30]}"