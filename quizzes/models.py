from django.db import models
from django.utils import timezone

class Quiz(models.Model):

    title = models.CharField(max_length=200, verbose_name="Quiz Title")
    description = models.TextField(max_length=1000, verbose_name="Quiz Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.title
    
class Meta:
    verbose_name = "Quiz"
    verbose_name_plural = "Quizzes"