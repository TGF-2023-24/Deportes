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

// Define a function to handle the selection of a squad
function handleSquadSelection() {
    // Get the selected squad ID from the dropdown
    const squadId = document.getElementById('squad-select').value;
    
    // Fetch the squad players from the server
    fetch(`/squad/${squadId}/players/`)
        .then(response => {
            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Failed to fetch squad players');
            }
            // Parse the JSON response
            return response.json();
        })
        .then(data => {
            // Display the squad players on the football field
            displaySquadPlayers(data);
        })
        .catch(error => {
            console.error('Error fetching squad players:', error);
            // Handle errors gracefully (e.g., display error message)
        });
}

// Define a function to display squad players on the football field
function displaySquadPlayers(players) {
    // Get the container element for displaying squad players
    const playerList = document.getElementById('player-list');
    
    // Clear previous player list
    playerList.innerHTML = '';
    
    // Iterate over the players and add them to the list
    players.forEach(playerName => {
        const playerItem = document.createElement('li');
        playerItem.textContent = playerName;
        playerList.appendChild(playerItem);
    });
}

// Add event listener to the squad select dropdown
document.getElementById('squad-select').addEventListener('change', handleSquadSelection);

// Initialize by fetching players for the selected squad
handleSquadSelection();


document.addEventListener('DOMContentLoaded', function() {
    // Function to add dots for each position
    function addDots() {
        const dotContainer = document.getElementById('player-dots');
        dotContainer.innerHTML = ''; // Clear previous dots

        // Get the dimensions of the football field container
        const fieldContainer = document.querySelector('.football-field-container');
        const containerWidth = fieldContainer.offsetWidth;
        const containerHeight = fieldContainer.offsetHeight;

        // Add dots for each position
        Object.keys(positionMapping).forEach(position => {
            const dot = document.createElement('div');
            dot.className = 'player-position-dot';
            dot.position = position;
            // Calculate the position of the dot based on container dimensions
            const left = parseFloat(positionMapping[position].left) / 500 * containerWidth; // Normalize left position
            const top = parseFloat(positionMapping[position].top) / 800 * containerHeight; // Normalize top position
            dot.style.left = left + 'px';
            dot.style.top = top + 'px';
            dotContainer.appendChild(dot);
        });
    }

    // Function to handle dot click
    function handleDotClick(dot) {
        // Toggle dot activation
        dot.classList.toggle('activated');
        
        // Fetch and display players for the selected position
        if (dot.classList.contains('activated')) {
            const position = dot.position;
            const squadId = document.getElementById('squad-select').value;
            fetch(`/squad/${squadId}/players/${position}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch players for position ' + position);
                    }
                    return response.json();
                })
                .then(data => {
                    displayPlayers(data);
                })
                .catch(error => {
                    console.error('Error fetching players:', error);
                });
        } else {
            // Clear player list when dot is deactivated
            clearPlayerList();
        }
    }

    // Function to display players
    function displayPlayers(players) {
        const playerList = document.getElementById('player-list');
        playerList.innerHTML = ''; // Clear previous player list

        console.log("Players:", players); // Log players array to console

        players.forEach(player => {
            console.log("Player:", player); // Log each player object to console
            const playerItem = document.createElement('li');
            playerItem.textContent = player.Name;
            // Add click event listener to select player
            playerItem.addEventListener('click', function() {
                // Get selected position
                const selectedPosition = document.querySelector('.player-position-dot.activated').position;
                // Add player name under selected position
                addPlayerName(selectedPosition, player.Name);
                // Disable dot selection for this player
                document.querySelectorAll('.player-position-dot').forEach(dot => {
                    if (dot.position === selectedPosition) {
                        dot.classList.add('disabled');
                    }
                });
                // Remove click event listener to prevent reselection
                this.removeEventListener('click', arguments.callee);
            });
            playerList.appendChild(playerItem);
        });

        // Add "Select a player" header after displaying players
        playerList.innerHTML += '<li class="player-list-header">Select a player</li>';

        console.log("Player list:", playerList); // Log the player list element to console
    }


    // Function to add player name under selected position
    function addPlayerName(position, playerName) {
        const fieldContainer = document.querySelector('.football-field-container');
        const playerPosition = document.createElement('div');
        playerPosition.className = 'player-position';
        playerPosition.textContent = playerName;
        playerPosition.style.left = positionMapping[position].left;
        playerPosition.style.top = positionMapping[position].top;
        fieldContainer.appendChild(playerPosition);
    }

    // Function to clear player list
    function clearPlayerList() {
        const playerList = document.getElementById('player-list');
        playerList.innerHTML = ''; // Clear player list
    }

    // Add dots when the page is loaded
    addDots();

    // Add event listeners for dot clicks
    document.querySelectorAll('.player-position-dot').forEach(dot => {
        dot.addEventListener('click', function() {
            handleDotClick(dot);
        });
    });

    // Resize dots when the window is resized
    window.addEventListener('resize', function() {
        addDots();
    });
});
