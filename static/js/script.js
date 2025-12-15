document.addEventListener('DOMContentLoaded', () => {

    // 1. Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            menuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a nav link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                menuToggle.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }

    // 2. Particles.js Configuration
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
        "Digital Business Major",
        "AI Developer",
        "Data Researcher",
        "Tech Strategist",
        "Problem Solver",
        "Value Creator",
        "Passionate Learner"
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
                    // Support suffixes like '2+' by parsing numeric part and keeping suffix
                    const targetAttr = stat.getAttribute('data-target') || '0';
                    const match = targetAttr.toString().match(/^(\d+)(\D*)$/);
                    const target = match ? parseInt(match[1], 10) : 0;
                    const suffix = match ? match[2] : '';
                    const duration = 2000;
                    const increment = target / (duration / 16);
                    let current = 0;

                    const updateCounter = () => {
                        current += increment;
                            if (current < target) {
                            stat.textContent = Math.ceil(current) + suffix;
                            requestAnimationFrame(updateCounter);
                        } else {
                            stat.textContent = target + suffix;
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

// 4. Award Modal Logic with Image Slider
const modal = document.getElementById('awardModal');
let currentSlide = 0;
let currentAwardImages = [];

function openAwardModal(index) {
    const award = awardsData[index];

    // Set title and details
    document.getElementById('modalTitle').textContent = award.name;
    document.getElementById('m-subject').textContent = award.subject;
    document.getElementById('m-award').textContent = award.award;
    document.getElementById('m-date').textContent = award.date;

    // Show/hide organization if provided
    const orgWrapper = document.getElementById('m-org-wrapper');
    if (award.organization && award.organization.trim() !== '') {
        document.getElementById('m-org').textContent = award.organization;
        orgWrapper.style.display = 'block';
    } else {
        orgWrapper.style.display = 'none';
    }

    // Show/hide description if provided
    const descWrapper = document.getElementById('m-desc-wrapper');
    if (award.description && award.description.trim() !== '') {
        document.getElementById('m-description').textContent = award.description;
        descWrapper.style.display = 'block';
    } else {
        descWrapper.style.display = 'none';
    }

    // Setup image slider
    currentAwardImages = award.images || [];
    currentSlide = 0;
    setupImageSlider();

    // Show modal
    modal.style.display = 'flex';
}

function setupImageSlider() {
    const sliderContainer = document.getElementById('imageSlider');
    const sliderImages = document.getElementById('sliderImages');
    const sliderDots = document.getElementById('sliderDots');

    // Clear existing content
    sliderImages.innerHTML = '';
    sliderDots.innerHTML = '';

    if (currentAwardImages.length === 0) {
        // Show default icon if no images
        sliderImages.innerHTML = `
            <div class="slider-image active">
                <div class="default-award-icon">
                    <i class="fas fa-award"></i>
                    <p>증빙 자료 없음</p>
                </div>
            </div>
        `;
        sliderContainer.style.display = 'block';
        document.querySelectorAll('.slider-btn').forEach(btn => btn.style.display = 'none');
    } else {
        // Show images
        currentAwardImages.forEach((img, index) => {
            const imgDiv = document.createElement('div');
            imgDiv.className = 'slider-image' + (index === 0 ? ' active' : '');
            imgDiv.innerHTML = `<img src="${img}" alt="Award Certificate ${index + 1}">`;
            sliderImages.appendChild(imgDiv);

            // Create dot
            const dot = document.createElement('span');
            dot.className = 'slider-dot' + (index === 0 ? ' active' : '');
            dot.onclick = () => goToSlide(index);
            sliderDots.appendChild(dot);
        });

        sliderContainer.style.display = 'block';

        // Show/hide navigation buttons
        const showButtons = currentAwardImages.length > 1;
        document.querySelectorAll('.slider-btn').forEach(btn => {
            btn.style.display = showButtons ? 'flex' : 'none';
        });
    }
}

function changeSlide(direction) {
    if (currentAwardImages.length <= 1) return;

    currentSlide += direction;

    if (currentSlide >= currentAwardImages.length) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = currentAwardImages.length - 1;
    }

    updateSlider();
}

function goToSlide(index) {
    currentSlide = index;
    updateSlider();
}

function updateSlider() {
    // Update images
    const images = document.querySelectorAll('.slider-image');
    images.forEach((img, index) => {
        img.classList.toggle('active', index === currentSlide);
    });

    // Update dots
    const dots = document.querySelectorAll('.slider-dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });
}

function closeAwardModal() {
    modal.style.display = 'none';
    currentSlide = 0;
    currentAwardImages = [];
}

window.onclick = function(event) {
    if (event.target == modal) {
        closeAwardModal();
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