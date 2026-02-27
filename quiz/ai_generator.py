import json
import google.generativeai as genai
from django.conf import settings
from .models import Quiz, Question, Answer, Category


class AIQuizGenerator:
    def __init__(self):
        # Configure Gemini API (Free tier)
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise Exception("GEMINI_API_KEY not configured in .env file")
        
        genai.configure(api_key=api_key)
        
        # Discover available models
        print("Discovering available Gemini models...")
        available_models = []
        try:
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
                    print(f"✓ Available: {model.name}")
        except Exception as e:
            print(f"Error listing models: {e}")
        
        # Try to use the first available model
        if not available_models:
            raise Exception("No models available with generateContent support")
        
        model_name = available_models[0]
        print(f"Using model: {model_name}")
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 16384,  # Increased token limit
            }
        )

    def generate_quiz(self, category_name, topic, num_questions=10, difficulty='medium'):
        """Generate a complete quiz using Google Gemini API"""
        
        # Subject-specific context based on category
        subject_context = self._get_subject_context(category_name)
        
        prompt = f"""You are an expert educational quiz creator specializing in {category_name}.

Generate a comprehensive quiz about "{topic}" with the following specifications:

Subject: {category_name}
Topic: {topic}
Number of Questions: {num_questions}
Difficulty Level: {difficulty}

{subject_context}

Requirements:
- Create exactly {num_questions} multiple choice questions
- Each question must have exactly 4 answer options (A, B, C, D)
- Only ONE answer should be correct
- Questions should be clear, concise, and educational
- Include a detailed explanation for why the correct answer is right
- Questions should progress from basic to advanced concepts
- Use real-world examples where applicable

Return ONLY valid JSON in this exact format (no markdown, no extra text):
{{
    "title": "Specific quiz title related to {topic}",
    "description": "Brief 1-2 sentence description of what this quiz covers",
    "questions": [
        {{
            "text": "Clear question text here?",
            "explanation": "Detailed explanation of why the correct answer is correct and why others are wrong",
            "answers": [
                {{"text": "First option", "is_correct": false}},
                {{"text": "Second option", "is_correct": true}},
                {{"text": "Third option", "is_correct": false}},
                {{"text": "Fourth option", "is_correct": false}}
            ]
        }}
    ]
}}

Generate the quiz now:"""

        try:
            # Generate content with Gemini Free API
            response = self.model.generate_content(
                prompt,
                safety_settings={
                    'HARASSMENT': 'block_none',
                    'HATE': 'block_none',
                    'SEXUAL': 'block_none',
                    'DANGEROUS': 'block_none'
                }
            )
            
            # Check if response was blocked
            if not response.text:
                print("Response was blocked or empty")
                return None
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            quiz_data = json.loads(response_text)
            
            # Validate quiz data
            if not self._validate_quiz_data(quiz_data, num_questions):
                print("Invalid quiz data structure, using fallback")
                return None
            
            return self._create_quiz_from_data(quiz_data, category_name, difficulty)

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text}")
            # Try to handle incomplete JSON by checking the response
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    print(f"Finish reason: {candidate.finish_reason}")
                    if str(candidate.finish_reason) == 'MAX_TOKENS':
                        print("Response truncated due to token limit. Try reducing number of questions.")
                        raise Exception("Quiz too large - please reduce the number of questions and try again")
            return None
        except Exception as e:
            print(f"Error generating quiz with Gemini: {e}")
            raise  # Re-raise to pass error message to user
    
    def _get_subject_context(self, category_name):
        """Get subject-specific context for better quiz generation"""
        contexts = {
            'Programming': """
Focus on:
- Programming concepts, syntax, and best practices
- Data structures and algorithms
- Code efficiency and optimization
- Common programming patterns
- Real-world coding scenarios
            """,
            'Science': """
Focus on:
- Scientific principles and theories
- Experimental methods and analysis
- Natural phenomena and explanations
- Scientific applications in daily life
- Recent discoveries and advancements
            """,
            'Mathematics': """
Focus on:
- Mathematical concepts and formulas
- Problem-solving techniques
- Practical applications of math
- Step-by-step reasoning
- Real-world mathematical scenarios
            """,
            'Business': """
Focus on:
- Business strategies and management
- Market analysis and trends
- Financial concepts and calculations
- Leadership and organizational behavior
- Case studies and practical scenarios
            """,
            'Humanities': """
Focus on:
- Historical events and contexts
- Cultural understanding and analysis
- Literary techniques and interpretations
- Philosophical concepts
- Social and political movements
            """
        }
        return contexts.get(category_name, "Focus on educational and thought-provoking questions relevant to the subject.")
    
    def _validate_quiz_data(self, quiz_data, expected_questions):
        """Validate the structure of quiz data"""
        if not isinstance(quiz_data, dict):
            return False
        if 'title' not in quiz_data or 'questions' not in quiz_data:
            return False
        if not isinstance(quiz_data['questions'], list):
            return False
        if len(quiz_data['questions']) != expected_questions:
            return False
        
        for question in quiz_data['questions']:
            if not isinstance(question, dict):
                return False
            if 'text' not in question or 'answers' not in question:
                return False
            if not isinstance(question['answers'], list):
                return False
            if len(question['answers']) != 4:
                return False
            
            # Check that exactly one answer is correct
            correct_count = sum(1 for ans in question['answers'] if ans.get('is_correct', False))
            if correct_count != 1:
                return False
        
        return True

    def _create_quiz_from_data(self, quiz_data, category_name, difficulty):
        """Create quiz objects in database from generated data"""
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category = Category.objects.create(
                name=category_name,
                slug=category_name.lower().replace(' ', '-'),
                description=f"{category_name} quizzes"
            )

        quiz = Quiz.objects.create(
            title=quiz_data['title'],
            category=category,
            description=quiz_data['description'],
            difficulty=difficulty,
            is_ai_generated=True,
            duration_minutes=len(quiz_data['questions']) * 1.5
        )
        
        for idx, question_data in enumerate(quiz_data['questions'], 1):
            question = Question.objects.create(
                quiz=quiz,
                text=question_data['text'],
                explanation=question_data.get('explanation', ''),
                order=idx
            )

            for ans_idx, answer_data in enumerate(question_data['answers'], 1):
                Answer.objects.create(
                    question=question,
                    text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    order=ans_idx
                )

        return quiz


