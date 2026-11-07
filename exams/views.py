from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Max, Count
from datetime import timedelta
from .models import Question, ExamAttempt, StudentAnswer, Profile
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth import get_user_model
from exams.seed_questions import seed

def db_test(request):
    User = get_user_model()
    # Delete existing admin
    User.objects.filter(username='admin').delete()
    # Create a fresh admin with a known password
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    return JsonResponse({'status': 'SUCCESS', 'message': 'Admin created with password: password123'})


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, _ = Profile.objects.get_or_create(user=user)
            request.session['role'] = profile.role
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        error = None
        if not username or not password:
            error = 'Username and password are required.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif User.objects.filter(username=username).exists():
            error = 'That username is already taken.'

        if error:
            return render(request, 'login.html', {'error': error})

        # 🔒 ALWAYS create as student — teachers are created by admin only
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role='student')
        login(request, user)
        request.session['role'] = 'student'
        return redirect('dashboard')

    return redirect('login')



@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    role = profile.role
    request.session['role'] = role  # keep sidebar in sync

    # ==================== STUDENT ====================
    if role == 'student':
        attempts = ExamAttempt.objects.filter(student=request.user).order_by('-submitted_at')

        agg = attempts.aggregate(avg=Avg('score'), best=Max('score'))
        avg_score = round(agg['avg'] or 0)
        best_score = agg['best'] or 0

        lang_defs = [('French', '🇫🇷'), ('English', '🇬🇧'), ('Yoruba', '🇳🇬')]
        languages = []
        scores_by_lang = {}
        for lang_name, flag in lang_defs:
            best_lang = attempts.filter(language=lang_name).aggregate(m=Max('score'))['m']
            scores_by_lang[lang_name] = best_lang
            pct = round((best_lang or 0) / 50 * 100) if best_lang is not None else 0
            languages.append({
                'name': lang_name,
                'flag': flag,
                'best': best_lang,
                'pct': pct,
            })

        languages_tried = sum(1 for v in scores_by_lang.values() if v is not None)

        untried = [l for l, v in scores_by_lang.items() if v is None]
        if untried:
            recommended = untried[0]
        elif scores_by_lang:
            recommended = min(scores_by_lang, key=lambda k: scores_by_lang[k] or 0)
        else:
            recommended = None

        dates = sorted({a.submitted_at.date() for a in attempts}, reverse=True)
        streak = 0
        if dates:
            today = timezone.now().date()
            cursor = today if dates[0] == today else (today - timedelta(days=1))
            if dates[0] == cursor:
                streak = 1
                for d in dates[1:]:
                    cursor -= timedelta(days=1)
                    if d == cursor:
                        streak += 1
                    else:
                        break

        today = timezone.now().date()
        attempts_today = sum(1 for a in attempts if a.submitted_at.date() == today)
        daily_pct = min(100, round(attempts_today / 3 * 100))

        context = {
            'attempts': attempts,
            'avg_score': avg_score,
            'best_score': best_score,
            'streak': streak,
            'attempts_today': attempts_today,
            'daily_pct': daily_pct,
            'languages': languages,
            'recommended': recommended,
            'languages_tried': languages_tried,
        }
        return render(request, 'dashboard_student.html', context)

    # ==================== TEACHER ====================
    elif role == 'teacher':
        questions = Question.objects.filter(created_by=request.user).order_by('-id')

        french_count = questions.filter(language='French').count()
        english_count = questions.filter(language='English').count()
        yoruba_count = questions.filter(language='Yoruba').count()

        max_count = max(french_count, english_count, yoruba_count, 1)
        french_pct = round(french_count / max_count * 100)
        english_pct = round(english_count / max_count * 100)
        yoruba_pct = round(yoruba_count / max_count * 100)

        context = {
            'questions': questions,
            'french_count': french_count,
            'english_count': english_count,
            'yoruba_count': yoruba_count,
            'french_pct': french_pct,
            'english_pct': english_pct,
            'yoruba_pct': yoruba_pct,
        }
        return render(request, 'dashboard_teacher.html', context)

    # ==================== ADMIN ====================
    else:
        all_attempts = ExamAttempt.objects.all().order_by('-submitted_at')

        agg = all_attempts.aggregate(avg=Avg('score'), best=Max('score'))
        avg_score = round(agg['avg'] or 0)
        best_score = agg['best'] or 0
        unique_students = all_attempts.values('student').distinct().count()

        french_count = all_attempts.filter(language='French').count()
        english_count = all_attempts.filter(language='English').count()
        yoruba_count = all_attempts.filter(language='Yoruba').count()

        max_count = max(french_count, english_count, yoruba_count, 1)
        french_pct = max(5, round(french_count / max_count * 100))
        english_pct = max(5, round(english_count / max_count * 100))
        yoruba_pct = max(5, round(yoruba_count / max_count * 100))

        # Score distribution for donut chart
        high_count = all_attempts.filter(score__gte=40).count()
        mid_count = all_attempts.filter(score__gte=25, score__lt=40).count()
        low_count = all_attempts.filter(score__lt=25).count()
        total = all_attempts.count() or 1  # avoid divide by zero

        high_pct = round(high_count / total * 100)
        mid_pct = round(mid_count / total * 100)
        low_pct = round(low_count / total * 100)

        # Circle circumference = 2πr = 2 * 3.14159 * 60 ≈ 377
        CIRCUMFERENCE = 377
        high_arc = round(high_count / total * CIRCUMFERENCE)
        mid_arc = round(mid_count / total * CIRCUMFERENCE)
        low_arc = round(low_count / total * CIRCUMFERENCE)

        top_performers = (
            all_attempts.values('student__username')
            .annotate(best=Max('score'), attempts=Count('id'))
            .order_by('-best', '-attempts')[:5]
        )

        context = {
            'attempts': all_attempts,
            'avg_score': avg_score,
            'best_score': best_score,
            'unique_students': unique_students,
            'french_count': french_count,
            'english_count': english_count,
            'yoruba_count': yoruba_count,
            'french_pct': french_pct,
            'english_pct': english_pct,
            'yoruba_pct': yoruba_pct,
            'high_count': high_count,
            'mid_count': mid_count,
            'low_count': low_count,
            'high_pct': high_pct,
            'mid_pct': mid_pct,
            'low_pct': low_pct,
            'high_arc': high_arc,
            'mid_arc': mid_arc,
            'low_arc': low_arc,
            'top_performers': top_performers,
        }
        return render(request, 'dashboard_admin.html', context)


