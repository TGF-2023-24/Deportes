document.addEventListener('DOMContentLoaded', function() {
    const futureScopeForm = document.getElementById('future-scope-form');
    futureScopeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const transferBudget = document.getElementById('transfer-budget').value;
        const selectedLeague = document.getElementById('league').value;
        const selectedExpectations = document.getElementById('expectations').value;
        saveFutureScopeSettings(transferBudget, selectedLeague, selectedExpectations);
    });


    // Fetch leagues
    const leagueSelect = document.getElementById('league');

    // Fetch leagues data from the server
    fetch('/api/leagues/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch leagues data');
            }
            return response.json();
        })
        .then(data => {
            populateLeagues(data);
        })
        .catch(error => {
            console.error('Error fetching leagues data:', error);
        });

    function populateLeagues(leaguesData) {
        // Clear existing options
        leagueSelect.innerHTML = '';

        // Iterate over league countries
        for (const country in leaguesData) {
            if (leaguesData.hasOwnProperty(country)) {
                // Create optgroup for each country
                const optgroup = document.createElement('optgroup');
                optgroup.label = country;

                // Iterate over leagues in the country
                leaguesData[country].forEach(league => {
                    const option = document.createElement('option');
                    option.value = league.id;
                    option.textContent = league.name;
                    optgroup.appendChild(option);
                });

                leagueSelect.appendChild(optgroup);
            }
        }
    }
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