# Fallback function to generate sample quiz without API
def generate_sample_quiz(category, topic, num_questions=10):
    """Generate a sample quiz without using AI API"""
    
    sample_data = {
        "title": f"{topic} Fundamentals",
        "description": f"Test your knowledge of {topic} in {category}",
        "questions": []
    }
    
    # Sample questions based on category
    if category.lower() == "programming":
        sample_questions = [
            {
                "text": "What is the time complexity of binary search?",
                "explanation": "Binary search divides the search space in half each time, resulting in O(log n) complexity.",
                "answers": [
                    {"text": "O(n)", "is_correct": False},
                    {"text": "O(log n)", "is_correct": True},
                    {"text": "O(n²)", "is_correct": False},
                    {"text": "O(1)", "is_correct": False}
                ]
            },
            {
                "text": "Which data structure uses LIFO (Last-In-First-Out) logic?",
                "explanation": "Stack follows LIFO principle where the last element added is the first one to be removed.",
                "answers": [
                    {"text": "Queue", "is_correct": False},
                    {"text": "Stack", "is_correct": True},
                    {"text": "Linked List", "is_correct": False},
                    {"text": "Binary Tree", "is_correct": False}
                ]
            }
        ]
    elif category.lower() == "science":
        sample_questions = [
            {
                "text": "What is the chemical formula for water?",
                "explanation": "Water consists of two hydrogen atoms and one oxygen atom.",
                "answers": [
                    {"text": "H2O", "is_correct": True},
                    {"text": "CO2", "is_correct": False},
                    {"text": "O2", "is_correct": False},
                    {"text": "H2O2", "is_correct": False}
                ]
            }
        ]
    else:
        sample_questions = [
            {
                "text": f"Sample question about {topic}?",
                "explanation": "This is a sample explanation.",
                "answers": [
                    {"text": "Option A", "is_correct": False},
                    {"text": "Option B", "is_correct": True},
                    {"text": "Option C", "is_correct": False},
                    {"text": "Option D", "is_correct": False}
                ]
            }
        ]
    
    # Repeat to reach desired number of questions
    while len(sample_data['questions']) < num_questions:
        sample_data['questions'].extend(sample_questions[:num_questions - len(sample_data['questions'])])
    
    generator = AIQuizGenerator()
    return generator._create_quiz_from_data(sample_data, category, 'medium')
