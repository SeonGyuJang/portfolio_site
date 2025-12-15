document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('activityModal');
    const iframe = document.getElementById('activityIframe');
    const triggers = document.querySelectorAll('.activity-trigger');

    // Open Modal
    triggers.forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            const filename = card.dataset.filename;
            
            if (category && filename) {
                // Construct the URL for the iframe
                iframe.src = `/activity/${category}/${filename}`;
                
                // Show modal with animation
                modal.classList.add('show');
                document.body.style.overflow = 'hidden'; // Prevent background scrolling
            }
        });
    });

    // Close Modal Function
    window.closeActivityModal = function() {
        modal.classList.remove('show');
        
        // 전체 화면 상태라면 해제
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }

        setTimeout(() => {
            iframe.src = ''; // Clear source to stop media/scripts
        }, 300); // Wait for transition
        document.body.style.overflow = '';
    }

    // Attach click listeners to any close buttons inside modal (in case of multiple button variants)
    document.querySelectorAll('.activity-close-btn').forEach(btn => {
        btn.addEventListener('click', closeActivityModal);
    });

    // Toggle 'maximized' mode (not native fullscreen): expand modal-content to fill viewport
    window.toggleActivityFullscreen = function() {
        const modalContent = document.querySelector('.activity-modal-content');
        const btn = document.querySelector('.fullscreen-btn');
        const icon = btn ? btn.querySelector('i') : null;
        const text = btn ? btn.querySelector('span') : null;

        const isNowMaximized = modalContent.classList.toggle('maximized');

        if (isNowMaximized) {
            if (icon) {
                icon.classList.remove('fa-expand');
                icon.classList.add('fa-compress');
            }
            if (text) text.textContent = '기본화면';
        } else {
            if (icon) {
                icon.classList.remove('fa-compress');
                icon.classList.add('fa-expand');
            }
            if (text) text.textContent = '전체보기';
        }
    }

    // Close on Escape key: if maximized, exit maximized; else close modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            const modalContent = document.querySelector('.activity-modal-content');
            if (modalContent.classList.contains('maximized')) {
                modalContent.classList.remove('maximized');
                const icon = document.querySelector('.fullscreen-btn i');
                const text = document.querySelector('.fullscreen-btn span');
                if(icon) {
                    icon.classList.remove('fa-compress');
                    icon.classList.add('fa-expand');
                }
                if(text) text.textContent = '전체보기';
            } else {
                closeActivityModal();
            }
        }
    });
});