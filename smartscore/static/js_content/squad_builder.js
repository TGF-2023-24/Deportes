
const positionMapping = {
    'GK': { top: '760px', left: '250px' },
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

const positionLimits = {
    'GK': 1, // Limit for Goalkeeper
    'DC': 3, // Limit for Defender Center
    'DL': 1, // Limit for Defender Left
    'DR': 1, // Limit for Defender Right
    'DM': 2, // Limit for Defensive Midfielder
    'WBL': 1, // Limit for Wing Back Left
    'WBR': 1, // Limit for Wing Back Right
    'MC': 3, // Limit for Midfielder Center
    'ML': 1, // Limit for Midfielder Left
    'MR': 1, // Limit for Midfielder Right
    'AMC': 2, // Limit for Attacking Midfielder Center
    'AML': 1, // Limit for Attacking Midfielder Left
    'AMR': 1, // Limit for Attacking Midfielder Right
    'STC': 2 // Limit for Striker Center
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
            
            if (blockedPlayers.has(player)) {
                playerBut.style.textDecoration = 'line-through';
                playerBut.classList.add('clicked');
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
        if (blockedPlayers.has(playerBut.textContent)) {
            alert('This player is already selected.');          
            return;
        }

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
    
    // Initialize an array to store player position containers for each position
    const playerPositionContainers = {};

    function addPlayerImage(position, playerName) {
        console.log('Adding player image:', playerName, 'at position:', position);
        const fieldContainer = document.querySelector('.football-field-container-squad-builder');
        console.log(fieldContainer);
        const containerWidth = fieldContainer.offsetWidth;
        const containerHeight = fieldContainer.offsetHeight;

        // Initialize player count for this position if it doesn't exist
        if (!playerCounts[position]) {
            playerCounts[position] = 0;
        }
        // Check if the position limit has been reached
        if (playerCounts[position] >= positionLimits[position]) {
            alert(`Cannot add player to ${position}. Maximum limit reached.`);
            return -1; // Exit the function if the limit is reached
        }

        // Get the number of players already present at this position
        const numPlayers = playerCounts[position];

        console.log('Number of players at position:', position, 'is:', numPlayers);

        playerPositionMapping[playerName] = position;
        const playerPosition = document.createElement('div');
        playerPosition.className = 'player-position';
        playerPosition.id = `player-position-${playerName}`; // Add unique id for the player position
        playerPosition.style.position = 'absolute'; // Position absolutely

        //Get player ID from the name
        fetch('/get-id-from-playerName/' + playerName + '/' + position)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch player ID');
                }
                return response.json();
            })
            .then(data => {
                playerID = data.id;
                //Convert player ID to string
                playerID = playerID.toString();
                console.log('Player ID (string):', playerID);

                // Create a hidden input field to store the player ID
                const playerIdInput = document.createElement('input');
                playerIdInput.type = 'hidden';
                playerIdInput.name = playerName; // Set the name attribute if you are submitting a form
                playerIdInput.value = playerID; // Set the value to the player ID
                playerPosition.appendChild(playerIdInput);


                // Create an img element for the player's image
                const playerImage = document.createElement('img');
                playerImage.src = `/static/smartscore/images/faces/${playerID}.png`; // Replace with the correct path to your player images
                playerImage.addEventListener('error', function () {
                    playerImage.src = '/static/smartscore/images/faces/default.png'; // Replace with the default image path
                });
                playerImage.alt = playerName; // Set alt text to player's name
                playerImage.style.width = '90px'; // Adjust width as needed
                playerImage.style.height = '100px'; // Adjust height as needed

                // Calculate the position of the image based on container dimensions
                const left = parseFloat(positionMapping[position].left) / 500 * containerWidth; // Normalize left position
                const top = parseFloat(positionMapping[position].top) / 800 * containerHeight; // Normalize top position

                playerPosition.style.left = left + 'px';
                playerPosition.style.top = top - 20 + 'px';
                fieldContainer.appendChild(playerPosition);
                console.log('Player image added:', playerName, 'at position:', left, top);

                // Append the player image to the player position container
                playerPosition.appendChild(playerImage);

                // Increment the player count for this position
                playerCounts[position]++;

                console.log('Player position containers:', playerPositionContainers);
                // Add the player position container to the array for this position
                if (!playerPositionContainers[position]) {
                    playerPositionContainers[position] = [];
                }
                playerPositionContainers[position].push(playerPosition);

                // Add the remove button
                const removeButton = document.createElement('button');
                removeButton.textContent = 'X';
                removeButton.classList.add('remove-button');
                removeButton.id = `remove-button-${playerName}`; // Add unique id for the remove button
                removeButton.style.position = 'absolute';
                removeButton.style.top = -10 + 'px'; // Adjust the position of the button
                removeButton.style.left = 78 + 'px'; // Adjust the position of the button
                console.log('Remove button added:', playerName, 'at position:', left + 20, top - 20);

                // Add click event listener to remove the player
                removeButton.addEventListener('click', function () {
                    playerPosition.remove();
                    removeButton.remove();
                    // Update player counts and position mapping
                    const removedPlayerName = playerName.trim();
                    delete playerPositionMapping[removedPlayerName];
                    addedPlayerCount--;
                    playerCounts[position]--;
                    //remove the player from the blocked players
                    blockedPlayers.delete(removedPlayerName);
                    console.log('Player removed:', removedPlayerName);
                    // remove linethrough style from the button
                    const playerButtons = document.querySelectorAll('.player-button');
                    playerButtons.forEach(button => {
                        if (button.textContent == removedPlayerName) {
                            button.style.textDecoration = 'none';
                            button.classList.remove('active');
                            button.classList.remove('clicked');

                        }
                    });
                });
                // Append the remove button to the player position container
                playerPosition.appendChild(removeButton);

                //Add the player name under the image
                const playerNameElement = document.createElement('div');
                playerNameElement.className = 'player-position-name';
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
                playerNameElement.textContent = printedName;
                //playerNameElement.style.position = 'absolute';
                playerNameElement.style.top = 100 + 'px'; // Adjust the position of the player name
                //playerNameElement.style.left = 25 + 'px'; // Adjust the position of the player name
                playerPosition.appendChild(playerNameElement);

                if (playerCounts[position] > 1) {
                // Adjust position of players based on the number of players at the position
                    for (let i = 0; i < playerPositionContainers[position].length; i++) {
                        let playerPositionContainer = playerPositionContainers[position][i];
                        console.log('Adjusting position of container:', playerPositionContainer);
                        // Adjust left position, first one to the left, second one to the right, and third one to the center
                        if (playerCounts[position] === 2) {
                            playerPositionContainer.style.left = (left + (i === 0 ? -48 : 48)) + 'px';
                        } else if (playerCounts[position] === 3) {
                            playerPositionContainer.style.left = (left + (i === 0 ? -88 : (i === 1 ? 88 : 0))) + 'px';
                        }
                    }
                }
            })


            .catch(error => {
                console.error('Error fetching player ID:', error);
            });

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
            if (addPlayerImage(selectedPosition, playerName) == -1) {
                return;
            }
            // Block the player
            blockedPlayers.add(playerName);
            console.log('Player blocked:', playerName);
            // Apply the line-through style to the button
            activePlayerButton.style.textDecoration = 'line-through';

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
        /*if (addedPlayerCount < 11) {
            alert('Please add 11 players to analyze the squad.');
            return;
        }*/
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

        const hiddenInputs = document.getElementsByName(playerName);
        if (hiddenInputs.length > 0) {
            const playerId = hiddenInputs[0].value;
            console.log("Player ID:", playerId);
        } else {
            console.log("Hidden input field for player not found.");
        }
        
        fetch (`/api/compare-players/${currentPlayer}/${playerName}/${position}`) 
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to fetch stats for ${currentPlayer}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Player stats:', data);
                radar = displayRadarChart(data, position);
            })

        const infoElement = document.createElement('p');
        infoElement.innerHTML = `Player ${currentPlayerIndex + 1} of ${replacementPlayers.length}`;
        infoElement.classList.add('info-element');

        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.classList.add('next-button'); // Add the next-button class
        nextButton.addEventListener('click', () => {
            // Update currentPlayerIndex to display the next player
            radar.remove();
            currentPlayerIndex = (currentPlayerIndex + 1) % replacementPlayers.length;
            const nextPlayer = replacementPlayers[currentPlayerIndex];
            currentPlayer = nextPlayer;
            playerNameElement.innerHTML = `<h3>${nextPlayer} (${position})</h3>`;
            fetch (`/api/compare-players/${nextPlayer}/${playerName}/${position}`) 
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to fetch stats for ${nextPlayer}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Player stats:', data);
                    radar = displayRadarChart(data, position);
                })
                infoElement.innerHTML = `Player ${currentPlayerIndex + 1} of ${replacementPlayers.length}`;
        });

        const previousButton = document.createElement('button');
        previousButton.textContent = 'Previous';
        previousButton.classList.add('previous-button'); // Add the previous-button class
        previousButton.addEventListener('click', () => {
            // Update currentPlayerIndex to display the previous player
            radar.remove();
            currentPlayerIndex = (currentPlayerIndex - 1 + replacementPlayers.length) % replacementPlayers.length;
            const previousPlayer = replacementPlayers[currentPlayerIndex];
            currentPlayer = previousPlayer;
            playerNameElement.innerHTML = `<h3>${previousPlayer} (${position})</h3>`;
            fetch (`/api/compare-players/${previousPlayer}/${playerName}/${position}`)

                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to fetch stats for ${previousPlayer}`);
                    }   
                    return response.json();
                })
                .then(data => {
                    console.log('Player stats:', data);
                    radar = displayRadarChart(data, position);
                })
                infoElement.innerHTML = `Player ${currentPlayerIndex + 1} of ${replacementPlayers.length}`;
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

                    // Clear the replacement player container
                    const replacementPlayerContainer = document.getElementById('replacement-player-container');
                    replacementPlayerContainer.innerHTML = '';
                    // Re-fetch and update squad analysis data
                    //Eliminate oldplayer from squad and button
                    
                    const playerToRemove = document.getElementById(`player-position-${playerName}`);
                    if (playerToRemove) {
                        playerToRemove.remove(); // Remove the player div
                    }

                    // Remove the remove button
                    const removeButtonToRemove = document.getElementById(`remove-button-${playerName}`);
                    if (removeButtonToRemove) {
                        removeButtonToRemove.remove(); // Remove the remove button
                    }
                    // Update the player count for the position
                    playerCounts[position]--;
                    //Add new player to squad
                    addPlayerImage(position, currentPlayer);
                    // Update the blocked players
                    blockedPlayers.delete(playerName);
                    blockedPlayers.add(currentPlayer);
                    
                    // Update the player position mapping
                    delete playerPositionMapping[playerName];
                    playerPositionMapping[currentPlayer] = position;

                    //delete old player button and add new player button active and clicked
                    const playerButtons = document.querySelectorAll('.player-button');
                    playerButtons.forEach(button => {
                        if (button.textContent == playerName) {
                            button.style.textDecoration = 'none';
                            button.classList.remove('active');
                            button.classList.remove('clicked');
                        }
                        if (button.textContent == currentPlayer) {
                            button.classList.add('active');
                            button.classList.add('clicked');
                            button.style.textDecoration = 'line-through';
                        }
                    });
                    // click the dot position button to display new button
                    const dotButton = document.querySelectorAll('.player-position-dot')
                    dotButton.forEach(dot => {
                        if (dot.position == position) {
                            dot.click();
                            dot.click();
                        }
                    });
                    document.getElementById('analyze-squad-btn').click();
                                                
                })
            }
            
        });

        
        replacementPlayerContainer.appendChild(playerNameElement);
        replacementPlayerContainer.appendChild(previousButton);
        replacementPlayerContainer.appendChild(nextButton);
        replacementPlayerContainer.appendChild(replaceButton);
        replacementPlayerContainer.appendChild(infoElement);
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

        return radarChartDiv;
    }

});

