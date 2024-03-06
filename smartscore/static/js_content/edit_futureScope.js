document.addEventListener('DOMContentLoaded', function() {
    console.log('Future Scope page loaded');
    const countrySelect = document.querySelector('.country-select');
    const leagueSelect = document.getElementById('.league-select');
    
    // Function to populate leagues based on selected country
    function populateLeagues(selectedCountry, selectedLeague) {
        console.log('Populating leagues for country:', selectedCountry, 'and league:', selectedLeague);
        const leagueOptions = leagueSelect.querySelectorAll('option');
        
        // Clear current selection
        leagueSelect.selectedIndex = -1;
        
        // Show all leagues if no country is selected
        if (!selectedCountry) {
            leagueOptions.forEach(option => {
                option.style.display = '';
            });
            return;
        }

        // Hide leagues that do not belong to the selected country
        leagueOptions.forEach(option => {
            const leagueCountry = option.getAttribute('data-country');
            if (leagueCountry !== selectedCountry) {
                option.style.display = 'none';
            } else {
                option.style.display = '';
            }
        });

        // Set the initial league value if available
        if (selectedLeague) {
            leagueSelect.value = selectedLeague;
        }
    }

    // Add event listener to the country selection dropdown
    countrySelect.addEventListener('change', function() {
        console.log('Country selected:', this.value);
        const selectedCountry = this.value;
        const selectedLeague = leagueSelect.value; // Get the current league value
        populateLeagues(selectedCountry, selectedLeague); // Pass both country and league values
    });

    // Populate leagues initially (in case there is a pre-selected country and league)
    populateLeagues(countrySelect.value, leagueSelect.value);
});
