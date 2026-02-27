// Main JavaScript file for QuizMaster

document.addEventListener('DOMContentLoaded', function() {
    console.log('QuizMaster loaded');
    initializeAnimations();
    initializeProgressRing();
    initializeSearch();
    applyCategoryColors();
});

function initializeAnimations() {
    const cards = document.querySelectorAll('.category-card, .stat-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                entry.target.style.transition = 'all 0.5s ease';
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    cards.forEach(card => observer.observe(card));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function initializeProgressRing() {
    const progressRing = document.querySelector('.progress-ring-progress');
    if (progressRing) {
        const offset = progressRing.getAttribute('data-offset');
        if (offset) {
            progressRing.style.strokeDashoffset = offset;
        }
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.category-card');
            cards.forEach(card => {
                const title = card.querySelector('.category-title')?.textContent.toLowerCase() || '';
                const description = card.querySelector('.category-description')?.textContent.toLowerCase() || '';
                card.style.display = (title.includes(searchTerm) || description.includes(searchTerm)) ? 'block' : 'none';
            });
        });
    }
}

// Apply category colors from data attributes
function applyCategoryColors() {
    const placeholders = document.querySelectorAll('.category-placeholder[data-color]');
    placeholders.forEach(placeholder => {
        const color = placeholder.getAttribute('data-color');
        if (color) {
            placeholder.style.background = color;
        }
    });
}

// Level filter functionality
function filterByLevel(level) {
    const cards = document.querySelectorAll('.category-card');
    const buttons = document.querySelectorAll('.level-filter-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.closest('.level-filter-btn').classList.add('active');
    cards.forEach(card => {
        if (level === 'all') {
            card.style.display = 'block';
        } else {
            card.style.display = card.getAttribute('data-level') === level ? 'block' : 'none';
        }
    });
}

// Generate and start quiz
function generateAndStartQuiz(categoryName, categorySlug) {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = 'Generating...';
    btn.disabled = true;
    
    const topic = categoryName + ' Fundamentals';
    fetch(`/generate-quiz/?topic=${encodeURIComponent(topic)}&category=${encodeURIComponent(categoryName)}`, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.quiz_id) {
            window.location.href = `/quiz/${data.quiz_id}/start/`;
        } else {
            alert('Failed to generate quiz. Please try again.');
            btn.textContent = originalText;
            btn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while generating the quiz.');
        btn.textContent = originalText;
        btn.disabled = false;
    });
}

function generateAIQuiz() {
    const topic = prompt('Enter a topic for the AI-generated quiz:');
    if (topic) {
        window.location.href = `/generate-quiz/?topic=${encodeURIComponent(topic)}`;
    }
}
