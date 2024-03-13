document.addEventListener('DOMContentLoaded', function() {
    // Get the button and list elements
    const button = document.getElementById('openListIcon1');
    const list = document.getElementById('list1');

    // Add click event listener to the button
    button.addEventListener('click', function() {
        // Toggle the visibility of the list
        list.classList.toggle('show');
    });
});
