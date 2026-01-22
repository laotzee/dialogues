document.addEventListener('DOMContentLoaded', () => {
    
    const navToggle = document.querySelector('.nav-toggle');
    const primaryNav = document.querySelector('.primary-navigation');

    if (navToggle && primaryNav) {

        navToggle.addEventListener('click', () => {
            const isVisible = primaryNav.getAttribute('data-visible') === 'true';

            if (isVisible) {
                primaryNav.setAttribute('data-visible', 'false');
                navToggle.setAttribute('aria-expanded', 'false');
            } else {
                primaryNav.setAttribute('data-visible', 'true');
                navToggle.setAttribute('aria-expanded', 'true');
            }
        });
    } 
});

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.button-item');
    const container = document.querySelector('.blog-container');

    buttons.forEach(button => {
        button.addEventListener('click', async () => {

            const content_type = button.getAttribute('data-type');

            buttons.forEach(btn => btn.classList.remove('focused'));
            button.classList.add('focused');

            try {
                const response = await fetch(`/?type=${content_type}`, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const html = await response.text();

                // 3. Clear and Inject
                container.innerHTML = html;
            } catch (err) {
                console.error("Error loading posts:", err);
            }
        });
    });
});


