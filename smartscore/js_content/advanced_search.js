document.addEventListener('DOMContentLoaded', function() {
    // Function to add buttons for positions
    function addPositionButtons() {
        const positionButtons = document.getElementById('position-buttons');
        const positions = ['GK', 'DC', 'DL', 'DR', 'DM', 'WBL', 'WBR', 'MC', 'ML', 'MD', 'AMC', 'AML', 'AMR', 'STC'];
        positions.forEach(position => {
            const button = document.createElement('button');
            button.textContent = position;
            button.classList.add('position-btn');
            button.addEventListener('click', function() {
                // Toggle active class on button click
                button.classList.toggle('active');
            });
            positionButtons.appendChild(button);
        });
    }

    // Call the function to add position buttons
    addPositionButtons();

    // Function to handle search button click
    document.getElementById('search-btn').addEventListener('click', function() {
        // Get selected positions
        const selectedPositions = Array.from(document.querySelectorAll('.position-btn.active')).map(button => button.textContent);
        // Get selected qualities (implement as needed)
        
        // Log selected positions and qualities (for testing)
        console.log('Selected Positions:', selectedPositions);
    });
});
