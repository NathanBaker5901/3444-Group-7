document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('darkmode-toggle');
    const background = document.querySelector('.background');
    
    // Check if dark mode is stored in localStorage
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        if (background) {
            background.classList.add('dark-mode');
        }
        if (toggle) {
            toggle.checked = true;
        }
    }

    // Toggle button event listener
    if (toggle) {
        toggle.addEventListener('change', () => {
            document.body.classList.toggle('dark-mode');
            if (background) {
                background.classList.toggle('dark-mode');
            }

            // Update localStorage based on the current mode
            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('darkMode', 'enabled');
            } else {
                localStorage.setItem('darkMode', 'disabled');
            }
        });
    }
});
