from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import F
import json

from .models import Category, Quiz, Question, Answer, QuizAttempt, UserResponse, UserProfile, SavedQuiz
from .ai_generator import AIQuizGenerator, generate_sample_quiz


@login_required
def dashboard(request):
    """Main dashboard view"""
    categories = Category.objects.prefetch_related('quizzes').all()
    context = {'categories': categories}
    return render(request, 'dashboard.html', context)


@login_required
def quiz_generator_page(request):
    """Quiz generator page"""
    return render(request, 'quiz_generator.html')


@login_required
def category_quizzes(request, slug):
    """Show quizzes in a category"""
    category = get_object_or_404(Category, slug=slug)
    quizzes = category.quizzes.filter(is_active=True).select_related('category', 'created_by')
    context = {'category': category, 'quizzes': quizzes}
    return render(request, 'category_quizzes.html', context)


@login_required
def start_quiz(request, quiz_id):
    """Start a new quiz attempt"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Create a new quiz attempt
    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz,
        total_questions=quiz.questions.count()
    )
    
    return redirect('take_quiz', attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    """Take quiz view"""
    attempt = get_object_or_404(
        QuizAttempt.objects.select_related('quiz'),
        id=attempt_id,
        user=request.user
    )
    
    if attempt.completed_at:
        return redirect('quiz_results', attempt_id=attempt.id)
    
    quiz = attempt.quiz
    questions = quiz.questions.prefetch_related('answers').all()
    
    # Prepare questions data for JSON
    questions_data = [
        {
            'id': q.id,
            'text': q.text,
            'answers': [{'id': a.id, 'text': a.text} for a in q.answers.all()]
        }
        for q in questions
    ]
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'questions_json': json.dumps(questions_data)
    }
    return render(request, 'quiz_take.html', context)


@login_required
@require_POST
def save_response(request):
    """Save user's answer to a question"""
    data = json.loads(request.body)
    attempt_id = data.get('attempt_id')
    question_id = data.get('question_id')
    answer_id = data.get('answer_id')
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(Answer, id=answer_id)
    
    # Create or update response
    response, created = UserResponse.objects.update_or_create(
        attempt=attempt,
        question=question,
        defaults={
            'selected_answer': answer,
            'is_correct': answer.is_correct
        }
    )
    
    return JsonResponse({'success': True})


@login_required
@require_POST
def submit_quiz(request, attempt_id):
    """Submit quiz and calculate score"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if attempt.completed_at:
        return JsonResponse({'error': 'Quiz already submitted'}, status=400)
    
    # Calculate score
    correct_count = attempt.responses.filter(is_correct=True).count()
    time_taken = int((timezone.now() - attempt.started_at).total_seconds())
    
    # Update attempt
    QuizAttempt.objects.filter(id=attempt_id).update(
        score=correct_count,
        completed_at=timezone.now(),
        time_taken_seconds=time_taken
    )
    
    # Update user profile using F expressions
    from django.db.models import F
    UserProfile.objects.filter(user=request.user).update(
        quizzes_completed=F('quizzes_completed') + 1,
        total_score=F('total_score') + correct_count
    )
    
    return JsonResponse({'success': True, 'redirect': f'/results/{attempt.id}/'})


@login_required
def quiz_results(request, attempt_id):
    """Show quiz results"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if not attempt.completed_at:
        return redirect('take_quiz', attempt_id=attempt.id)
    
    responses = attempt.responses.all().select_related('question', 'selected_answer')
    wrong_answers = attempt.total_questions - attempt.score
    
    # Format time taken
    minutes = attempt.time_taken_seconds // 60
    seconds = attempt.time_taken_seconds % 60
    time_taken = f"{minutes:02d}:{seconds:02d}"
    
    # Calculate progress ring offset (for SVG circle animation)
    # Circle circumference = 2 * π * r = 2 * 3.14 * 50 = 314
    circumference = 314
    progress_offset = circumference - (circumference * attempt.percentage_score / 100)
    
    context = {
        'attempt': attempt,
        'responses': responses,
        'wrong_answers': wrong_answers,
        'time_taken': time_taken,
        'progress_offset': progress_offset
    }
    return render(request, 'results.html', context)


@login_required
def my_results(request):
    """Show user's quiz history"""
    attempts = QuizAttempt.objects.filter(
        user=request.user,
        completed_at__isnull=False
    ).select_related('quiz', 'quiz__category').order_by('-completed_at')
    return render(request, 'my_results.html', {'attempts': attempts})


