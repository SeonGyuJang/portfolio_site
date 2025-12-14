document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('activityModal');
    const iframe = document.getElementById('activityIframe');
    const closeBtn = document.querySelector('.activity-close-btn');
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
        setTimeout(() => {
            iframe.src = ''; // Clear source to stop media/scripts
        }, 300); // Wait for transition
        document.body.style.overflow = '';
    }
    
    // Close on button click
    if(closeBtn) {
        closeBtn.addEventListener('click', closeActivityModal);
    }

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeActivityModal();
        }
    });
});