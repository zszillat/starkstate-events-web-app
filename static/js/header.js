// Select elements
const menuToggleButton = document.getElementById('menuToggleButton');
const mobileMenu = document.getElementById('mobileMenu');

// Toggle Menu
menuToggleButton.addEventListener('click', () => {
     state = mobileMenu.style.height
     if (state === '0px' || state === '0') {
        mobileMenu.style.height = mobileMenu.scrollHeight + 'px';
     } else {
        mobileMenu.style.height = '0px'
     }
});