// Define a mapping of profiles to archetypes and their corresponding attributes
const archetypesByProfile = {
    'forward': {
        'Striker': ['Hdr_rat', 'Conv_rat', 'Gol_90'],
        'Target-man': ['Hdr_rat', 'Key_hdr_90', 'Ch_c_90'],
        'False-nine': ['Ch_c_90', 'Key_pass_90', 'Pr_pass_90']
    },
    'winger': {
        'Wide-winger': ['Drb_90', 'Ch_c_90', 'Cr_c_90'],
        'Inverted-winger': ['Drb_90', 'Shot_rat', 'Gol_90']
    },
    'midfielder': {
        'Regista': ['Pass_rat', 'Pr_pass_90', 'Cr_c_90'],
        'Play-maker': ['Pr_pass_90', 'Key_pass_90', 'Ch_c_90'],
        'Box-to-box': ['Int_90', 'Dist_90', 'Tackles_rat']
    },
    'defender': {
        'Ball-playing': ['Pass_rat', 'Pr_pass_90', 'Blocks_90'],
        'Stopper': ['Tackles_rat', 'Int_90', 'Hdr_rat'],
        'Full-back': ['Blocks_90', 'Tackles_rat', 'Dist_90'],
        'Wing-back': ['Cr_c_90', 'Drb_90', 'Dist_90']
    },
    'goalkeeper': {
        'Ball-playing': ['Pass_rat', 'Pr_pass_90'],
        'Penalty-specialist': ['Pen_saved_rat']
    }
};

// Define a mapping of profiles to positions
const positionsByProfile = {
    'forward': ['STC'],
    'winger': ['AML', 'AMR', 'ML', 'MR'], 
    'midfielder': ['MC', 'DM', 'AMC'],
    'defender': ['DC', 'DL', 'DR', 'WBL', 'WBR'],
    'goalkeeper': ['GK']
};


