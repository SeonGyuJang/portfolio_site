document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Scroll Animation (Intersection Observer)
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });

    // 2. Typing Effect Logic (Hero Section)
    const texts = [
        "Digital Business Major", 
        "Data Researcher", 
        "Student Leader", 
        "Challenge Seeker"
    ];
    
    const typingSpan = document.querySelector('.typing-text');
    
    if (typingSpan) {
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let typeSpeed = 100;

        function type() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                typingSpan.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
                typeSpeed = 50; 
            } else {
                typingSpan.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
                typeSpeed = 100;
            }

            if (!isDeleting && charIndex === currentText.length) {
                isDeleting = true;
                typeSpeed = 2000; // 문장 완성 후 대기 시간
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typeSpeed = 500;
            }

            setTimeout(type, typeSpeed);
        }

        setTimeout(type, 1000); // 1초 후 시작
    }
});

// 3. Gallery Filter Logic
function filterGallery(category, btn) {
    document.querySelectorAll('.gallery-filter').forEach(el => el.classList.remove('active'));
    btn.classList.add('active');

    const cards = document.querySelectorAll('.gallery-card');
    cards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
            setTimeout(() => card.style.opacity = 1, 50); 
        } else {
            card.style.display = 'none';
            card.style.opacity = 0;
        }
    });
}

// 4. Modal Logic
const modal = document.getElementById('awardModal');
const mTitle = document.getElementById('modalTitle');
const mDesc = document.getElementById('modalDesc');

function openModal(title, content) {
    if (mTitle) mTitle.textContent = title;
    // content 인자를 사용하여 내용 변경 로직 추가 가능
    if (modal) modal.style.display = 'flex';
}

function closeModal() {
    if (modal) modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// 5. Skills Toggle Logic
function toggleSkill(card) {
    const isActive = card.classList.contains('active');
    
    // 다른 열린 카드들 닫기
    document.querySelectorAll('.skill-card').forEach(c => {
        c.classList.remove('active');
        c.querySelector('.progress-fill').style.width = '0%';
    });

    if (!isActive) {
        card.classList.add('active');
        const level = card.getAttribute('data-level');
        const fill = card.querySelector('.progress-fill');
        const text = card.querySelector('.progress-text');
        
        setTimeout(() => {
            fill.style.width = level + '%';
        }, 100);
        
        let count = 0;
        const interval = setInterval(() => {
            if (count >= level) clearInterval(interval);
            else {
                count++;
                text.textContent = count + '%';
            }
        }, 10);
    }
}