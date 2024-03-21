document.addEventListener('DOMContentLoaded', function() {
    // Get the button and list elements
    const button = document.getElementById('openListIcon1');
    const list = document.getElementById('list1');
    let listVisible = false;

    const button2 = document.getElementById('openListIcon2');
    const list2 = document.getElementById('list2');
    let list2Visible = false;

    console.log('Button:', button);
    console.log('List:', list);

    // Add click event listener to the button
    button.addEventListener('click', function() {
        // Toggle the visibility of the list
        listVisible = !listVisible;
        if (listVisible) {
            list.classList.add('show');
        } else {
            list.classList.remove('show');
        }
    });

    button2.addEventListener('click', function() {
        // Toggle the visibility of the list
        list2Visible = !list2Visible;
        if (list2Visible) {
            list2.classList.add('show');
        } else {
            list2.classList.remove('show');
        }
    });
});
