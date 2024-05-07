document.addEventListener('DOMContentLoaded', function() {
    const sidebarLinks = document.querySelectorAll('.sidebar-body-menu a');
    const toolsLink = document.getElementById('tools');
    const libraryLink = document.getElementById('library');

    // Function to check if a given URL matches the current page URL
    const urlMatchesCurrentPage = (url) => {
        return window.location.pathname === url;
    };

    sidebarLinks.forEach(link => {
        // Check if the link's href matches the current URL
        if (urlMatchesCurrentPage(link.getAttribute('href'))) {
            link.classList.add('active');
        }

        link.addEventListener('click', function(event) {
            // Remove "active" class from all links
            sidebarLinks.forEach(link => {
                link.classList.remove('active');
            });

            // Add "active" class to the clicked link
            this.classList.add('active');

        });
    });
});
