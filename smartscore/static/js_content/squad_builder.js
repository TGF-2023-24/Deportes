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
    'MR': { top: '400px', left: '425px' },
    'AMC': { top: '250px', left: '250px' },
    'AML': { top: '250px', left: '75px' },
    'AMR': { top: '250px', left: '425px' },
    'STC': { top: '125px', left: '250px' }
};

addedPlayerCount = 0;

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
            addedPlayerCount = 0;
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
    let activePlayerButton = null; // Track the active player button
    // Define a Set to keep track of used players
    let blockedPlayers = new Set();
    const playerCounts = {};
    const playerPositionMapping = {};


    // Function to add dots for each position
    function addDots() {
        const dotContainer = document.getElementById('player-dots');
        dotContainer.innerHTML = ''; // Clear previous dots

        // Get the dimensions of the football field container
        const fieldContainer = document.querySelector('.football-field-container-squad-builder');
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
        const activatedDots = document.querySelectorAll('.player-position-dot.activated');
    
        // Deactivate all other dots
        activatedDots.forEach(activatedDot => {
            if (activatedDot !== dot) {
                activatedDot.classList.remove('activated');
            }
        });
        
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
                    document.getElementById('example-btn');

                })
                .catch(error => {
                    console.error('Error fetching players:', error);
                });
        } else {
            // Clear player list when dot is deactivated
            clearPlayerList();
            document.getElementById('example-btn').style.display = 'none';

        }
    }

     // Function to add players dynamically
     function displayPlayers(players) {
        const playerList = document.getElementById('player-list');
        playerList.innerHTML = ''; // Clear previous player list


        players.forEach(player => {
            const playerBut = document.createElement('button');
            playerBut.textContent = player;
            playerBut.classList.add('player-button'); // Add a class for styling

            // Apply style if player is blocked
            if (blockedPlayers.has(player)) {
                playerBut.style.textDecoration = 'line-through';
            }

            // Check if the player is blocked
            playerBut.addEventListener('click', function () {
                handlePlayerButtonClick(playerBut);
            });

            playerList.appendChild(playerBut);
        });

        // Add "Select a player" header after displaying players
        playerList.innerHTML += '<p class="player-list-header">Select a player</p>';
    }
    
    // Function to handle player button click
    function handlePlayerButtonClick(playerBut) {
         // Check if the player is already blocked
        if (playerBut.classList.contains('active')) {
            // Remove active class from the clicked button
            playerBut.classList.remove('active');
            playerBut.classList.remove('clicked');
            activePlayerButton = null;
            return;
        }

        // Remove active class from previously active button
        if (activePlayerButton) {
            activePlayerButton.classList.remove('active');
        }

        // Set the current button as active
        playerBut.classList.add('active');
        activePlayerButton = playerBut;

         // Add the "clicked" class to change color
        playerBut.classList.add('clicked');

        // Block the player
        blockedPlayers.add(playerBut.textContent);
        console.log('Player blocked:', playerBut.textContent);
    }

    // Add event listener to player buttons
    document.querySelectorAll('.player-button').forEach(playerBut => {
        playerBut.addEventListener('click', function () {
            handlePlayerButtonClick(playerBut);
        });
    });
    

    // Function to add player name under selected position
    function addPlayerName(position, playerName) {
        console.log('Adding player name:', playerName, 'at position:', position);
        const fieldContainer = document.querySelector('.football-field-container-squad-builder'); 
        console.log(fieldContainer);
        const containerWidth = fieldContainer.offsetWidth;
        const containerHeight = fieldContainer.offsetHeight;

        // Initialize player count for this position if it doesn't exist
        if (!playerCounts[position]) {
            playerCounts[position] = 0;
        }

        // Get the number of players already present at this position
        const numPlayers = playerCounts[position];
        
        playerPositionMapping[playerName] = position;
        const playerPosition = document.createElement('div');
        playerPosition.className = 'player-position';
        playerPosition.style.position = 'absolute'; // Position absolutely
        playerPosition.textContent = playerName;
        // Calculate the position of the dot based on container dimensions
        const left = parseFloat(positionMapping[position].left) / 500 * containerWidth; // Normalize left position
        const top = parseFloat(positionMapping[position].top) / 800 * containerHeight + numPlayers * 30; // Normalize top position
        playerPosition.style.left = left + 'px';
        playerPosition.style.top = top + 'px';
        fieldContainer.appendChild(playerPosition);
        console.log('Player added:', playerName, 'at position:', left, top);
        // Increment the player count for this position
        playerCounts[position]++;
  
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

    // Function to handle example button click
    document.getElementById('add-player-btn').addEventListener('click', function () {
        console.log(addedPlayerCount, 'players added.');
        if (addedPlayerCount >= 11) {
            alert('Football is played with 11 players.');
            return;
        }
        if (activePlayerButton) {
            const selectedPosition = document.querySelector('.player-position-dot.activated').position;
            const playerName = activePlayerButton.textContent; // Retrieve active player name
            addedPlayerCount++;
            addPlayerName(selectedPosition, playerName);
            // Disable the dot corresponding to the selected position
            document.querySelectorAll('.player-position-dot').forEach(dot => {
                if (dot.position === selectedPosition) {
                    dot.classList.add('disabled');
                }
            });
            // Remove the active class from the active player button
            activePlayerButton.classList.remove('active');
            activePlayerButton = null; // Reset the active player button
        } else {
            console.log('No player selected.');
        }
    });


    // Attach event listener to the parent element and delegate the event to the dynamic elements
    document.getElementById('player-list').addEventListener('click', function (event) {
        const target = event.target;
        if (target.classList.contains('player-button')) {
            handlePlayerButtonClick(target);
        }
    });


    // Function to handle the analyze squad button click
    document.getElementById('analyze-squad-btn').addEventListener('click', function() {
        // Check if there are 11 players added to the field
        //if (addedPlayerCount === 11) {
            console.log('Analyzing squad...');
            const squadPlayers = {}; // Object to store players by position
              
            // Iterate over player names and get their positions
            Object.keys(playerPositionMapping).forEach(playerName => {
                const position = playerPositionMapping[playerName];
                // Store player name under their position
                if (!squadPlayers[position]) {
                    squadPlayers[position] = [];
                }
                squadPlayers[position].push(playerName);
            });
    
            // Iterate over positions and get stats
            Object.keys(squadPlayers).forEach(position => {
                const squadPosition = squadPlayers[position];
                console.log('Analyzing position:', position, 'with players:', squadPosition);
                // Fetch stats for the position from the server

                const playerString = JSON.stringify(squadPlayers[position]);
                console.log('Player string:', playerString);
                // Fetch stats for the position from the server
                fetch(`/api/squad-stats/${position}/${playerString}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error(`Failed to fetch stats for position ${position}`);
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Store stats for the position
                        console.log('Stats for position:', data);
                        // Iterate over the received data
                        Object.keys(data).forEach(position => {
                            const positionStats = data[position];
                            
                            // Iterate over players in the position
                            Object.keys(positionStats).forEach(playerName => {
                                const playerStats = positionStats[playerName];
                                
                                // Display the player's name
                                const playerNameElement = document.createElement('div');
                                playerNameElement.innerHTML = `<strong>${playerName}:</strong>`;
                                document.getElementById('standout-stats').appendChild(playerNameElement);
                                
                                // Iterate over player stats
                                Object.keys(playerStats).forEach(statName => {
                                    const stat = playerStats[statName];
                                    let hasStandoutStat = false;
                                    // Check if the stat is standout
                                    if ((stat.is_max || stat.is_min || stat.comparison !== 'average') && stat.comparison !== 'average') {
                                        hasStandoutStat = true;
                                        let symbol = '';
                                        let color = '';
                                        if (stat.comparison.includes('above')) {
                                            symbol = '+';
                                            color = 'green';
                                        } else if (stat.comparison.includes('below')) {
                                            symbol = '-';
                                            color = 'red';
                                        }
                                        
                                        // Display the standout stat in your HTML
                                        const statElement = document.createElement('div');
                                        statElement.style.color = color;
                                        statElement.innerHTML = `${symbol} ${statName} - ${stat.value} (${stat.comparison})`;
                                        
                                        // Append the stat element to your HTML
                                        document.getElementById('standout-stats').appendChild(statElement);
                                    }
                                });

                                // If no standout stats, display "Player is solid"
                                if (!hasStandoutStat) {
                                    const solidPlayerElement = document.createElement('div');
                                    solidPlayerElement.innerHTML = `Player is solid`;
                                    document.getElementById('standout-stats').appendChild(solidPlayerElement);
                                }
                            });
                        });
                    })
                    .catch(error => {
                        //Ahora está fallando, no sé como se hace el fetch en el servidor (he intentado hacerlo como en player_detail.js pero no funciona)
                        console.error('Error fetching stats:', error);
                    });
            });

            // Display squad players with their positions
            //console.log('Squad Players:', squadPlayers);
           // console.log('Squad Stats:', squadStats);
        //} else {
        //    alert('Please add 11 players to analyze the squad.');
        //}
    });
    

});


// Function to display standout stats (good or bad) for a position
function displayStandoutStats(position, stats) {
    // Iterate over stats for the position and check for standout values
    Object.keys(stats[position]).forEach(attribute => {
        const attributeStats = stats[position][attribute];
        // Check for standout values (e.g., above-average or below-average)
        if (attributeStats.avg > 0) { //De prueba, habría que cambiarlo por algo más significativo
            console.log(`Position ${position}: ${attribute} has above-average value: ${attributeStats.avg}`);
        }
        //Estaría bien que se mostrara en la interfaz para cada jugador un resumen de en qué destaca y qué le falta
        //Igual esto es mejor hacerlo en python para poder reutilizarlo en otros sitios
    });
}