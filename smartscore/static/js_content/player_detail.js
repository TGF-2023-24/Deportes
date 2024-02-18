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
        '400px,425px': 'MR',
        '250px,250px': 'AMC',
        '250px,75px': 'AML',
        '250px,425px': 'AMR',
        '125px,250px': 'STC'
    };




    // Function to create the initial radar chart
    function createInitialRadarChart() {
        var ctx = document.getElementById('radarChart').getContext('2d');
        radarChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['', ' ', ' ', ' ', ' ', ' '],
                datasets: [{
                    label: player_name,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scale: {
                    ticks: {
                        min: 0,  // Set the minimum value of the scale
                        max: 100,  // Set the maximum value of the scale
                    }
                }
            }
        });
    }

    createInitialRadarChart();

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
         fetch(`/api/position-stats/${position}/${custom_id}`)
         .then(response => response.json())
         .then(data => {
             console.log(data);

              // Update the UI to display the stats for the clicked position
              document.getElementById('avg_stats_title').innerHTML = `
              <h3>Avg stats for: ${position}</h3>
            `;
            
            let statsHTML = ''; 
            let normalizedStats = []; // Array to store normalized stats
            let normalizedPlayerValues = []; // Object to store normalized player values

            for (const [key, value] of Object.entries(data[position])) {
                normalized_avg = (100 * (value.avg - value.min) / (value.max - value.min)).toFixed(2);
                statsHTML += `<li>${key}: ${normalized_avg}</li>`;
                normalizedStats[key] = normalized_avg; // Store normalized stats in an array
                normalizedPlayerValues.push((100 * (data[player_name][key] - value.min) / (value.max - value.min)).toFixed(2));
            }

            console.log(normalizedStats);
            document.getElementById('avg_stats').innerHTML = statsHTML;

            // Clean all datasets from radar chart and add player stats
            radarChart.data.datasets.splice(0);

            const keys = Object.keys(data[player_name]);

            // Add a new dataset with the data from the fetched position
            radarChart.data.datasets.push({
                label: player_name + ' Stats',
                data: normalizedPlayerValues,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            });
            radarChart.data.labels = keys; // Assuming keys contains the labels
            addDatasetToRadarChart(normalizedStats, position);
            
         })
         .catch(error => {
             console.error('Error fetching position stats:', error);
         });
    }

    function addDatasetToRadarChart(statsData, position) {
        // Clear existing datasets
        radarChart.data.datasets.splice(1);
    
        const values = Object.values(statsData);
        // Add a new dataset with the data from the fetched position
        radarChart.data.datasets.push({
            label: 'Avg ' + position + ' Stats',
            data: values,
            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Change color if needed
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        });

    
        // Update the chart
        radarChart.update();
    }

    // Get player surname to display
    var playerNameElement = document.getElementById('player-name');
    var nameParts = playerNameElement.textContent.split(' ');
    var lastName = nameParts[nameParts.length - 1];
    playerNameElement.textContent = lastName;

    
});
