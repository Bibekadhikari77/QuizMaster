from django.core.management.base import BaseCommand
from quiz.models import Category, Quiz, Question, Answer


class Command(BaseCommand):
    help = 'Create sample quizzes for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'Programming',
                'slug': 'programming',
                'description': 'Test your coding logic in Python and JS. From syntax to algorithms.',
                'color': '#4F46E5'
            },
            {
                'name': 'Science',
                'slug': 'science',
                'description': 'Biology, Physics, and Chemistry essentials for professionals.',
                'color': '#10B981'
            },
            {
                'name': 'Mathematics',
                'slug': 'mathematics',
                'description': 'Algebra and Calculus challenges. Advanced problem solving.',
                'color': '#F59E0B'
            }
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create a sample Programming quiz
        prog_category = Category.objects.get(slug='programming')
        
        quiz, created = Quiz.objects.get_or_create(
            title='Advanced Data Structures',
            category=prog_category,
            defaults={
                'description': 'Test your knowledge of advanced data structures and algorithms',
                'difficulty': 'hard',
                'duration_minutes': 20,
                'is_ai_generated': False,
                'is_active': True
            }
        )

        if created:
            # Question 1
            q1 = Question.objects.create(
                quiz=quiz,
                text='Which of the following data structures uses LIFO (Last-In-First-Out) logic?',
                explanation='Stack follows LIFO principle where the last element added is the first one to be removed.',
                order=1
            )
            Answer.objects.create(question=q1, text='Queue', is_correct=False, order=1)
            Answer.objects.create(question=q1, text='Stack', is_correct=True, order=2)
            Answer.objects.create(question=q1, text='Linked List', is_correct=False, order=3)
            Answer.objects.create(question=q1, text='Binary Tree', is_correct=False, order=4)

            # Question 2
            q2 = Question.objects.create(
                quiz=quiz,
                text='What is the time complexity of binary search?',
                explanation='Binary search divides the search space in half each time, resulting in O(log n) complexity.',
                order=2
            )
            Answer.objects.create(question=q2, text='O(n)', is_correct=False, order=1)
            Answer.objects.create(question=q2, text='O(log n)', is_correct=True, order=2)
            Answer.objects.create(question=q2, text='O(n²)', is_correct=False, order=3)
            Answer.objects.create(question=q2, text='O(1)', is_correct=False, order=4)

            # Question 3
            q3 = Question.objects.create(
                quiz=quiz,
                text='Which data structure is used for implementing recursion?',
                explanation='Recursion uses the call stack to store function calls.',
                order=3
            )
            Answer.objects.create(question=q3, text='Queue', is_correct=False, order=1)
            Answer.objects.create(question=q3, text='Array', is_correct=False, order=2)
            Answer.objects.create(question=q3, text='Stack', is_correct=True, order=3)
            Answer.objects.create(question=q3, text='Graph', is_correct=False, order=4)

            self.stdout.write(self.style.SUCCESS(f'Created quiz: {quiz.title}'))

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
