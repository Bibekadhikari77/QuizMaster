from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    subject = models.CharField(max_length=150, blank=True, default='General')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='intermediate')
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    color = models.CharField(max_length=50, default='#4F46E5')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Quiz(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    duration_minutes = models.IntegerField(default=15)
    image = models.ImageField(upload_to='quizzes/', blank=True, null=True)
    is_ai_generated = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    explanation = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Question {self.order}: {self.text[:50]}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.text[:50]} ({'Correct' if self.is_correct else 'Incorrect'})"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_questions}"

    @property
    def percentage_score(self):
        if self.total_questions == 0:
            return 0
        return int((self.score / self.total_questions) * 100)

    @property
    def efficiency(self):
        if self.time_taken_seconds == 0:
            return 100
        expected_time = self.quiz.duration_minutes * 60
        if self.time_taken_seconds <= expected_time:
            return 100
        return max(0, int(100 - ((self.time_taken_seconds - expected_time) / expected_time * 100)))


class UserResponse(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.order}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    professional_level = models.CharField(max_length=50, default='Beginner')
    global_rank = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    quizzes_completed = models.IntegerField(default=0)
    address = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def average_score(self):
        attempts = self.user.quiz_attempts.filter(completed_at__isnull=False)
        if not attempts.exists():
            return 0
        total = sum(attempt.percentage_score for attempt in attempts)
        return int(total / attempts.count())


class SavedQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.quiz.title}"
