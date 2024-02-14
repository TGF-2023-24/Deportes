document.addEventListener('DOMContentLoaded', function() {
    var dots = document.querySelectorAll('.player-position-dot');
    var activatedDot = null;

    // Position mapping
    const positionMapping = {
        '750px,250px': 'GK',
        '650px,250px': 'DC',
        '650px,75px': 'DL',
        '650px,425px': 'DR',
        '525px,250px': 'DM',
        '525px,75px': 'WBL',
        '525px,425px': 'WBR',
        '400px,250px': 'MC',
        '400px,75px': 'ML',
        '400px,425px': 'MD',
        '250px,250px': 'AMC',
        '250px,75px': 'AML',
        '250px,425px': 'AMR',
        '125px,250px': 'STC'
    };

    // Function to create the initial radar chart
    function createInitialRadarChart(playerStats) {
        var ctx = document.getElementById('radarChart').getContext('2d');
        radarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Goal', 'Curr ability', 'Poss lost', 'Penalty saved'],
                datasets: [{
                    label: 'Player Stats',
                    data: [playerStats.Goal, playerStats.CAbil, playerStats.Poss_lost_90, playerStats.Penalty_sav],
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
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

    createInitialRadarChart(initialPlayerStats);

    // Add event listener for dot click
    dots.forEach(function(dot) {
        dot.addEventListener('click', function() {
            handleDotClick(dot);
        });
    });

    // Function to handle dot click
    function handleDotClick(clickedDot) {
        // Deactivate previously activated dot
        if (activatedDot !== null) {
            activatedDot.classList.remove('activated');
        }

        // Activate the clicked dot
        clickedDot.classList.add('activated');
        activatedDot = clickedDot;

        // Get the CSS styles of the clicked dot
        var top = clickedDot.style.top;
        var left = clickedDot.style.left;
        var position = positionMapping[`${top},${left}`];

        console.log('Activated dot:', position);

         // Send an AJAX request to fetch stats for the clicked position
         fetch(`/api/position-stats/${position}/`)
         .then(response => response.json())
         .then(data => {
             console.log(data);
              // Update the UI to display the stats for the clicked position
              document.getElementById('avg_stats_title').innerHTML = `
                <h3>Avg stats for: ${position}</h3>
            `;
              document.getElementById('avg_stats').innerHTML = `
              <li>Goal: ${data[position].Goal}</li>
              <li>Curr ability: ${data[position].CAbil}</li>
              <li>Poss lost: ${data[position].Poss_lost_90}</li>
              <li>Penalty saved: ${data[position].Penalty_sav}</li>
            `;

            addDatasetToRadarChart(data[position], position);

            
         })
         .catch(error => {
             console.error('Error fetching position stats:', error);
         });
    }

    // Function to add a new dataset to the radar chart
    function addDatasetToRadarChart(statsData, position) {
        //Clear existing datasets
        radarChart.data.datasets.splice(1);
        // Add a new dataset with the data from the fetched position
        radarChart.data.datasets.push({
            label: position + ' Stats',
            data: [statsData.Goal, statsData.CAbil, statsData.Poss_lost_90, statsData.Penalty_sav],
            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Change color if needed
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        });

        // Update the chart
        radarChart.update();
    }

    
});
