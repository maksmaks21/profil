from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Quiz, Question, Answer, QuizSession, UserAnswer

class AnswerInline(admin.TabularInline):
    """Для відображення відповідей всередині питання"""
    model = Answer
    extra = 4
    min_num = 2
    max_num = 4
    
    def clean(self, forms, for_commit=False):
        """Перевіряємо що є хоча б одна правильна відповідь"""
        super().clean(forms, for_commit)
        
        has_correct = False
        for form in forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            if form.cleaned_data.get('is_correct') and not form.cleaned_data.get('DELETE'):
                has_correct = True
                break
        
        if not has_correct:
            raise ValidationError('Потрібно вибрати хоча б одну правильну відповідь')

class QuestionInline(admin.TabularInline):
    """Для відображення питань всередині вікторини"""
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'is_active', 'get_time_display')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    
    def get_time_display(self, obj):
        if not obj.has_time_limit:
            return "Без часу"
        return f"{obj.hours}год {obj.minutes}хв"
    get_time_display.short_description = "Час"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('text',)

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'is_completed', 'started_at')
    list_filter = ('is_completed', 'quiz')
    search_fields = ('user__username', 'quiz__title')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'is_correct', 'time_spent')
    list_filter = ('is_correct',)