@login_required
def leaderboard(request):
    """Show global leaderboard"""
    top_users = UserProfile.objects.select_related('user').order_by('-total_score')[:50]
    return render(request, 'leaderboard.html', {'top_users': top_users})


@login_required
def saved_quizzes(request):
    """Show user's saved quizzes"""
    saved = SavedQuiz.objects.filter(user=request.user).select_related('quiz', 'quiz__category')
    return render(request, 'saved_quizzes.html', {'saved_quizzes': saved})


@login_required
def generate_ai_quiz(request):
    """Generate a new quiz using AI"""
    topic = request.GET.get('topic', 'General Knowledge')
    category_name = request.GET.get('category', 'General')
    
    # Check if this is an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Try to generate with AI, fallback to sample quiz
    try:
        generator = AIQuizGenerator()
        quiz = generator.generate_quiz(
            category_name=category_name,
            topic=topic,
            num_questions=10,
            difficulty='medium'
        )
    except Exception as e:
        print(f"AI generation failed: {e}")
        quiz = generate_sample_quiz(category_name, topic, 10)
    
    if quiz:
        if is_ajax:
            return JsonResponse({
                'success': True,
                'quiz_id': quiz.id,
                'quiz_title': quiz.title
            })
        else:
            messages.success(request, f'Quiz "{quiz.title}" generated successfully!')
            return redirect('start_quiz', quiz_id=quiz.id)
    else:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'error': 'Failed to generate quiz'
            })
        else:
            messages.error(request, 'Failed to generate quiz')
            return redirect('dashboard')


@login_required
@require_POST
def generate_custom_quiz(request):
    """Generate a custom quiz from the sidebar form"""
    try:
        data = json.loads(request.body)
        topic = data.get('topic', 'General Knowledge')
        level = data.get('level', 'intermediate')
        num_questions = int(data.get('num_questions', 10))
        
        # Validate inputs
        if not topic:
            return JsonResponse({
                'success': False,
                'error': 'Topic is required'
            }, status=400)
        
        if level not in ['beginner', 'intermediate', 'advanced', 'expert']:
            return JsonResponse({
                'success': False,
                'error': 'Invalid level'
            }, status=400)
        
        if num_questions < 1:
            return JsonResponse({
                'success': False,
                'error': 'Number of questions must be at least 1'
            }, status=400)
        
        # Generate quiz with AI
        try:
            generator = AIQuizGenerator()
            quiz = generator.generate_quiz(
                category_name=topic,
                topic=topic,
                num_questions=num_questions,
                difficulty=level
            )
            
            if quiz:
                return JsonResponse({
                    'success': True,
                    'quiz_id': quiz.id,
                    'quiz_title': quiz.title
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'AI could not generate the quiz. Please try with fewer questions or a different topic.'
                }, status=500)
        except Exception as gen_error:
            error_msg = str(gen_error)
            if "too large" in error_msg.lower() or "reduce" in error_msg.lower():
                return JsonResponse({
                    'success': False,
                    'error': error_msg
                }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Quiz generation failed: {error_msg}'
                }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        print(f"Error generating custom quiz: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name
        )
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


@login_required
def profile_view(request):
    """User profile page"""
    profile = request.user.profile
    attempts = QuizAttempt.objects.filter(
        user=request.user,
        completed_at__isnull=False
    ).select_related('quiz', 'quiz__category').order_by('-completed_at')[:10]
    
    total_attempts = attempts.count()
    if total_attempts > 0:
        scores = [attempt.percentage_score for attempt in attempts]
        average_score = int(sum(scores) / total_attempts)
        total_score = sum(attempt.score for attempt in attempts)
        best_score = int(max(scores))
    else:
        average_score = total_score = best_score = 0
    
    context = {
        'profile': profile,
        'total_attempts': total_attempts,
        'average_score': average_score,
        'total_score': total_score,
        'best_score': best_score,
        'recent_attempts': attempts,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        user = request.user
        
        # Update user information
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Validate email
        if email and User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, 'This email is already in use by another account.')
            return redirect('edit_profile')
        
        user.email = email
        user.save()
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        # Update profile model
        profile.mobile_number = request.POST.get('mobile_number', '').strip()
        profile.address = request.POST.get('address', '').strip()
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'edit_profile.html', {'profile': profile})
