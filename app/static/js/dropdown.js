<script>
    document.addEventListener('DOMContentLoaded', () => {
        
        // 1. Select the necessary elements from the DOM
        const navToggle = document.querySelector('.nav-toggle');
        const primaryNav = document.querySelector('.primary-navigation');

        // IMPORTANT: Check if the elements were successfully found
        if (navToggle && primaryNav) {
            // 2. Add an event listener to the toggle button
            navToggle.addEventListener('click', () => {
                // Check the current state of the menu using the data-visible attribute
                const isVisible = primaryNav.getAttribute('data-visible') === 'true';

                // 3. Toggle the data-visible state and the accessibility attribute
                if (isVisible) {
                    // If the menu is currently visible, hide it
                    primaryNav.setAttribute('data-visible', 'false');
                    navToggle.setAttribute('aria-expanded', 'false');
                } else {
                    // If the menu is currently hidden, show it
                    primaryNav.setAttribute('data-visible', 'true');
                    navToggle.setAttribute('aria-expanded', 'true');
                }
            });
        } 
    });
</script>
