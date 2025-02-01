// Afficher le message flash pendant 3 secondes
window.onload = function() {
    const flashMessage = document.querySelector('.flash-message');
    if (flashMessage) {
        flashMessage.style.display = 'block';
        setTimeout(() => {
            flashMessage.style.display = 'none';
        }, 3000);  // Disparaît après 3 secondes
    }
};