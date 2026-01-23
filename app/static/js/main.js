document.addEventListener('DOMContentLoaded', () => {

    const blogContainer = document.querySelector('.blog-container');
    const navToggle = document.querySelector('.nav-toggle');
    const primaryNav = document.querySelector('.primary-navigation');
    const filterButtons = document.querySelectorAll('.button-item');

    async function updateBlogContent(url) {
        if (!blogContainer) return;

        blogContainer.classList.add('loading');

        try {
            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });

            if (!response.ok) throw new Error('Network response was not ok');
            
            const html = await response.text();

            setTimeout(() => {
                blogContainer.innerHTML = html;
                
                requestAnimationFrame(() => {
                    blogContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                });

                blogContainer.classList.remove('loading');
            }, 300);

        } catch (err) {
            console.error("Content update failed:", err);
            blogContainer.classList.remove('loading');
        }
    }

    if (navToggle && primaryNav) {
        navToggle.addEventListener('click', () => {
            const isVisible = primaryNav.getAttribute('data-visible') === 'true';
            
            primaryNav.setAttribute('data-visible', !isVisible);
            navToggle.setAttribute('aria-expanded', !isVisible);
        });
    }

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            if (button.classList.contains('focused')) return;

            filterButtons.forEach(btn => btn.classList.remove('focused'));
            button.classList.add('focused');

            const contentType = button.getAttribute('data-type');
            updateBlogContent(`/?type=${contentType}`);
        });
    });

    document.addEventListener('click', (e) => {
        const pageBtn = e.target.closest('#pagination-nav .page-link');
        
        if (!pageBtn) return;

        const isInactive = pageBtn.parentElement.classList.contains('active') || 
                           pageBtn.parentElement.classList.contains('disabled');

        if (!isInactive) {
            const pageNum = pageBtn.dataset.page;
            updateBlogContent(`/?page=${pageNum}`);
        }
    });
});
