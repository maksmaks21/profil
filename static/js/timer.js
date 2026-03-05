// Глобальний об'єкт для керування таймером вікторини
const QuizTimer = {
    container: document.getElementById('quiz-timer-container'),
    progressCircle: document.querySelector('.timer-progress'),
    timerText: document.querySelector('.timer-text'),
    totalSeconds: 0,
    timeLeft: 0,
    timerInterval: null,
    quizId: null,
    
    // Ініціалізація таймера
    init: function(quizId, totalSeconds) {
        this.quizId = quizId;
        this.totalSeconds = totalSeconds;
        this.timeLeft = totalSeconds;
        this.show();
        this.updateDisplay();
        
        // Запускаємо таймер
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
        }
        
        this.timerInterval = setInterval(() => this.tick(), 1000);
    },
    
    // Кожна секунда
    tick: function() {
        if (this.timeLeft <= 0) {
            this.stop();
            return;
        }
        
        this.timeLeft--;
        this.updateDisplay();
    },
    
    // Оновлення відображення
    updateDisplay: function() {
        // Форматуємо час
        const hours = Math.floor(this.timeLeft / 3600);
        const minutes = Math.floor((this.timeLeft % 3600) / 60);
        const seconds = this.timeLeft % 60;
        
        let timeString;
        if (hours > 0) {
            timeString = `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        } else {
            timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        
        // Оновлюємо текст
        this.timerText.textContent = timeString;
        
        // Оновлюємо прогрес
        const progress = this.timeLeft / this.totalSeconds;
        const dashOffset = 283 * (1 - progress);
        this.progressCircle.style.strokeDashoffset = dashOffset;
        
        // Змінюємо колір в залежності від часу
        this.progressCircle.classList.remove('warning', 'danger');
        if (progress < 0.3) {
            this.progressCircle.classList.add('danger');
        } else if (progress < 0.6) {
            this.progressCircle.classList.add('warning');
        }
    },
    
    // Показати таймер
    show: function() {
        this.container.style.display = 'block';
    },
    
    // Сховати таймер
    hide: function() {
        this.container.style.display = 'none';
    },
    
    // Зупинити таймер
    stop: function() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    },
    
    // Скинути таймер
    reset: function() {
        this.stop();
        this.hide();
        this.timeLeft = 0;
        this.totalSeconds = 0;
    }
};

// Експортуємо для використання в інших скриптах
window.QuizTimer = QuizTimer;