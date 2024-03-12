// Define a mapping of profiles to archetypes and their corresponding attributes
const archetypesByProfile = {
    'attacker': {
        'All': [],
        'Striker': ['Hdr_rat', 'Conv_rat', 'Gol_90'],
        'Target-man': ['Hdr_rat', 'Key_hdr_90', 'Ch_c_90'],
        'False-nine': ['Ch_c_90', 'Key_pass_90', 'Pr_pass_90'],
        'Wide-winger': ['Drb_90', 'Ch_c_90', 'Cr_c_90'],
        'Inverted-winger': ['Drb_90', 'Shot_rat', 'Gol_90'],
    },
    'midfielder': {
        'All': [],
        'Regista': ['Pass_rat', 'Pr_pass_90', 'Cr_c_90'],
        'Play-maker': ['Pr_pass_90', 'Key_pass_90', 'Ch_c_90'],
        'Box-to-box': ['Int_90', 'Dist_90', 'Tackles_rat']
    },
    'defender': {
        'All': [],
        'Ball-playing': ['Pass_rat', 'Pr_pass_90', 'Blocks_90'],
        'Stopper': ['Tackles_rat', 'Int_90', 'Hdr_rat'],
        'Full-back': ['Blocks_90', 'Tackles_rat', 'Dist_90'],
        'Wing-back': ['Cr_c_90', 'Drb_90', 'Dist_90']
    },
    'goalkeeper': {
        'All': [],
        'Ball-playing': ['Pass_rat', 'Pr_pass_90'],
        'Penalty-specialist': ['Pen_saved_rat']
    }
};

// Define a mapping of profiles to positions
const positionsByProfile = {
    'attacker': ['STC', 'AML', 'AMR'],
    'midfielder': ['MC', 'DM', 'AMC', 'ML', 'MR'],
    'defender': ['DC', 'DL', 'DR', 'WBL', 'WBR'],
    'goalkeeper': ['GK']
};


document.addEventListener('DOMContentLoaded', function() {
    // Get the select elements
    const profileSelect = document.getElementById('profile');
    const archetypeSelect = document.getElementById('archetype');

    // Get the regenerate button
    const regenerateButton = document.getElementById('regenerate');

    // Global variable to keep track of the current index
    let currentIndex = 0;

    // Event listener for regenerate button

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

                    displayRecommendations(data);
                }
                else {
                    alert('No recommendations found');
                }

            })
            .catch(error => {
                console.error('Error fetching recommendations:', error);
                // Handle errors (e.g., display an error message)
            });
    });

    regenerateButton.addEventListener('click', function() {
        // Increment currentIndex to shift the recommendations to the next set
        currentIndex = (currentIndex + 3) % newData.length; // Wrap around to the beginning if currentIndex exceeds data length
    
        // Display recommendations based on the updated currentIndex
        displayRecommendations(newData);
    });
    

    function displayRecommendations(data) {
        console.log('Recommendations:', data);
    
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
            
            // Create player element
            const playerElement = document.createElement('div');
            playerElement.classList.add('shirt-container'); // Add class for shirt container
    
            // Create shirt image element
            const shirtImageElement = document.createElement('img');
            shirtImageElement.src = shirt_img; // Use the variable defined in your HTML
            shirtImageElement.alt = 'Shirt';
    
            // Create player details container
            const playerDetailsElement = document.createElement('div');
            playerDetailsElement.classList.add('player-details');
    
            // Create player name element
            const playerNameElement = document.createElement('p');
            playerNameElement.classList.add('player-name');
            playerNameElement.textContent = recommendation.name;
    
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
    
            // Append player element to recommendation container
            container.appendChild(playerElement);
    
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

            // Append smart score container to recommendation container
            container.appendChild(smartScoreContainer);
        });
    }

});
