document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('darkmode-toggle');
    const background = document.querySelector('.background');
    
    // Check if dark mode is stored in localStorage
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        background.classList.add('dark-mode');
        toggle.checked = true;
    }

    // Toggle button event listener
    toggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode');
        background.classList.toggle('dark-mode');

        // Update localStorage based on the current mode
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });
});
