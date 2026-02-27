from django.contrib import admin
from .models import Category, Quiz, Question, Answer, QuizAttempt, UserResponse, UserProfile, SavedQuiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'question_count', 'is_ai_generated', 'created_at']
    list_filter = ['category', 'difficulty', 'is_ai_generated']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'text', 'order']
    list_filter = ['quiz']
    inlines = [AnswerInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'percentage_score', 'started_at', 'completed_at']
    list_filter = ['quiz', 'started_at']
    search_fields = ['user__username', 'quiz__title']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'professional_level', 'global_rank', 'quizzes_completed', 'average_score', 'mobile_number']
    search_fields = ['user__username', 'mobile_number']
    list_editable = ['mobile_number']


admin.site.register(Answer)
admin.site.register(UserResponse)
admin.site.register(SavedQuiz)