@login_required
def take_exam(request, language):
    if language not in ['French', 'English', 'Yoruba']:
        return redirect('dashboard')

    questions = list(Question.objects.filter(language=language)[:50])

    if request.method == 'POST':
        attempt = ExamAttempt.objects.create(
            student=request.user,
            language=language,
            total_questions=len(questions)
        )

        score = 0
        for q in questions:
            selected = request.POST.get(f'q_{q.id}', '')
            is_correct = (selected == q.correct_answer)
            if is_correct:
                score += 1
            StudentAnswer.objects.create(
                attempt=attempt,
                question=q,
                selected_answer=selected,
                is_correct=is_correct
            )

        attempt.score = score
        attempt.save()
        return redirect('result_page', attempt_id=attempt.id)

    return render(request, 'exam_page.html', {'questions': questions, 'language': language})


@login_required
def submit_exam(request):
    return redirect('dashboard')


@login_required
def result_page(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, student=request.user)
    return render(request, 'result_page.html', {'attempt': attempt})


@login_required
def view_scores(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role not in ['admin', 'teacher']:
        return redirect('dashboard')
    attempts = ExamAttempt.objects.all().order_by('-submitted_at')
    return render(request, 'scores.html', {'attempts': attempts})


@login_required
def add_question(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.role not in ['teacher', 'admin']:
        return redirect('dashboard')

    if request.method == 'POST':
        language = request.POST.get('language')
        text = request.POST.get('text', '').strip()
        option_a = request.POST.get('option_a', '').strip()
        option_b = request.POST.get('option_b', '').strip()
        option_c = request.POST.get('option_c', '').strip()
        option_d = request.POST.get('option_d', '').strip()
        correct = request.POST.get('correct')

        if (language in ['French', 'English', 'Yoruba']
                and text and option_a and option_b and option_c and option_d
                and correct in ['A', 'B', 'C', 'D']):
            Question.objects.create(
                language=language,
                text=text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct,
                created_by=request.user,
            )
            messages.success(request, f'Question added to {language} successfully!')
        else:
            messages.error(request, 'Please fill all fields and mark the correct answer.')

    return redirect('dashboard')

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def force_admin(request):
    User = get_user_model()
    # Delete any existing admin to clear conflicts
    User.objects.filter(username='admin').delete()
    # Create the admin using Django's native encryption
    User.objects.create_superuser('admin', 'admin@example.com', 'emman12345')
    return HttpResponse("<h1>SUCCESS! Admin account created. You can now log in.</h1>")

from django.http import HttpResponse

def run_seed(request):
    try:
        seed()
        return HttpResponse("<h1>SUCCESS! 150 Questions added to the database. Go check your admin panel!</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Error: {str(e)}</h1>")
    
