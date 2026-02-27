# 🎓 QuizMaster - Complete Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage Guide](#usage-guide)
5. [Features](#features)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Overview

QuizMaster is a modern, AI-powered quiz application with a sleek UI matching professional educational platforms. Built with Django, it features:

- ✨ AI-generated quizzes using OpenAI GPT
- 🎯 Interactive quiz taking with real-time tracking
- 📊 Comprehensive analytics and results
- 🏆 Global leaderboard system
- 📱 Responsive, modern design

**Tech Stack:** Django 5.0, SQLite, HTML5, CSS3, JavaScript, OpenAI API

---

## Installation

### Quick Start (3 commands)

```bash
# 1. Run setup
./setup.sh

# 2. Activate environment
source venv/bin/activate

# 3. Start server
python manage.py runserver
```

### Manual Installation

#### Step 1: Prerequisites
```bash
# Verify Python (3.8+ required)
python3 --version

# Install pip if needed
sudo apt install python3-pip  # Ubuntu/Debian
brew install python3          # macOS
```

#### Step 2: Setup Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add:
# - SECRET_KEY (optional for dev)
# - OPENAI_API_KEY (get from OpenAI)
nano .env
```

#### Step 5: Setup Database
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter: username, email, password

# Load sample data
python manage.py create_sample_data
```

#### Step 6: Run Server
```bash
python manage.py runserver
```

**Access:** http://localhost:8000/

---

## Configuration

### Environment Variables (.env)

```env
# Security
SECRET_KEY=your-secret-key-here
DEBUG=True

# OpenAI (for AI quiz generation)
OPENAI_API_KEY=sk-your-api-key-here
```

### Getting OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy key to .env file

**Note:** AI generation works without API key (uses fallback sample quizzes)

### Database Configuration

**Development (default):**
```python
# SQLite - automatic, no setup needed
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quizmaster_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Usage Guide

### For Students/Users

#### 1. Create Account
```
1. Visit http://localhost:8000/
2. Click "Sign up"
3. Fill in:
   - Username
   - Email
   - First Name
   - Password (twice)
4. Submit → Auto-login to dashboard
```

#### 2. Browse Quizzes
```
Dashboard shows:
- Available categories (Programming, Science, Math, etc.)
- Your statistics (quizzes completed, average score, rank)
- Search bar for finding quizzes
```

#### 3. Take a Quiz
```
1. Click category card
2. Choose a quiz
3. Click "Start Quiz"
4. Answer questions:
   - Click answer to select
   - Use Next/Previous buttons
   - Click question numbers to jump
   - Timer shows remaining time
5. Click "Submit Quiz" when done
```

#### 4. View Results
```
Results page shows:
- Overall score percentage
- Correct/wrong breakdown
- Time taken
- Efficiency rating
- Question-by-question review
- Explanations for each answer
```

#### 5. Track Progress
```
- "My Results" - View quiz history
- "Leaderboard" - See global rankings
- "Saved Quizzes" - Access bookmarked quizzes
```

### For Administrators

#### Access Admin Panel
```
URL: http://localhost:8000/admin/
Login: Your superuser credentials
```

#### Create Quiz Category
```
1. Admin → Categories → Add Category
2. Fill in:
   - Name (e.g., "History")
   - Slug (e.g., "history")
   - Description
   - Color (hex code)
   - Image (optional)
3. Save
```

#### Create Custom Quiz
```
1. Admin → Quizzes → Add Quiz
2. Fill in:
   - Title
   - Category
   - Description
   - Difficulty (Easy/Medium/Hard)
   - Duration (minutes)
3. Add Questions:
   - Click "Add another Question"
   - Enter question text
   - Add explanation
   - Set order number
4. For each question, add 4 answers:
   - Answer text
   - Check "Is correct" for right answer
   - Set order
5. Save
```

#### Generate AI Quiz
```
Two methods:

Method 1 - Via Interface:
1. Login to site (not admin)
2. Dashboard → "Generate AI Quiz" button
3. Enter topic (e.g., "Machine Learning")
4. Select category
5. System generates 10-question quiz

Method 2 - Direct URL:
/generate-quiz/?topic=Python&category=Programming
```

#### Manage Users
```
Admin → Users:
- View all registered users
- Edit user details
- View user profiles and stats
- Manage permissions
```

#### View Analytics
```
Admin → Quiz Attempts:
- See all quiz submissions
- Filter by user/quiz
- View scores and times
- Export data
```

---

## Features

### User Features

#### Dashboard
- **Category Cards**: Visual cards for each quiz category
- **Statistics**: Personal stats (quizzes completed, avg score, rank)
- **Search**: Find quizzes by name or description
- **Navigation**: Sidebar with easy access to all sections

#### Quiz Taking
- **Real-time Timer**: Countdown timer with visual feedback
- **Progress Tracking**: Progress bar showing completion percentage
- **Question Navigation**: Click numbers to jump to any question
- **Auto-save**: Responses saved automatically
- **Review Mode**: Check all answers before submitting

#### Results & Analytics
- **Score Display**: Large, clear percentage score
- **Breakdown**: Correct vs. wrong questions
- **Time Analysis**: Time taken vs. expected time
- **Efficiency**: Performance rating
- **Explanations**: Detailed explanation for each answer
- **Review**: See your answer vs. correct answer

#### Leaderboard
- **Global Rankings**: See top performers
- **User Stats**: Quizzes completed, average score
- **Your Position**: Highlighted in the list
- **Tier System**: Elite, Pro, Beginner tiers

### Admin Features

#### Content Management
- Create/edit/delete categories
- Create/edit/delete quizzes
- Manage questions and answers
- Upload category images
- Set quiz difficulty and duration

#### User Management
- View all users
- Edit user profiles
- Manage professional levels
- Update rankings

#### Analytics
- View all quiz attempts
- Filter and sort submissions
- Track user progress
- Export data for analysis

### AI Features

#### Quiz Generation
- **Topic-based**: Generate quizzes on any topic
- **Smart Questions**: Contextually relevant questions
- **Explanations**: AI-generated answer explanations
- **Fallback**: Sample quizzes if AI unavailable

#### Quality Control
- Questions validated for clarity
- 4 answer choices per question
- One correct answer marked
- Explanations provided

---

## Troubleshooting

### Common Issues

#### 1. Server Won't Start
```bash
# Error: Port already in use
python manage.py runserver 8080

# Error: Module not found
pip install -r requirements.txt

# Error: Database error
python manage.py migrate
```

#### 2. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings
# Verify STATIC_URL and STATICFILES_DIRS in settings.py
```

#### 3. AI Generation Fails
```bash
# Check .env file
cat .env | grep OPENAI

# Verify API key is valid
# Check OpenAI dashboard for credits

# System will use fallback sample quizzes
```

#### 4. Login Issues
```bash
# Reset password via admin panel
python manage.py changepassword username

# Create new superuser
python manage.py createsuperuser
```

#### 5. Database Errors
```bash
# Reset database (WARNING: deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py create_sample_data
```

### Verification

```bash
# Run verification script
./verify.sh

# Manual checks
python manage.py check
python manage.py check --deploy
```

---

## FAQ

**Q: Do I need an OpenAI API key?**
A: No, it's optional. The system will use sample quizzes if no API key is provided.

**Q: Can I use PostgreSQL instead of SQLite?**
A: Yes, update the DATABASES setting in settings.py and install psycopg2.

**Q: How do I add more categories?**
A: Use the admin panel at /admin/ or create them via Django shell.

**Q: Can users create their own quizzes?**
A: Currently, only admins can create quizzes. User creation can be added by extending the views.

**Q: How is scoring calculated?**
A: Score = (Correct Answers / Total Questions) × 100

**Q: What's the efficiency rating?**
A: Compares time taken vs. expected time. 100% if within expected time.

**Q: Can I export quiz data?**
A: Yes, via the admin panel. Click on Quiz Attempts and use the export function.

**Q: Is there a mobile app?**
A: Not yet, but the web interface is fully responsive.

**Q: How do I customize the design?**
A: Edit static/css/style.css. Main colors are in CSS variables at the top.

**Q: Can I add more question types?**
A: Currently supports multiple choice. Other types require model and template changes.

---

## Support & Resources

- **Documentation**: README.md, QUICKSTART.md, PROJECT_STRUCTURE.md
- **Django Docs**: https://docs.djangoproject.com/
- **OpenAI API**: https://platform.openai.com/docs/
- **Verification**: Run `./verify.sh` to check setup

---

## Quick Commands Reference

```bash
# Setup
./setup.sh                          # Full automated setup
./verify.sh                         # Verify installation

# Server
python manage.py runserver          # Start dev server
python manage.py runserver 8080     # Start on port 8080

# Database
python manage.py makemigrations     # Create migrations
python manage.py migrate            # Apply migrations
python manage.py flush              # Clear database

# Users
python manage.py createsuperuser    # Create admin
python manage.py changepassword user # Change password

# Data
python manage.py create_sample_data # Load sample data
python manage.py shell              # Django shell

# Utilities
python manage.py check              # Check project
python manage.py collectstatic      # Collect static files
```

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-02  
**Author:** QuizMaster Team  
**License:** MIT
