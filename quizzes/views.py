from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Quiz, Question, Answer, QuizSession, UserAnswer
from .forms import UserRegisterForm, QuizCreateForm, QuestionForm, AnswerFormSet

# ======= ГЛОБАЛЬНІ ПЕРЕРОБКИ =======
# Цей файл містить основні "view" функції для застосунку вікторин.
# Кожна функція відповідає за обробку HTTP-запитів і повернення відповідної
# HTML-сторінки чи JSON-результату. Коментарі пояснюють, які моделі
# залучені і як працює логіка.


# Головна сторінка
# Показує всі активні вікторини, відсортовані за датою створення.
# Викликається на маршрут 'home'.
def home(request):
    """Головна сторінка з популярними та новими вікторинами"""
    quizzes = Quiz.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'quizzes': quizzes,
        'page_title': 'Home Page',
    }
    return render(request, 'quizzes/home.html', context)


# Детальна сторінка вікторини
# Виводить інформацію про конкретну вікторину: опис, автора, кількість
# питань тощо. Параметр `quiz_id` передається через URL.
def quiz_detail(request, quiz_id):
    """Детальна сторінка вікторини"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        'quiz': quiz,
        'page_title': f'Вікторина: {quiz.title}',
    }
    return render(request, 'quizzes/quiz_detail.html', context)


# Реєстрація
# Обробляє POST-запит з формою реєстрації. Якщо дані валідні, зберігає нового
# користувача, робить логін та переспрямовує на головну з повідомленням.
def register(request):
    """Реєстрація нового користувача"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Реєстрація пройшла успішно! Ласкаво просимо!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'quizzes/register.html', {'form': form})


# Вхід в систему
# Оновлена версія - тільки для звичайних користувачів (не адмінів)
def user_login(request):
    """Вхід користувача в систему (тільки для звичайних користувачів)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Спроба аутентифікації
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Перевіряємо, чи це звичайний користувач (не адмін)
            if not user.is_superuser and not user.is_staff:
                login(request, user)
                messages.success(request, f'Вітаємо, {username}! Ви успішно увійшли.')
                return redirect('home')
            else:
                # Якщо це адмін - повідомляємо, що вхід тільки через адмін-панель
                messages.error(request, 'Адміністратори повинні входити через адмін-панель (/admin)')
        else:
            messages.error(request, 'Неправильне ім\'я користувача або пароль')
    
    return render(request, 'quizzes/login.html')


# Вихід з системи
# Видаляє сесію користувача та показує інформаційне повідомлення.
def user_logout(request):
    """Вихід користувача з системи"""
    logout(request)
    messages.info(request, 'Ви вийшли з системи. До зустрічі!')
    return redirect('home')


# Профіль користувача
# Показує вікторини, створені поточним користувачем, та загальну кількість.
@login_required
def profile(request):
    """Сторінка профілю користувача"""
    user_quizzes = Quiz.objects.filter(creator=request.user).order_by('-created_at')
    total_quizzes = user_quizzes.count()
    
    context = {
        'user': request.user,
        'user_quizzes': user_quizzes,
        'total_quizzes': total_quizzes,
    }
    
    return render(request, 'quizzes/profile.html', context)


# ========== ФУНКЦІЇ ДЛЯ СТВОРЕННЯ ВІКТОРИН ==========

@login_required
def create_quiz(request):
    """Створення нової вікторини"""
    if request.method == 'POST':
        form = QuizCreateForm(request.POST)
        if form.is_valid():
            # Зберігаємо вікторину з поточним користувачем
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            
            messages.success(request, 'Вікторину успішно створено! Тепер додайте питання.')
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        form = QuizCreateForm()
    
    return render(request, 'quizzes/create_quiz.html', {'form': form})


@login_required
def my_quizzes(request):
    """Список вікторин поточного користувача"""
    quizzes = Quiz.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'quizzes/my_quizzes.html', {'quizzes': quizzes})


@login_required
def add_questions(request, quiz_id):
    """Додавання питань до вікторини"""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    
    if request.method == 'POST':
        # Отримуємо текст питання
        question_text = request.POST.get('text')
        
        if question_text:
            # Створюємо питання
            question = Question.objects.create(
                quiz=quiz,
                text=question_text,
                order=quiz.questions.count() + 1
            )
            
            # Обробка відповідей
            correct_answer = request.POST.get('correct_answer')
            answers_added = False
            
            for i in range(1, 5):  # Максимум 4 відповіді
                answer_text = request.POST.get(f'answer_{i}')
                
                if answer_text and answer_text.strip():  # Якщо поле не пусте
                    is_correct = (correct_answer == str(i))
                    Answer.objects.create(
                        question=question,
                        text=answer_text.strip(),
                        is_correct=is_correct
                    )
                    answers_added = True
            
            if answers_added:
                messages.success(request, 'Питання додано!')
                
                # Перевіряємо, чи хочемо додати ще питання
                if 'add_another' in request.POST:
                    return redirect('add_questions', quiz_id=quiz.id)
                else:
                    return redirect('quiz_detail', quiz_id=quiz.id)
            else:
                # Якщо не додано жодної відповіді - видаляємо питання
                question.delete()
                messages.error(request, 'Додайте хоча б одну відповідь!')
        else:
            messages.error(request, 'Введіть текст питання!')
    
    return render(request, 'quizzes/add_questions.html', {'quiz': quiz})


@login_required
def edit_quiz(request, quiz_id):
    """Редагування вікторини"""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    
    if request.method == 'POST':
        form = QuizCreateForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вікторину оновлено!')
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizCreateForm(instance=quiz)
    
    return render(request, 'quizzes/edit_quiz.html', {'form': form, 'quiz': quiz})


@login_required
def delete_quiz(request, quiz_id):
    """Видалення вікторини"""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Вікторину видалено!')
        return redirect('my_quizzes')
    
    return render(request, 'quizzes/delete_quiz.html', {'quiz': quiz})


# ========== ФУНКЦІЇ ДЛЯ ПРОХОДЖЕННЯ ВІКТОРИН ==========

@login_required
def play_quiz(request, quiz_id):
    """Початок проходження вікторини"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Перевіряємо, чи користувач вже проходив цю вікторину
    existing_session = QuizSession.objects.filter(
        quiz=quiz,
        user=request.user,
        is_completed=True
    ).first()
    
    if existing_session:
        messages.warning(request, 'Ви вже проходили цю вікторину!')
        return redirect('quiz_results', session_id=existing_session.id)
    
    # Створюємо нову сесію або повертаємо незавершену, щоб не губити дані
    session, created = QuizSession.objects.get_or_create(
        quiz=quiz,
        user=request.user,
        is_completed=False,
        defaults={'started_at': timezone.now()}
    )
    
    # Отримуємо всі питання вікторини, сортуємо за полем order
    questions = list(quiz.questions.all().order_by('order'))
    
    if not questions:
        messages.error(request, 'У цій вікторині немає питань!')
        return redirect('quiz_detail', quiz_id=quiz.id)
    
    # Зберігаємо масив ID питань, індекс поточного питання та id сесії
    request.session['quiz_questions'] = [q.id for q in questions]
    request.session['current_question_index'] = 0
    request.session['quiz_session_id'] = session.id
    
    # Перенаправляємо на перше питання
    return redirect('play_question', quiz_id=quiz.id, question_index=0)


