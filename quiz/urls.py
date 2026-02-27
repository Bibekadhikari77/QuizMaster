from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('quiz-generator/', views.quiz_generator_page, name='quiz_generator'),
    
    # Quiz Management
    path('category/<slug:slug>/', views.category_quizzes, name='category_quizzes'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/take/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    path('results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),
    
    # Quiz Actions
    path('save-response/', views.save_response, name='save_response'),
    path('submit-quiz/<int:attempt_id>/', views.submit_quiz, name='submit_quiz'),
    
    # User Pages
    path('my-results/', views.my_results, name='my_results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('saved-quizzes/', views.saved_quizzes, name='saved_quizzes'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # AI Generation
    path('generate-quiz/', views.generate_ai_quiz, name='generate_quiz'),
    path('generate-custom-quiz/', views.generate_custom_quiz, name='generate_custom_quiz'),
]
