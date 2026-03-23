import io
import base64
import random
#import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
#from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Avg, Count, Min

import matplotlib
matplotlib.use('Agg') # режим без GUI
import matplotlib.pyplot as plt

from .models import UserProfile, TestResult

def home(request):
    """
    Домашнаяя страница
    """
    return render(request, 'home.html')

def register(request):
    """
    Страница регистрации
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Войдите.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """
    Страница входа
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """
    Страница выхода
    """
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('home')

@login_required
def profile(request):
    """
    Страница профиля с расширенной статистикой
    """
    profile_to_render = request.user.userprofile

    # Общие метрики
    total_tests = TestResult.objects.filter(user=request.user).count()
    perfect_tests = TestResult.objects.filter(user=request.user, score=10).count()

    # Процент идеальных тестов (с защитой от деления на ноль)
    perfect_percentage = (
        round((perfect_tests / total_tests) * 100, 1) if total_tests > 0 else 0
    )

    # Статистика по успешным тестам (score == 10)
    successful_tests = TestResult.objects.filter(user=request.user, score=10)

    min_time_perfect = successful_tests.aggregate(min=Min('total_time_seconds'))['min'] or 0
    avg_time_perfect = successful_tests.aggregate(avg=Avg('total_time_seconds'))['avg'] or 0

    # Среднее время последних 5 успешных тестов
    last_5_perfect = successful_tests.order_by('-started_at')[:5]
    avg_last_5_perfect = last_5_perfect.aggregate(avg=Avg('total_time_seconds'))['avg'] or 0

    # Последние 3 результата (все, не только идеальные)
    recent_results = TestResult.objects.filter(user=request.user).order_by('-started_at')[:3]

    return render(request, 'profile.html', {
        'profile': profile_to_render,
        'total_tests': total_tests,
        'perfect_tests': perfect_tests,
        'perfect_percentage': perfect_percentage,
        'min_time_perfect': min_time_perfect,
        'avg_time_perfect': round(avg_time_perfect, 1),
        'avg_last_5_perfect': round(avg_last_5_perfect, 1),
        'recent_results': recent_results,
    })

