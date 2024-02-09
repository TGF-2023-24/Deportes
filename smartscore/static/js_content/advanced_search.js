
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


document.addEventListener('DOMContentLoaded', function() {
    // Function to add dots for each position
    function addDots() {
        const dotContainer = document.getElementById('player-dots');
        dotContainer.innerHTML = ''; // Clear previous dots

        // Add dots for each position
        Object.keys(positionMapping).forEach(position => {
            const dot = document.createElement('div');
            dot.className = 'player-position-dot';
            dot.style.top = positionMapping[position].top;
            dot.style.left = positionMapping[position].left;
            dotContainer.appendChild(dot);
        });
    }

    // Function to handle dot click
    function handleDotClick(dot) {
        dot.classList.toggle('activated'); // Toggle dot activation
    }

    // Add dots when the page is loaded
    addDots();

    // Add event listeners for dot clicks
    document.querySelectorAll('.player-position-dot').forEach(dot => {
        dot.addEventListener('click', function() {
            handleDotClick(dot);
        });
    });

    // Function to handle search button click
    document.getElementById('search-btn').addEventListener('click', function() {
        // Get activated dots
        const activatedDots = document.querySelectorAll('.activated');
        // Get positions corresponding to activated dots
        const selectedPositions = Array.from(activatedDots).map(dot => {
            const position = Object.keys(positionMapping).find(key =>
                positionMapping[key].top === dot.style.top &&
                positionMapping[key].left === dot.style.left
            );
            return position;
        });

        // Send search query to the server (implement as needed)
        console.log('Selected positions:', selectedPositions);
    });
});