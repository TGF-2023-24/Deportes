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
    let playerCounts = {};
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

            // Check if the player is blocked
            playerBut.addEventListener('click', function () {
                handlePlayerButtonClick(playerBut);
                // Apply style if player is blocked
                if (blockedPlayers.has(player)) {
                    playerBut.style.textDecoration = 'line-through';
                }
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
            activePlayerButton.classList.remove('clicked');
        }

        // Set the current button as active
        playerBut.classList.add('active');
        activePlayerButton = playerBut;

         // Add the "clicked" class to change color
        playerBut.classList.add('clicked');

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

        console.log('Number of players at position:', position, 'is:', numPlayers);
        
        playerPositionMapping[playerName] = position;
        const playerPosition = document.createElement('div');
        playerPosition.className = 'player-position';
        playerPosition.style.position = 'absolute'; // Position absolutely
        //Split player name to get surname
        const playerNameSplit = playerName.split(" ");
        //If it's a double name, we take the second part
        if (playerNameSplit.length > 2) {
            printedName = playerNameSplit[1] + " " + playerNameSplit[2];
        }
        else if (playerNameSplit.length == 1) {
            printedName = playerNameSplit[0];
        }
        else {
            printedName = playerNameSplit[1];
        }
        playerPosition.textContent = printedName;
        // Calculate the position of the dot based on container dimensions
        const left = parseFloat(positionMapping[position].left) / 500 * containerWidth; // Normalize left position
        const top = parseFloat(positionMapping[position].top) / 800 * containerHeight + numPlayers * 30; // Normalize top position
        playerPosition.style.left = left + 'px';
        playerPosition.style.top = top + 'px';
        fieldContainer.appendChild(playerPosition);
        console.log('Player added:', playerName, 'at position:', left, top);
        // Increment the player count for this position
        playerCounts[position]++;
  
            
        // Add the remove button
        const removeButton = document.createElement('button');
        removeButton.textContent = 'X';
        removeButton.classList.add('remove-button');
        removeButton.style.position = 'absolute';
        removeButton.style.top = (top - 20) + 'px'; // Adjust the position of the button
        removeButton.style.left = (left + 20) + 'px'; // Adjust the position of the button

        // Add click event listener to remove the player
        removeButton.addEventListener('click', function () {
            playerPosition.remove();
            removeButton.remove();
            // Update player counts and position mapping
            const removedPlayerName = playerName.trim();
            playerCounts[position]--;
            delete playerPositionMapping[removedPlayerName];
            addedPlayerCount--;
        });

        fieldContainer.appendChild(removeButton);
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

    // Function to handle add-player button click
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
            // Block the player
            blockedPlayers.add(playerName);
            console.log('Player blocked:', playerName);
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

    let currentPlayerIndex = 0;
    // Function to handle the analyze squad button click
    document.getElementById('analyze-squad-btn').addEventListener('click', function() {
        // Check if there are 11 players added to the field
        //if (addedPlayerCount === 11) {
            document.getElementById('standout-stats').innerHTML = '';
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
                                let hasStandoutStat = false;
                                let positiveStatsCount = 0;
                                let negativeStatsCount = 0;
                                // Display the player's name
                                const playerNameElement = document.createElement('div');
                                playerNameElement.innerHTML = `<strong>${playerName} (${position}):</strong>`;
                                document.getElementById('standout-stats').appendChild(playerNameElement);
                                
                                // Iterate over player stats
                                Object.keys(playerStats).forEach(statName => {
                                    const stat = playerStats[statName];
                                    // Check if the stat is standout
                                    if ((stat.is_max || stat.is_min || stat.comparison !== 'average') && stat.comparison !== 'average') {
                                        hasStandoutStat = true;
                                        let symbol = '';
                                        let color = '';
                                        if (stat.comparison.includes('above')) {
                                            symbol = '+';
                                            color = 'forestgreen';
                                            positiveStatsCount++;
                                        } else if (stat.comparison.includes('below')) {
                                            symbol = '-';
                                            color = 'red';
                                            negativeStatsCount++;
                                        } else if (stat.comparison.includes('exceptional')) {
                                            symbol = '⬆';
                                            color = 'darkgreen';
                                            positiveStatsCount++;
                                        } else if (stat.comparison.includes('horrible')) {
                                            symbol = '⬇';
                                            color = 'darkred';
                                            negativeStatsCount++;
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
                                
                                else if (negativeStatsCount > positiveStatsCount) {
                                    //Add a replace button
                                    console.log(`We need to replace ${playerName}`)
                                    const replaceButton = document.createElement('button');
                                    replaceButton.innerHTML = 'Replace';
                                    replaceButton.classList.add('replace-button');
                                    replaceButton.addEventListener('click', () => {
                                        // Hay que implementar esto
                                        console.log(`Replace ${playerName}`);
                                        const squadId = document.getElementById('squad-select').value;

                                        fetch(`/api/replacement-players/${position}/${playerName}/${squadId}`)
                                        .then(response => {
                                            if (!response.ok) {
                                                throw new Error(`Failed to fetch replacement players for ${playerName}`);
                                            }
                                            return response.json();
                                        })
                                        .then(data => {
                                            console.log('Replacement players:', data);
                                            currentPlayerIndex = 0;
                                            displayReplacementPlayers(data, position, playerName);
                                        })
                                        .catch(error => {
                                            console.error('Error fetching replacement players:', error);
                                        });
                                    });
                                    document.getElementById('standout-stats').appendChild(replaceButton);
                                }

                            });
                        });
                    })
                    .catch(error => {
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


    // Function to display replacement players
    function displayReplacementPlayers(replacementPlayers, position, playerName) {
        const replacementPlayerContainer = document.getElementById('replacement-player-container');
        replacementPlayerContainer.innerHTML = ''; // Clear previous content

        if (replacementPlayers.length === 0) {
            const noReplacementMsg = document.createElement('p');
            noReplacementMsg.textContent = 'No replacement players available.';
            replacementPlayerContainer.appendChild(noReplacementMsg);
            return;
        }

        // Get the current player based on the currentPlayerIndex
        let  currentPlayer = replacementPlayers[currentPlayerIndex];

        const playerNameElement = document.createElement('p');
        playerNameElement.innerHTML = `<h3>${currentPlayer} (${position})</h3>`;

        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.classList.add('next-button'); // Add the next-button class
        nextButton.addEventListener('click', () => {
            // Update currentPlayerIndex to display the next player
            currentPlayerIndex = (currentPlayerIndex + 1) % replacementPlayers.length;
            const nextPlayer = replacementPlayers[currentPlayerIndex];
            currentPlayer = nextPlayer;
            playerNameElement.innerHTML = `<h3>${nextPlayer} (${position})</h3>`;
            
        });

        
        const replaceButton = document.createElement('button');
        replaceButton.textContent = 'Replace';
        replaceButton.classList.add('replace2-button'); // Add the replace-button class
        replaceButton.addEventListener('click', () => {
            // Implement the functionality to replace the player in the squad
            // Get the squad ID from the dropdown
            const confirmMessage = `Are you sure you want to replace ${playerName}?`;
            if (confirm(confirmMessage)) {
                const squadId = document.getElementById('squad-select').value;
                console.log(squadId);
                // Get the player to be replaced
                console.log('Player to be removed: ' + playerName);
                // Remove the player from the squad
                // Add the new player to the squad
                console.log('New player:', currentPlayer);
                fetch(`/api/replace-player/${squadId}/${playerName}/${currentPlayer}/${position}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to replace player ${playerName} with ${currentPlayer}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Squad after replacement:', data);
                    
                    handleSquadSelection();
                    resetProgramState();
                    
                    playerCounts[position] = 0;
                })
            }
            
        });

        const compareButton = document.createElement('button');
        compareButton.textContent = 'Compare stats';
        compareButton.classList.add('compare-button'); // Add the compare-button class
        compareButton.addEventListener('click', () => {
            
            // Implement the functionality to compare the player with the current squad
            fetch (`/api/compare-players/${currentPlayer}/${playerName}/${position}`) 
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to fetch stats for ${currentPlayer}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Player stats:', data);
                displayRadarChart(data, position);
            })

            
            console.log('Compare player:', currentPlayer);
        });
        replacementPlayerContainer.appendChild(playerNameElement);
        replacementPlayerContainer.appendChild(nextButton);
        replacementPlayerContainer.appendChild(replaceButton);
        replacementPlayerContainer.appendChild(compareButton);
    }


    // Function to display radar chart
    
    function displayRadarChart(stats, position) {
        // Create a new div element for the radar chart
        const radarChartDiv = document.createElement('div');
        radarChartDiv.classList.add('radar-chart-container');

        // Create a canvas element for the chart
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 400;
        radarChartDiv.appendChild(canvas);

        // Create a close button
        const closeButton = document.createElement('button');
        closeButton.classList.add('close-button');
        closeButton.textContent = 'X';
        closeButton.addEventListener('click', () => {
            radarChartDiv.remove(); // Remove the radar chart div when the close button is clicked
        });
        radarChartDiv.appendChild(closeButton);

        // Append the radar chart div to the specific container replacemt-player-container
        document.getElementById('replacement-player-container').appendChild(radarChartDiv);

        // Extract player names and their stats
        const playerNames = Object.keys(stats);
        const playerStats = Object.values(stats);
        const labels = Object.keys(playerStats[0][playerNames[0]]);

        // Extract max and min values from average stats
        const avgStats = stats['avg'];
        const maxValues = {};
        const minValues = {};
        const avgPosStat = {};
        for (const positionName in avgStats) {
            const positionStats = avgStats[positionName];
            for (const statName in positionStats) {
                if (statName !== 'attribute_name') { // Skip non-statistic fields
                    const statValue = positionStats[statName];
                    if (typeof statValue === 'object') {
                        maxValues[statName] = statValue['max'];
                        minValues[statName] = statValue['min'];
                        avgPosStat[statName] = statValue['avg'];
                    }
                }
            }
        }

        console.log('Max values:', maxValues);
        console.log('Min values:', minValues);
        console.log('Avg values:', avgPosStat);

        // Create datasets for each player and the average
        const datasets = playerNames.map((playerName, index) => {
            if (playerName == 'avg') {
                return;
            }
            const playerValues = Object.values(playerStats[playerNames.indexOf(playerName)][playerName]);
            const normalizedPlayerValues = playerValues.map((value, idx) => {
                const statName = Object.keys(playerStats[playerNames.indexOf(playerName)][playerName])[idx];
                const normalizedValue = (value - minValues[statName]) * 100 / (maxValues[statName] - minValues[statName]);
                return normalizedValue;
            });
            return {
                label: playerName,
                data: normalizedPlayerValues,
                backgroundColor: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.2)`,
                borderColor: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 1)`,
                borderWidth: 1
            };
        });

        // Create dataset for average
        const avgValues = Object.values(avgPosStat);
        const normalizedAvgValues = avgValues.map((value, idx) => {
            const statName = Object.keys(avgPosStat)[idx];
            const normalizedValue = (value - minValues[statName]) * 100 / (maxValues[statName] - minValues[statName]);
            return normalizedValue;
        });
        datasets.push({
            label: 'Average',
            data: normalizedAvgValues,
            backgroundColor: 'rgba(255, 99, 132, 0.2)', // Example color
            borderColor: 'rgba(255, 99, 132, 1)', // Example color
            borderWidth: 1
        });

        // Create the radar chart using Chart.js
        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: datasets.filter(dataset => dataset !== undefined), // Filter out undefined datasets
            },
            options: {
                scale: {
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

});



// Function to reset the program state
function resetProgramState() {
    // Clear player positions
    const playerPositionDivs = document.querySelectorAll('.player-position');
    playerPositionDivs.forEach(div => {
        div.parentNode.removeChild(div); // Remove the div from its parent node
    });

    // Clear remove buttons
    const removeButtons = document.querySelectorAll('.remove-button');
    removeButtons.forEach(button => {
        button.parentNode.removeChild(button); // Remove the button from its parent node
    });
    // Clear replacement player container
    document.getElementById('replacement-player-container').innerHTML = '';

    // Clear standout stats
    document.getElementById('standout-stats').innerHTML = '';

    // Reset active player button
    if (activePlayerButton) {
        activePlayerButton.classList.remove('active');
        activePlayerButton.classList.remove('clicked');
        activePlayerButton = null;
    }

    // Reset player counts and position mapping
    blockedPlayers.clear();
    // Reset all values in playerCounts to 0
    playerCounts = {};
       
    playerPositionMapping = {};
    addedPlayerCount = 0;
    handleSquadSelection();
    console.log(playerCounts);
}
