document.addEventListener('DOMContentLoaded', function() {
    const openListIcon = document.getElementById('openListIcon');
    const catSubMenu = document.querySelector('.cat-sub-menu');

    openListIcon.addEventListener('click', function() {
        catSubMenu.classList.toggle('show');
        console.log('clicked');
    });
});
