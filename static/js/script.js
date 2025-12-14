document.addEventListener('DOMContentLoaded', () => {

    // 1. Particles.js Configuration
    if (typeof particlesJS !== 'undefined' && document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 80,
                    density: {
                        enable: true,
                        value_area: 800
                    }
                },
                color: {
                    value: ['#862633', '#00205B', '#ffd700']
                },
                shape: {
                    type: 'circle',
                    stroke: {
                        width: 0,
                        color: '#000000'
                    }
                },
                opacity: {
                    value: 0.3,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 1,
                        opacity_min: 0.1,
                        sync: false
                    }
                },
                size: {
                    value: 3,
                    random: true,
                    anim: {
                        enable: true,
                        speed: 2,
                        size_min: 0.1,
                        sync: false
                    }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#ffffff',
                    opacity: 0.2,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 2,
                    direction: 'none',
                    random: true,
                    straight: false,
                    out_mode: 'out',
                    bounce: false,
                    attract: {
                        enable: true,
                        rotateX: 600,
                        rotateY: 1200
                    }
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: {
                        enable: true,
                        mode: 'grab'
                    },
                    onclick: {
                        enable: true,
                        mode: 'push'
                    },
                    resize: true
                },
                modes: {
                    grab: {
                        distance: 140,
                        line_linked: {
                            opacity: 0.5
                        }
                    },
                    push: {
                        particles_nb: 4
                    }
                }
            },
            retina_detect: true
        });
    }

    // 2. Scroll Animation (Intersection Observer)
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

    // 3. Enhanced Typing Effect Logic
    const texts = [
        "Data Researcher",
        "Digital Business Major",
        "AI/ML Enthusiast",
        "Student Leader",
        "Problem Solver"
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
                typeSpeed = 2000;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                typeSpeed = 500;
            }

            setTimeout(type, typeSpeed);
        }

        setTimeout(type, 1500);
    }

    // 4. Stats Counter Animation
    const statNumbers = document.querySelectorAll('.stat-number');
    let hasAnimated = false;

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.getAttribute('data-target'));
                    const duration = 2000;
                    const increment = target / (duration / 16);
                    let current = 0;

                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            stat.textContent = Math.ceil(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            stat.textContent = target;
                        }
                    };

                    setTimeout(() => updateCounter(), 500);
                });
            }
        });
    }, { threshold: 0.5 });

    const heroContent = document.querySelector('.hero-content');
    if (heroContent) {
        statsObserver.observe(heroContent);
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

// 6. Tab Switching Logic for About Me Section
function switchTab(tabId) {
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Remove active class from all tab panels
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });

    // Add active class to clicked button
    event.target.closest('.tab-button').classList.add('active');

    // Show the selected tab panel
    document.getElementById(tabId).classList.add('active');
}