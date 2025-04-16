document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('menuToggleButton');
    const mobileMenu = document.getElementById('mobileMenu');
  
    toggleButton.addEventListener('click', () => {
      mobileMenu.classList.toggle('show');
    });
  });
  