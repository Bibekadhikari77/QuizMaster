# QuizMaster - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env and add your keys

# 4. Setup database
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Create sample data
python manage.py create_sample_data

# 7. Run server
python manage.py runserver
```

## 📋 What You Need

1. **Python 3.8+** - Check: `python3 --version`
2. **OpenAI API Key** (optional) - Get from: https://platform.openai.com/
   - Sign up for OpenAI account
   - Go to API Keys section
   - Create new secret key
   - Add to .env file

## 🎯 First Steps After Setup

1. **Access the Application**
   - Open browser: http://localhost:8000/
   - You'll see the login page

2. **Create Your Account**
   - Click "Sign up"
   - Fill in: username, email, first name, password
   - Submit and you're logged in!

3. **Explore the Dashboard**
   - View available quiz categories
   - Check your stats (will be 0 initially)
   - Browse categories

4. **Take Your First Quiz**
   - Click on any category card
   - Click "Start Quiz"
   - Answer questions
   - Submit and view results!

5. **Generate AI Quiz** (if you have OpenAI key)
   - Click "Generate AI Quiz" button
   - Enter a topic (e.g., "Python Functions")
   - Wait for generation
   - Start the quiz!

## 🔧 Common Issues & Solutions

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 8080
```

### Virtual Environment Not Activating
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### AI Quiz Generation Failing
- Check OPENAI_API_KEY in .env
- Make sure you have credits on OpenAI account
- System will use sample quizzes as fallback

## 📱 Features Overview

### Dashboard
- View quiz categories
- See your statistics
- Search for quizzes
- Access navigation menu

### Quiz Taking
- Real-time timer
- Progress tracking
- Question navigation
- Save responses automatically
- Submit when ready

### Results Page
- Overall score percentage
- Correct/wrong breakdown
- Time taken
- Efficiency rating
- Question-by-question review
- Explanations for answers

### Leaderboard
- Global rankings
- User statistics
- Your position highlighted

## 🎨 Customization Tips

### Add Your Own Quiz Categories
1. Go to admin: http://localhost:8000/admin/
2. Login with superuser account
3. Click "Categories" → "Add Category"
4. Fill in details and save

### Create Custom Quizzes
1. In admin, go to "Quizzes"
2. Click "Add Quiz"
3. Fill in details
4. Add questions inline or separately
5. Each question needs 4 answers (mark one as correct)

### Change Theme Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #4F46E5;  /* Main theme color */
    --secondary-color: #EC4899; /* Accent color */
}
```

## 🎓 Sample Data

The setup creates these categories:
- **Programming** - Coding challenges
- **Science** - Biology, Physics, Chemistry
- **Mathematics** - Algebra, Calculus
- **Business** - Management, Strategy
- **Humanities** - History, Literature

One sample quiz is included in Programming category.

## 📊 Admin Panel Features

Access at: http://localhost:8000/admin/

**What you can do:**
- Manage all categories
- Create/edit/delete quizzes
- View user attempts and scores
- Manage user accounts
- View all responses
- Monitor system activity

## 🔐 Security Notes

### For Development:
- Default SECRET_KEY is OK
- DEBUG=True is fine
- SQLite database works great

### For Production:
- Generate strong SECRET_KEY
- Set DEBUG=False
- Use PostgreSQL database
- Configure ALLOWED_HOSTS
- Set up HTTPS
- Use environment variables

## 💡 Pro Tips

1. **Testing AI Generation**
   - Start with simple topics
   - Be specific in topic names
   - Categories: Programming, Science, Math work best

2. **Better User Experience**
   - Complete profile information
   - Try different difficulty levels
   - Review wrong answers carefully
   - Retake quizzes to improve

3. **Content Creation**
   - Use admin panel for bulk creation
   - Add explanations to questions
   - Organize quizzes by difficulty
   - Use clear, concise question text

## 📞 Need Help?

1. Check README.md for detailed docs
2. Review Django documentation
3. Check console for error messages
4. Verify all migrations ran
5. Ensure virtual environment is active

## 🎉 You're All Set!

Your QuizMaster application is ready to use. Start by:
1. Creating an account (if not done)
2. Taking the sample quiz
3. Creating your own quizzes
4. Generating AI quizzes

Happy quizzing! 🚀