@login_required
def play_question(request, quiz_id, question_index):
    """Сторінка з питанням"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Отримуємо список питань, збережених у сесії браузера
    question_ids = request.session.get('quiz_questions', [])
    
    if not question_ids or question_index >= len(question_ids):
        # Захищаємося від підозрілого чи некоректного URL
        messages.error(request, 'Помилка завантаження питань')
        return redirect('quiz_detail', quiz_id=quiz.id)
    
    # Витягаємо конкретне питання з бази по ID
    question = get_object_or_404(Question, id=question_ids[question_index])
    
    # Отримуємо поточну сесію користувача
    session_id = request.session.get('quiz_session_id')
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    
    # Якщо відповідь на питання вже є, автоматично переходимо далі
    existing_answer = UserAnswer.objects.filter(
        session=session,
        question=question
    ).first()
    
    if existing_answer:
        next_index = question_index + 1
        if next_index < len(question_ids):
            return redirect('play_question', quiz_id=quiz.id, question_index=next_index)
        else:
            return redirect('quiz_results', session_id=session.id)
    
    context = {
        'quiz': quiz,
        'question': question,
        'question_index': question_index,
        'total_questions': len(question_ids),
        'session': session,
    }
    
    return render(request, 'quizzes/play_question.html', context)


@login_required
def submit_answer(request):
    """Обробка відповіді на питання"""
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer_id')
        time_spent = request.POST.get('time_spent', 0)
        
        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)
        
        # Отримуємо сесію
        session_id = request.session.get('quiz_session_id')
        session = get_object_or_404(QuizSession, id=session_id, user=request.user)
        
        # Перевіряємо чи вже відповідали
        existing = UserAnswer.objects.filter(session=session, question=question).exists()
        if existing:
            return JsonResponse({'success': False, 'error': 'Вже відповіли'})
        
        # Зберігаємо відповідь
        is_correct = answer.is_correct
        user_answer = UserAnswer.objects.create(
            session=session,
            question=question,
            answer=answer,
            is_correct=is_correct,
            time_spent=time_spent
        )
        
        # Оновлюємо рахунок сесії: плюс 10 балів за правильну відповідь
        if is_correct:
            session.score += 10
            session.save()
        
        # Передаємо назад статус для відображення на фронтенді
        return JsonResponse({
            'success': True,
            'is_correct': is_correct,
            'correct_answer': question.answers.filter(is_correct=True).first().text if not is_correct else None,
            'score': session.score
        })
    
    # Якщо метод не POST, повертаємо невдалу відповідь
    return JsonResponse({'success': False})


@login_required
def quiz_results(request, session_id):
    """Сторінка з результатами"""
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    
    # Позначаємо сесію як завершену
    if not session.is_completed:
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()
    
    # Отримуємо статистику
    total_questions = session.quiz.questions.count()
    correct_answers = session.answers.filter(is_correct=True).count()
    
    # Отримуємо рейтинг всіх учасників
    all_sessions = QuizSession.objects.filter(
        quiz=session.quiz,
        is_completed=True
    ).order_by('-score')[:10]
    
    # Знаходимо місце користувача
    rank = None
    for i, s in enumerate(all_sessions, 1):
        if s.id == session.id:
            rank = i
            break
    
    context = {
        'session': session,
        'quiz': session.quiz,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score': session.score,
        'all_sessions': all_sessions,
        'rank': rank,
    }
    
    return render(request, 'quizzes/results.html', context)