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
        'Stopper': ['Tackles_rat', 'Intercept_90', 'Hdr_rat'],
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
    'midfielder': ['MC', 'DMC', 'AMC', 'ML', 'MR'],
    'defender': ['DC', 'DL', 'DR', 'WBL', 'WBR'],
    'goalkeeper': ['GK']
};


document.addEventListener('DOMContentLoaded', function() {
    // Get the select elements
    const profileSelect = document.getElementById('profile');
    const archetypeSelect = document.getElementById('archetype');

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
                console.log('Recommendations:', data);
                // Handle the received recommendations (e.g., display them on the page)
            })
            .catch(error => {
                console.error('Error fetching recommendations:', error);
                // Handle errors (e.g., display an error message)
            });
    });
});
