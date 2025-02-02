console.log("popup.js chargé");

function handlePopup(buttonId, popupId, closeId) {
    const button = document.getElementById(buttonId);
    const popup = document.getElementById(popupId);
    const closeButton = document.getElementById(closeId);

    if (!button) console.error(`Bouton introuvable : #${buttonId}`);
    if (!popup) console.error(`Popup introuvable : #${popupId}`);
    if (!closeButton) console.error(`Bouton de fermeture introuvable : #${closeId}`);

    if (!button || !popup || !closeButton) return;

    button.addEventListener('click', function() {
        console.log("Bouton cliqué !");
        popup.classList.remove('hidden');
        popup.classList.add('visible');
    });

    closeButton.addEventListener('click', function() {
        console.log("Fermeture du popup !");
        popup.classList.remove('visible');
        popup.classList.add('hidden');
    });
}

// Appelle la fonction après le chargement du DOM
document.addEventListener("DOMContentLoaded", function() {
    handlePopup("new-item-open-popup", "new-item-popup", "new-item-close-popup");
});
document.addEventListener("DOMContentLoaded", function() {
    handlePopup("edit-item-open-popup", "edit-item-popup", "edit-item-close-popup");
});
document.addEventListener("DOMContentLoaded", function() {
    handlePopup("delet-item-open-popup", "delet-item-popup", "delet-item-close-popup");
});