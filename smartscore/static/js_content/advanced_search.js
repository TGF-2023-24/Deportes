document.addEventListener('DOMContentLoaded', function() {
    // Mapping of positions to coordinates
    const positionMapping = {
        'GK': { top: '750px', left: '250px' },
        'DC': { top: '650px', left: '250px' },
        'DL': { top: '650px', left: '75px' },
        'DR': { top: '650px', left: '425px' },
        'DM': { top: '525px', left: '250px' },
        'WBL': { top: '525px', left: '75px' },
        'WBR': { top: '525px', left: '425px' },
        'MC': { top: '400px', left: '250px' },
        'ML': { top: '400px', left: '75px' },
        'MD': { top: '400px', left: '425px' },
        'AMC': { top: '250px', left: '250px' },
        'AML': { top: '250px', left: '75px' },
        'AMR': { top: '250px', left: '425px' },
        'STC': { top: '125px', left: '250px' }
    };


    // Function to add buttons for positions
    function addDots(positions) {
        const field = document.getElementById('football-field');
        const dotContainer = document.getElementById('player-dots');
        dotContainer.innerHTML = ''; // Clear previous dots

        // Add dots for selected positions
        positions.forEach(position => {
            if (positionMapping[position]) {
                const dot = document.createElement('div');
                dot.className = 'player-position-dot';
                dot.style.top = positionMapping[position].top;
                dot.style.left = positionMapping[position].left;
                dotContainer.appendChild(dot);
            }
        });
    }

    document.getElementById('search-btn').addEventListener('click', function() {
        // Get selected positions
        const selectedPositions = Array.from(document.querySelectorAll('input[name="position"]:checked')).map(checkbox => checkbox.value);
        // Get selected qualities (implement as needed)

        // Add dots to the football field
        addDots(selectedPositions);

        // Send search query to the server (implement as needed)
    });


});