@login_required
def password_change(request):
    """
    Страница смены пароля
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль изменён!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {'form': form})

@login_required
def start_test(request):
    """
    Генерация 10 случайных примеров на сложение двузначных чисел
    """
    questions = []
    correct_answers = []
    for _ in range(10):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        questions.append({"a": a, "b": b})
        correct_answers.append(a + b)

    # Сохраняем в сессии — только для текущей сессии, не в БД
    request.session['test_questions'] = questions
    request.session['test_correct_answers'] = correct_answers
    request.session['test_started_at'] = timezone.now().isoformat()

    return render(request, 'test/start.html', {
        'questions': questions
    })

@login_required
def submit_test(request):
    """
    Принимаем ответы пользователя и проверяем на сервере
    """
    if request.method != "POST":
        return redirect('start_test')

    # Получаем данные из сессии
    questions = request.session.get('test_questions')
    correct_answers = request.session.get('test_correct_answers')
    started_at_str = request.session.get('test_started_at')

    if not questions or not correct_answers or not started_at_str:
        messages.error(request, "Тест не найден. Начните заново.")
        return redirect('start_test')

    # Парсим ответы пользователя
    user_answers = []
    for i in range(10):
        answer_str = request.POST.get(f'answer_{i}')
        if answer_str is None or not answer_str.strip().isdigit():
            messages.error(request, "Некорректный ответ.")
            return redirect('start_test')
        user_answers.append(int(answer_str))

    # Подсчёт баллов
    score = sum(1 for i, ans in enumerate(user_answers) if ans == correct_answers[i])

    # Время прохождения
    started_at = timezone.datetime.fromisoformat(started_at_str)
    total_time_seconds = int((timezone.now() - started_at).total_seconds())

    # Сохраняем результат в БД
    TestResult.objects.create(
        user=request.user,
        score=score,
        total_time_seconds=total_time_seconds,
        questions=questions,
        answers=user_answers
    )

    # Очищаем сессию
    del request.session['test_questions']
    del request.session['test_correct_answers']
    del request.session['test_started_at']

    # Сообщение и перенаправление
    if score == 10:
        messages.success(request, f"🏆 Отлично! 10/10 за {total_time_seconds} секунд!")
    else:
        messages.info(request, f"Вы набрали {score}/10 за {total_time_seconds} секунд.")

    return redirect('test_results')

@login_required
def test_results(request):
    """
    Последние результаты пользователя
    """
    results = TestResult.objects.filter(user=request.user).order_by('-started_at')[:10]
    return render(request, 'test/results.html', {'results': results})

@login_required
def leaderboard(request):
    """
    Топ-10 по успешным тестам и по минимальному времени
    """
    # Топ по количеству идеальных тестов (10/10)
    top_by_perfect = (
        TestResult.objects.filter(score=10)
        .values('user__username')
        .annotate(perfect_count=Count('id'))
        .order_by('-perfect_count')[:10]
    )

    # Топ по минимальному времени среди идеальных тестов
    top_by_fastest = (
        TestResult.objects.filter(score=10)
        .values('user__username')
        .annotate(min_time=Min('total_time_seconds'))
        .order_by('min_time')[:10]
    )

    return render(request, 'test/leaderboard.html', {
        'top_by_perfect': top_by_perfect,
        'top_by_fastest': top_by_fastest,
    })

@login_required
def perfect_trend(request):
    """
    График + МНК прогресса по времени идеального прохождения тестов
    """
    user = request.user
    perfect_data = TestResult.get_perfect_times_for_user(user)

    # Если нет идеальных тестов — рендерим пустую страницу без графика
    if not perfect_data:
        context = {
            'perfect_count': 0,
            'plot_url': None,
            'b': None,
        }
        return render(request, 'perfect_trend.html', context)

    x = [item[0] for item in perfect_data]  # номер теста
    y = [item[1] for item in perfect_data]  # время в секундах
    n = len(x)

    # 1 тест — только точка, без МНК
    if n == 1:
        b = None
        plt.figure(figsize=(8, 5))
        plt.scatter(x, y, color='blue', s=80, label='Идеальный тест')
        plt.title('Время на идеальный тест', fontsize=14)
        plt.xlabel('Номер идеального теста')
        plt.ylabel('Время (с)')
        plt.grid(True, alpha=0.3)
        plt.legend()
    else:
        # >= 2 теста — МНК
        def mean(a):
            return sum(a) / len(a)

        def mean_prod(a, b):
            return sum(ai * bi for ai, bi in zip(a, b)) / len(a)

        mx = mean(x)
        my = mean(y)
        mxy = mean_prod(x, y)
        mxx = mean_prod(x, x)

        # Расчёт коэффициентов b (наклона) и a
        b = (mxy - mx * my) / (mxx - mx**2)
        a = my - b * mx

        plt.figure(figsize=(8, 5))
        plt.scatter(x, y, color='blue', s=60, label='Идеальные тесты')
        linex = [x[0], x[-1]]
        liney = [a + b * xi for xi in linex]
        plt.plot(linex, liney, color='red', linestyle='--', linewidth=2, label=f'y = {a:.2f} + {b:.2f} * x')
        plt.title('Тренд времени на идеальные тесты (МНК)', fontsize=14)
        plt.xlabel('Номер идеального теста')
        plt.ylabel('Время (с)')
        plt.legend()
        plt.grid(True, alpha=0.3)

    # Сохраняем график в base64 (без GUI)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close() # Освобождаем память

    context = {
        'perfect_count': n,
        'plot_url': plot_url,
        'b': round(b, 3) if b is not None else None,
    }
    return render(request, 'perfect_trend.html', context)
