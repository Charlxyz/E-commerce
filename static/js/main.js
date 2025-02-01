// Tool tip
document.addEventListener('DOMContentLoaded', function() {
    // Sélectionner tous les tooltips
    const tooltips = document.querySelectorAll('.tooltip');
    
    // Ajouter la classe "tooltip-with-svg" aux tooltips qui contiennent un SVG
    tooltips.forEach(function(tooltip) {
        const svg = tooltip.querySelector('svg');
        if (svg) {
            tooltip.classList.add('tooltip-with-svg');
        }
    });
});