document.addEventListener('DOMContentLoaded', function() {
    // Get the select elements
    const profileSelect = document.getElementById('profile');
    const archetypeSelect = document.getElementById('archetype');

    const recommendationSection = document.querySelector('.recommendation-section');

    const titleElement = document.getElementById('recommend-title');
    
    titleElement.style.display = 'none';


    // Global variable to keep track of the current index
    let currentIndex = 0;


    // Define data variable in the scope accessible to both the event listener and displayRecommendations function
    let newData = [];

    // Function to populate the archetype selection based on the selected profile
    function populateArchetypes() {
        console.log('Profile selection changed');
        const selectedProfile = profileSelect.value;
        const archetypes = archetypesByProfile[selectedProfile] || {};

        // Clear previous options
        archetypeSelect.innerHTML = '';

        // Populate the archetype selection with the new options
        Object.keys(archetypes).forEach(function(archetypeName) {
            const option = document.createElement('option');
            option.value = archetypeName;
            option.textContent = capitalize(archetypeName); // Optional: capitalize the archetype
            archetypeSelect.appendChild(option);
        });
    }

    // Event listener to trigger population of archetypes when profile selection changes
    profileSelect.addEventListener('change', populateArchetypes);

    // Initial population of archetypes based on the default profile selection
    populateArchetypes();

    // Optional: Function to capitalize the first letter of a string
    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    const recommendButton = document.getElementById('recommend');

    // Event listener to trigger recommendations when the "recommend" button is clicked
    recommendButton.addEventListener('click', function() {

        // Get the spinner container element
        const spinnerContainer = document.querySelector('.spinner-container');

        // Create the loading spinner element
        const loadingSpinner = document.createElement('div');
        loadingSpinner.classList.add('spinner'); // Apply the spinner CSS class

        // Append the loading spinner to the spinner container
        spinnerContainer.appendChild(loadingSpinner);

        // Get the select elements
        const profileSelect = document.getElementById('profile');
        const archetypeSelect = document.getElementById('archetype');
        const footSelect = document.getElementById('foot');

        // Get the selected values
        const selectedProfile = profileSelect.value;
        const selectedArchetype = archetypeSelect.value;
        const selectedFoot = footSelect.value;

        // Generate the list of positions based on the selected profile
        const positions = selectedProfile === 'all' ? [] : positionsByProfile[selectedProfile];

        // Generate the list of attributes based on the selected archetype
        const attributes = selectedArchetype === 'all' || selectedArchetype === '' ? [] : archetypesByProfile[selectedProfile][selectedArchetype];

        

        // Optional: Print the selected values and generated API URL for debugging
        console.log('Selected Profile:', selectedProfile);
        console.log('Selected Archetype:', selectedArchetype);
        console.log('Selected Foot:', selectedFoot);
        console.log('Positions:', positions);
        console.log('Attributes:', attributes);

        // Generate the API request URL
        const apiUrl = `/get_recommendations/?positions=${positions.join(',')}&attributes=${attributes.join(',')}&foot=${selectedFoot}`;
        console.log('API URL:', apiUrl);

        // Send the API request
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                newData = data;
                // Display the recommendations
                if (data.length > 0) {
                    currentIndex = 0; // Reset currentIndex to 0 when new recommendations are fetched
                    spinnerContainer.removeChild(loadingSpinner); // Remove the loading spinner
                    titleElement.style.display = 'block';
                    // Clear previous recommendations
                    //remove any button if they exist  
                    const ispreviousButton = document.getElementById('previousButton');
                    if (ispreviousButton) {
                        recommendationSection.removeChild(ispreviousButton);
                    }
                    
                    const isnextButton = document.getElementById('nextButton');
                    if (isnextButton) {
                        recommendationSection.removeChild(isnextButton);
                    }

                    
                 
                    
                    const previousButton = document.createElement('button');
                    previousButton.textContent = 'Previous';
                    previousButton.classList.add('primary-default-btn');
                    previousButton.id = 'previousButton';

                    previousButton.addEventListener('click', function() {
                        // Decrement currentIndex to move to the previous set of recommendations
                        if (currentIndex - 3 >= 0) {
                            currentIndex -= 3;
                        }

                        //currentIndex = (currentIndex - 3 + newData.length) % newData.length; // Ensure positive value

                        // Display recommendations based on the updated currentIndex
                        displayRecommendations(newData, selectedProfile, selectedArchetype, selectedFoot);
                        updateInfoText(); // Update the info text
                    });

                    recommendationSection.appendChild(previousButton);

                    const nextButton = document.createElement('button');
                    nextButton.textContent = 'Next';
                    nextButton.classList.add('primary-default-btn');
                    nextButton.id = 'nextButton';

                    nextButton.addEventListener('click', function() {
                        // Increment currentIndex to move to the next set of recommendations
                        if (currentIndex + 3 < newData.length) {
                            currentIndex += 3;
                        }
                        // Display recommendations based on the updated currentIndex
                        displayRecommendations(newData, selectedProfile, selectedArchetype, selectedFoot);
                        updateInfoText(); // Update the info text
                    });

                    nextButton.style.marginLeft = '10px'; // Adjust the margin as needed

                    recommendationSection.appendChild(nextButton);

                    
                    // Create info text element
                    const infoText = document.createElement('span');
                    infoText.id = 'infoText';

                    // Function to update info text
                    function updateInfoText() {
                        const currentPage = Math.floor(currentIndex / 3) + 1; // Current page number
                        const totalPages = Math.ceil(newData.length / 3); // Total number of pages
                        infoText.textContent = `Page ${currentPage} of ${totalPages}`; // Display page information
                    }

                    updateInfoText(); // Initial update

                    // Add separation between buttons and info text
                    const separationElement = document.createElement('div');
                    separationElement.style.marginTop = '10px'; // Adjust margin as needed
                    recommendationSection.appendChild(separationElement);

                    recommendationSection.appendChild(infoText);
                    displayRecommendations(data, selectedProfile, selectedArchetype, selectedFoot);
              
                }
                else {
                    alert('No recommendations found');
                }
            })
            .catch(error => {
                console.error('Error fetching recommendations:', error);
                alert('An error occurred while fetching recommendations');
            });
    });

    
    
    function displayRecommendations(data, selectedProfile, selectedArchetype, selectedFoot) {
    
        // Select recommendation containers
        const recommendationContainers = [
            document.getElementById('recommendation1'),
            document.getElementById('recommendation2'),
            document.getElementById('recommendation3')
        ];
    
        // Clear previous recommendations
        recommendationContainers.forEach(container => {
            container.innerHTML = ''; // Clear the container
        });
    
        // Slice the data array starting from currentIndex to display the next set of players
        const slicedData = data.slice(currentIndex, currentIndex + 3);
    
        // Populate recommendation containers
        slicedData.forEach((recommendation, index) => {
            const container = recommendationContainers[index];

            // Assuming recommendation object contains an 'id' property
            const playerId = recommendation.id;

            // Create a link (anchor) element
            const playerLink = document.createElement('a');
            const playerLinkImage = document.createElement('a');

            // Set the href attribute to the URL of the player_detail page for the specific player
            const playerDetailUrl = `/player/${playerId}`; // Replace playerId with the actual player ID
            playerLink.href = playerDetailUrl;
            playerLinkImage.href = playerDetailUrl;
            playerLink.target = '_blank';
            playerLinkImage.target = '_blank';

            const playerImageFilename = `${playerId}.png`; // or whatever extension your images have
            const playerImageUrl = `/static/smartscore/images/faces/${playerImageFilename}`;

            // Now playerImageUrl contains the URL for the player image
            const playerImageElement = document.createElement('img');
            playerImageElement.src = playerImageUrl; // Use the URL
            playerImageElement.alt = 'Player Image';
            playerImageElement.classList.add('player-image'); // Add class for player image

            playerImageElement.addEventListener('error', function() {
                // If the image fails to load, use a placeholder image
                playerImageElement.src = '/static/smartscore/images/faces/unknown.png';
            });

            // Append the shirt image element to the player link
            playerLinkImage.appendChild(playerImageElement);
            container.appendChild(playerLinkImage);
            
            // Create player element
            const playerElement = document.createElement('div');
            playerElement.classList.add('shirt-container'); // Add class for shirt container
    
            // Create shirt image element
            const shirtImageElement = document.createElement('img');
            shirtImageElement.src = shirt_img; // Use the variable defined in your HTML
            shirtImageElement.alt = 'Shirt';
            shirtImageElement.classList.add('shirt-image'); // Add class for shirt image
            // Create player details container
            const playerDetailsElement = document.createElement('div');
            playerDetailsElement.classList.add('player-details');
    
            // Create player name element
            const playerNameElement = document.createElement('p');
            playerNameElement.classList.add('player-name');
            nameParts = recommendation.name.split(' ');
            lastName = nameParts[nameParts.length - 1];
            playerNameElement.textContent = lastName;
    
            // Create player number element
            const playerNumberElement = document.createElement('p');
            playerNumberElement.classList.add('player-number');
            playerNumberElement.textContent = recommendation.dorsal;
    
            // Append elements to player details container
            playerDetailsElement.appendChild(playerNameElement);
            playerDetailsElement.appendChild(playerNumberElement);
    
            // Append shirt image and player details container to player element
            playerElement.appendChild(shirtImageElement);
            playerElement.appendChild(playerDetailsElement);
            playerLink.appendChild(playerElement);
            // Append player element to recommendation container
            //container.appendChild(playerElement);
            container.appendChild(playerLink);
            // Create container for smart score display and save button
            const smartScoreAndButtonContainer = document.createElement('div');
            smartScoreAndButtonContainer.style.display = 'inline-block'; // Set display property

    
           // Create smart score container
            const smartScoreContainer = document.createElement('div');
            smartScoreContainer.classList.add('bubble-container-smartscore');
    
            // Create smart score display element
            const smartScoreDisplay = document.createElement('div');
            smartScoreDisplay.id = 'smartScoreDisplay'; // Set the ID
            smartScoreDisplay.classList.add('bubble-smartscore'); // Add class
            // Set smart score value
            smartScoreDisplay.textContent = recommendation.score;
    
            // Append smart score display to smart score container
            smartScoreContainer.appendChild(smartScoreDisplay);

            // Add save button
            const saveButton = document.createElement('button');
            saveButton.id = 'save';
            saveButton.textContent = 'Save';
            saveButton.classList.add('primary-default-btn');

            // Add some separation to the save button
            saveButton.style.marginBottom = '10px'; // Adjust the margin as needed

            // Append the save button to the recommendation section
            

            const requestData = {
                position: selectedProfile,
                archetype: selectedArchetype,
                foot: selectedFoot,
                recommendation: recommendation  // Include the recommendations data
            };

            console.log('Data:', requestData);

            saveButton.addEventListener('click', function() {
                fetch('/api/save-recommendations/', {
                    method: 'POST',  
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },        
                    body: JSON.stringify(requestData)                    
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Success:', data);
                        alert(data.message);
                    })
                    .catch(error => {
                        console.error('Error saving recommendations:', error);
                        spinnerContainer.removeChild(loadingSpinner); // Remove the loading spinner
                        alert('An error occurred while saving recommendations');
                    });
            });
    
            smartScoreAndButtonContainer.appendChild(smartScoreContainer);
            smartScoreAndButtonContainer.appendChild(saveButton);
            container.appendChild(smartScoreAndButtonContainer);

            updateBubbleColor(recommendation.score, smartScoreDisplay);
        });
    }

    function updateBubbleColor(smartscore, smartScoreDisplay) {
        if (smartScoreDisplay) {
            smartScoreDisplay.style.backgroundColor = testColorGradient(smartscore);
        }      
    }
});

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function testColorGradient(smartscore){
    var color1 = {
        red: 19, green: 233, blue: 19
        };
    var color3 = {
        red: 255, green: 0, blue: 0
        };
    var color2 = {
        red: 255, green: 255, blue: 0
        };
    color = colorGradient(1- smartscore/100, color1, color2, color3);
    return color;
}

function colorGradient(fadeFraction, rgbColor1, rgbColor2, rgbColor3) {
    var color1 = rgbColor1;
    var color2 = rgbColor2;
    var fade = fadeFraction;

    // Do we have 3 colors for the gradient? Need to adjust the params.
    if (rgbColor3) {
      fade = fade * 2;

      // Find which interval to use and adjust the fade percentage
      if (fade >= 1) {
        fade -= 1;
        color1 = rgbColor2;
        color2 = rgbColor3;
      }
    }

    var diffRed = color2.red - color1.red;
    var diffGreen = color2.green - color1.green;
    var diffBlue = color2.blue - color1.blue;

    var gradient = {
      red: parseInt(Math.floor(color1.red + (diffRed * fade)), 10),
      green: parseInt(Math.floor(color1.green + (diffGreen * fade)), 10),
      blue: parseInt(Math.floor(color1.blue + (diffBlue * fade)), 10),
    };

    return 'rgb(' + gradient.red + ',' + gradient.green + ',' + gradient.blue + ')';
}
