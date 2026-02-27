# QuizMaster - AI-Powered Quiz Platform

A modern, full-featured quiz application built with Django, featuring AI-generated quizzes, real-time progress tracking, and comprehensive analytics.

## Features

### 🎯 Core Features
- **AI-Generated Quizzes** - Automatically create quizzes using OpenAI GPT
- **Multiple Categories** - Programming, Science, Mathematics, Business, Humanities, and more
- **Real-time Quiz Taking** - Interactive quiz interface with progress tracking
- **Comprehensive Results** - Detailed analytics with explanations
- **User Profiles** - Track progress, scores, and rankings
- **Leaderboard System** - Global rankings based on performance
- **Saved Quizzes** - Bookmark quizzes for later

### 🎨 Design Features
- Modern, clean UI matching the provided screenshots
- Responsive design for all devices
- Smooth animations and transitions
- Color-coded feedback (correct/incorrect answers)
- Progress bars and timers
- Visual statistics and charts

## Tech Stack

- **Backend**: Django 5.0.1
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)
- **AI**: OpenAI GPT-3.5-turbo
- **Authentication**: Django Auth System

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

1. **Clone and navigate to the project**
```bash
cd /home/bibek/Desktop/professional/Quiz
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file**
```bash
cp .env.example .env
```

5. **Edit .env file and add your credentials**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
OPENAI_API_KEY=your-openai-api-key-here
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```

8. **Create sample data (optional)**
```bash
python manage.py shell
```

Then in the Python shell:
```python
from quiz.models import Category

Category.objects.create(
    name='Programming',
    slug='programming',
    description='Test your coding logic in Python and JS. From syntax to algorithms.',
    color='#4F46E5'
)

Category.objects.create(
    name='Science',
    slug='science',
    description='Biology, Physics, and Chemistry essentials for professionals.',
    color='#10B981'
)

Category.objects.create(
    name='Mathematics',
    slug='mathematics',
    description='Algebra and Calculus challenges. Advanced problem solving.',
    color='#F59E0B'
)

exit()
```

9. **Run the development server**
```bash
python manage.py runserver
```

10. **Access the application**
- Main site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

## Usage

### Creating Your First Account
1. Navigate to http://localhost:8000/
2. Click "Sign up" to create a new account
3. Fill in your details and submit
4. You'll be automatically logged in

### Taking a Quiz
1. Browse categories on the dashboard
2. Click "Start Quiz" on any category
3. Answer questions one by one
4. Use navigation buttons or click question numbers to jump around
5. Click "Submit Quiz" when finished
6. View your detailed results with explanations

### Generating AI Quizzes
1. On the dashboard, click "Generate AI Quiz" button (if no quizzes exist)
2. Enter a topic (e.g., "Python Functions", "World War II", "Linear Algebra")
3. The system will generate a 10-question quiz automatically
4. Start the quiz immediately

### Admin Panel Features
- Access: http://localhost:8000/admin/
- Manage categories, quizzes, questions, and answers
- View user attempts and responses
- Monitor user profiles and rankings

## Project Structure

```
Quiz/
├── quizmaster/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── quiz/                    # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   ├── signals.py          # Signal handlers
│   └── ai_generator.py     # AI quiz generation
├── templates/              # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── quiz_take.html
│   ├── results.html
│   ├── login.html
│   └── register.html
├── static/                 # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── media/                  # Uploaded files
├── manage.py
└── requirements.txt
```

## Database Models

### Core Models
- **Category** - Quiz categories (Programming, Science, etc.)
- **Quiz** - Individual quizzes with metadata
- **Question** - Quiz questions with explanations
- **Answer** - Multiple choice answers (one correct per question)
- **QuizAttempt** - User's quiz attempts and scores
- **UserResponse** - Individual question responses
- **UserProfile** - Extended user information and stats
- **SavedQuiz** - User's bookmarked quizzes

## API Endpoints

### Authentication
- `GET/POST /login/` - User login
- `GET/POST /register/` - User registration
- `GET /logout/` - User logout

### Main Pages
- `GET /` - Dashboard
- `GET /category/<slug>/` - Category quizzes
- `GET /my-results/` - User's quiz history
- `GET /leaderboard/` - Global rankings
- `GET /saved-quizzes/` - Saved quizzes

### Quiz Actions
- `GET /quiz/<id>/start/` - Start new quiz attempt
- `GET /quiz/take/<attempt_id>/` - Take quiz
- `POST /save-response/` - Save answer
- `POST /submit-quiz/<attempt_id>/` - Submit completed quiz
- `GET /results/<attempt_id>/` - View results

### AI Generation
- `GET /generate-quiz/?topic=<topic>&category=<category>` - Generate new quiz

## Customization

### Adding New Categories
1. Go to admin panel
2. Click "Categories" → "Add Category"
3. Fill in name, slug, description, and color
4. Upload an image (optional)

### Customizing Colors
Edit `static/css/style.css` and modify the CSS variables in `:root`:
```css
:root {
    --primary-color: #4F46E5;
    --secondary-color: #EC4899;
    --success-color: #10B981;
    /* ... etc */
}
```

### Changing AI Model
Edit `quiz/ai_generator.py` and modify the OpenAI model:
```python
response = openai.chat.completions.create(
    model="gpt-4",  # Change from gpt-3.5-turbo
    ...
)
```

## Deployment

### Production Settings
1. Set `DEBUG=False` in .env
2. Add your domain to `ALLOWED_HOSTS` in settings.py
3. Configure proper database (PostgreSQL recommended)
4. Set up static file serving (Nginx/Apache)
5. Use Gunicorn or uWSGI for WSGI server
6. Configure SSL certificate

### Example Production Setup
```bash
# Install Gunicorn
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn quizmaster.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### AI Quiz Generation Not Working
- Verify OPENAI_API_KEY is set in .env
- Check your OpenAI account has credits
- System will fallback to sample quizzes if API fails

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

### Database Errors
```bash
python manage.py flush  # Clear database (WARNING: deletes all data)
python manage.py migrate --run-syncdb
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
MIT License - feel free to use this project for learning or commercial purposes.

## Support
For issues or questions:
- Check the documentation above
- Review Django documentation: https://docs.djangoproject.com/
- Check OpenAI API docs: https://platform.openai.com/docs/

## Credits
- Design inspired by modern educational platforms
- Built with Django and OpenAI
- Icons: Unicode emoji characters
# Quiz-generator
