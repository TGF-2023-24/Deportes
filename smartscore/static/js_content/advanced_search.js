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

fieldCategories = {
    general: [
        { displayName: 'Age', attributeName: 'Age' },
        { displayName: 'Height', attributeName: 'Height' },
        { displayName: 'Weight', attributeName: 'Weight' },
        { displayName: 'Salary', attributeName: 'Salary' },
       // { displayName: 'CAbil', attributeName: 'CAbil' },
       // { displayName: 'Pot_abil', attributeName: 'Pot_abil' },
        { displayName: 'Starter Matches', attributeName: 'Strater_match' },
        { displayName: 'Substitute Matches', attributeName: 'Res_match' },
        { displayName: 'International Matches', attributeName: 'International_match' },
        { displayName: 'Minutes', attributeName: 'Min' },
        { displayName: 'Distance / 90', attributeName: 'Dist_90' },
        { displayName: 'Shirt Number', attributeName: 'Dorsal' },
        { displayName: 'Name', attributeName: 'Name' },
        { displayName: 'Nationality', attributeName: 'Nacionality' },
        { displayName: 'Club', attributeName: 'Club' }, 
        { displayName: 'League', attributeName: 'League' },
    ],
    goalkeeping: [
        { displayName: 'Clean Sheets', attributeName: 'Clean_sheet' },
        { displayName: 'Goals Allowed', attributeName: 'Goal_allowed' },
        { displayName: 'Save Ratio', attributeName: 'Sv_rat' },
        { displayName: 'Expected Save Ratio', attributeName: 'xSv_rat' },
        { displayName: 'Penalty Save Ratio', attributeName: 'Pen_saved_rat' }
    ],
    defensive: [
        { displayName: 'Blocks / 90', attributeName: 'Blocks_90' },
        { displayName: 'Clearances / 90', attributeName: 'Clr_90' },
        { displayName: 'Interceptions / 90', attributeName: 'Int_90' },
        { displayName: 'Tackle Completion Ratio', attributeName: 'Tackles_rat' },
        { displayName: 'Key Tackles / 90', attributeName: 'Key_tck_90' },
        { displayName: 'Headers Won Ratio', attributeName: 'Hdr_rat' },
        { displayName: 'Key Headers / 90', attributeName: 'Key_hdr_90' },
        { displayName: 'Mistakes that Lead to Goals', attributeName: 'Gl_mistake' },
        { displayName: 'Fouls Commited', attributeName: 'Fcomm' }, 
        { displayName: 'Yellow Cards', attributeName: 'Yel' },
        { displayName: 'Red Cards', attributeName: 'Red' }
    ],
    creative: [
        { displayName: 'Assists', attributeName: 'Asis' },
        { displayName: 'Assists / 90', attributeName: 'Asis_90' },
        { displayName: 'Pass completion ratio', attributeName: 'Pass_rat' },
        { displayName: 'Progressive passes / 90', attributeName: 'Pr_pass_90' },
        { displayName: 'Key passes / 90', attributeName: 'Key_pass_90' },
        { displayName: 'Crosses completed / 90', attributeName: 'Cr_c_90' },
        { displayName: 'Crosses completion ratio', attributeName: 'Cr_c_acc' },
        { displayName: 'Chances created / 90', attributeName: 'Ch_c_90' },
        { displayName: 'Possesion lost / 90', attributeName: 'Poss_lost_90' }
    ],
    attacking: [
        { displayName: 'Goals', attributeName: 'Goal' },
        { displayName: 'Expected Goals', attributeName: 'xG' },
        { displayName: 'Goals / 90', attributeName: 'Gol_90' },
        { displayName: 'Dribbles / 90', attributeName: 'Drb_90' },
        { displayName: 'Shots on Target Ratio', attributeName: 'Shot_rat' },
        { displayName: 'Conversion Ratio', attributeName: 'Conv_rat' },
        { displayName: 'Fouls Received', attributeName: 'Faga' }
    ]
};




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
        dot.classList.toggle('activated'); // Toggle dot activation
        console.log('Activated dots:', document.querySelectorAll('.activated'));
    }

    // Add dots when the page is loaded
    addDots();

    // Add event listeners for dot clicks
    document.querySelectorAll('.player-position-dot').forEach(dot => {
        dot.addEventListener('click', function() {
            handleDotClick(dot);
        });
    });

    window.addEventListener('resize', function() {
        addDots();
    });

    const filterTypeSelect = document.getElementById("filter-type");
    const filterValueInput = document.getElementById("filter-value");

    // Function to update filter value input type
    function updateFilterValueType() {
        const selectedType = filterTypeSelect.value;
        filterValueInput.type = selectedType === "contains" ? "text" : "number";
    }

    // Call the function initially and whenever the filter type changes
    updateFilterValueType();
    filterTypeSelect.addEventListener("change", updateFilterValueType);


    // Function to handle filter category
    function populateFilterProperties(category) {
        const filterPropertySelect = document.getElementById('filter-property');
        filterPropertySelect.innerHTML = ''; // Clear previous options

        // Find the category in the fieldCategories object
        const categoryFields = fieldCategories[category];
        categoryFields.forEach(field => {
            const option = document.createElement('option');
            option.value = field.attributeName; // Use attribute name as value
            option.textContent = field.displayName; // Use display name as text content
            filterPropertySelect.appendChild(option);
        });
    }

    // Function to handle filter menu visibility
    document.getElementById('add-filter-btn').addEventListener('click', function() {
        const filterMenu = document.getElementById('filter-menu');
        filterMenu.style.display = filterMenu.style.display === 'block' ? 'none' : 'block';

        // Manually trigger the change event to populate filter properties for the default category
        if (filterMenu.style.display === 'block') {
            const selectedCategory = document.getElementById('filter-category').value;
            populateFilterProperties(selectedCategory);
        }
    });

    // Populate filter properties based on selected category
    document.getElementById('filter-category').addEventListener('change', function() {
        const selectedCategory = this.value;
        populateFilterProperties(selectedCategory);
    });

    // Function to handle applying filters
    document.getElementById('apply-filter-btn').addEventListener('click', function() {
        const filterType = document.getElementById('filter-type').value;
        const filterProperty = document.getElementById('filter-property').value;
        const filterValue = document.getElementById('filter-value').value;
        const appliedFilters = document.getElementById('applied-filters');
        // Create filter element
        const filterElement = document.createElement('div');
        filterElement.classList.add('filter-item'); // Add a class for styling
        filterElement.textContent = `${filterProperty} ${filterType} ${filterValue}`;
        appliedFilters.appendChild(filterElement);
    });

    // Function to handle search button click
    document.getElementById('adv-search-btn').addEventListener('click', function() {
        // Get activated dots
        const activatedDots = document.querySelectorAll('.activated');
        // Get positions corresponding to activated dots
        const selectedPositions = Array.from(activatedDots).map(dot => {
            // Retrieve the position stored in the dot's position property
            return dot.position;
        });
    
        // Get applied filters  
        const appliedFilters = document.getElementById('applied-filters').children;
        const filters = Array.from(appliedFilters).map(filterElement => {
            // Split the text content of the filter element into its components
            const [property, type, value] = filterElement.textContent.trim().split(' ');
            return { property, type, value };
        });
    
        // Construct the query parameters string
        const params = new URLSearchParams({
            selectedPositions: selectedPositions.join(','), // Convert array to comma-separated string
            filters: JSON.stringify(filters) // Convert filters array to JSON string
        });
    
        // Send GET request to the server
        fetch('/advanced_search/?' + params, {
            method: 'GET'
        })
        .then(response =>  window.location.href = response.url) //redirect to url with params
        .catch(error => {
            console.error('Error:', error);
        });
    });
    

})