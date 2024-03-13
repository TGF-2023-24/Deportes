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

            
            let statsHTML = ''; 
            let normalizedStats = []; // Array to store normalized stats
            let normalizedPlayerValues = []; // Object to store normalized player values

            for (const [key, value] of Object.entries(data[position])) {
                normalized_avg = (100 * (value.avg - value.min) / (value.max - value.min)).toFixed(2);
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

        fetch(`/api/player-smartscore/${position}/${custom_id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const smartScoreDisplay = document.getElementById('smartScoreDisplay');
            if (data && data.smartscore !== undefined) {
                const smartscoreBubble = document.getElementById('smartScoreDisplay');
                smartscoreBubble.setAttribute('data-smartscore', data.smartscore);
                smartScoreDisplay.textContent = data.smartscore.toFixed();
                updateBubbleColor(data.smartscore);
            } else {
                smartScoreDisplay.textContent = '--';
                console.error('Invalid data received from the API:', data);
            }
        })
        .catch(error => {
            console.error('Error fetching player smartscore:', error);
        });
    
    function updateBubbleColor(smartscore) {
        const smartscoreBubble = document.getElementById('smartScoreDisplay');
        smartscoreBubble.style.backgroundColor = testColorGradient(smartscore);
    }
    
    
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
    nameForSearch = playerNameElement.textContent;
    var nameParts = playerNameElement.textContent.split(' ');
    var lastName = nameParts[nameParts.length - 1];
    playerNameElement.textContent = lastName;

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
    
});
