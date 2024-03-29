document.addEventListener('DOMContentLoaded', function() {
    // Get the anchor and list elements
    const anchorTools = document.getElementById('tools');
    const list1 = document.getElementById('list1');
    let list1Visible = false;

    const anchorLibrary = document.getElementById('library');
    const list2 = document.getElementById('list2');
    let list2Visible = false;

    // Add click event listener to the anchor elements
    anchorTools.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        // Toggle the visibility of the list
        list1Visible = !list1Visible;
        if (list1Visible) {
            list1.classList.add('show');
        } else {
            list1.classList.remove('show');
        }
    });

    anchorLibrary.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        // Toggle the visibility of the list
        list2Visible = !list2Visible;
        if (list2Visible) {
            list2.classList.add('show');
        } else {
            list2.classList.remove('show');
        }
    });
});
