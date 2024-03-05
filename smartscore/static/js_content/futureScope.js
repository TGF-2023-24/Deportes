document.addEventListener('DOMContentLoaded', function() {
    console.log('Future Scope page loaded');
    const countrySelect = document.getElementById('country-select');
    const leagueSelect = document.getElementById('league-select');
    console.log('Country Select:', countrySelect);
    console.log('League Select:', leagueSelect);
    // Function to populate leagues based on selected countryy
    function populateLeagues(selectedCountry) {
        const leagueSelect = document.getElementById('league-select');
        leagueSelect.removeAttribute('disabled'); // Enable league selection

        const leagueOptions = leagueSelect.querySelectorAll('option');
        if (selectedCountry != ''){
            // Clear current selection
            leagueSelect.selectedIndex = -1;
        }
        
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
    }


    // Add event listener to the country selection dropdown
    countrySelect.addEventListener('change', function() {
        console.log('Country selected:', this.value);
        const selectedCountry = this.value;
        populateLeagues(selectedCountry);
    });

    // Populate leagues initially (in case there is a pre-selected country)
    populateLeagues(countrySelect.value);

    const transferBudget = document.getElementById('transfer-budget');
    transferBudget.addEventListener('input', function() {
        if (this.value.length > 4) {
            this.value = this.value.slice(0, 4); // Limit input to four digits
        }
    });
    

    // Add event listener to the form submission
    const futureScopeForm = document.getElementById('future-scope-form');
    futureScopeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const transferBudget = document.getElementById('transfer-budget').value;
        const selectedLeague = document.getElementById('league-select').value;
        const selectedExpectations = document.getElementById('expectations').value;
        console.log('Submitting form with Transfer Budget:', transferBudget);
        console.log('Selected League:', selectedLeague);
        console.log('Selected Expectations:', selectedExpectations);
        saveFutureScopeSettings(transferBudget, selectedLeague, selectedExpectations);
    });
});

function saveFutureScopeSettings(transferBudget, selectedLeague, selectedExpectations) {
    fetch('/api/save-futureScope/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            transfer_budget: transferBudget,
            selected_league: selectedLeague,
            selected_expectations: selectedExpectations
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to save future scope settings');
        }
        return response.json();
    })
    .then(data => {
        console.log('Future scope settings saved:', data);
        // Handle success (e.g., display success message to user)
        window.location.reload(); // Reload the page

    })
    .catch(error => {
        console.error('Error saving future scope settings:', error);
        // Handle error (e.g., display error message to user)
    });
}

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
