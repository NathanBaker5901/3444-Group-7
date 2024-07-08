document.addEventListener('DOMContentLoaded', (event) => {
    const toggleButton = document.getElementById('darkmode-toggle');

    // Check the local storage for theme state
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
        toggleButton.checked = true;
    }

    toggleButton.addEventListener('change', function () {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'enabled');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'disabled');
        }
    });
});
