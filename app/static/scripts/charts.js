let temperatureChart; 
const searchCity = document.getElementById('searchCity');
searchCity.addEventListener('input', () => {
  const city = searchCity.value.trim(); // Trim whitespace from input
  if (city === '') {
    return; // Exit early if no city input
  }
  // const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
  // const apiUrl = `${proxyUrl}weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${city}?unitGroup=us&key=NBRQYJ66AF3C6NLHLBJZ3SDYT&contentType=json`;
  fetch(`/weather?city=${city}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Extract data for plotting
      const labels = data.days.map((day, index) => `Day ${index + 1}`);
      const maxTemperatures = data.days.map(day => day.tempmax);
      const minTemperatures = data.days.map(day => day.tempmin);
      const humidities = data.days.map(day => day.humidity);
      const precipitations = data.days.map(day => day.precip);
      const windspeeds = data.days.map(day => day.windspeed);
      const pressures = data.days.map(day => day.pressure);
      const sunrises = data.days.map(day => day.sunrise);
      const sunsets = data.days.map(day => day.sunset);

      // Update the chart with the new data
      const ctx = document.getElementById('weatherChart');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Max Temperature (°F)',
              borderColor: 'rgba(255, 99, 132, 1)',
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              data: maxTemperatures,
              yAxisID: 'temperatureAxis',
            },
            {
              label: 'Min Temperature (°F)',
              borderColor: 'rgba(54, 162, 235, 1)',
              backgroundColor: 'rgba(54, 162, 235, 0.2)',
              data: minTemperatures,
              yAxisID: 'temperatureAxis',
            },
            {
              label: 'Humidity (%)',
              borderColor: 'rgba(255, 206, 86, 1)',
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
              data: humidities,
              yAxisID: 'humidityAxis',
            },
            {
              label: 'Precipitation (in)',
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              data: precipitations,
              yAxisID: 'precipitationAxis',
            },
            {
              label: 'Wind Speed (mph)',
              borderColor: 'rgba(153, 102, 255, 1)',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              data: windspeeds,
              yAxisID: 'windSpeedAxis',
            },
            {
              label: 'Pressure (mb)',
              borderColor: 'rgba(255, 159, 64, 1)',
              backgroundColor: 'rgba(255, 159, 64, 0.2)',
              data: pressures,
              yAxisID: 'pressureAxis',
            },
            {
              label: 'Sunrise',
              borderColor: 'rgba(255,156,67,8)',
              backgroundColor: 'rgba(234,56,25,67)',
              data:  sunrises,
              yAxisID: 'sunriseAxis',
            },
            {
             label: 'Sunrise',
             borderColor: 'rgba(134, 234, 67, 8)',
             backgroundColor: 'rgba(153, 102, 255, 0.2)',
             data : sunsets,
            yAxisID: "sunsetAxis",

            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: `Weather Forecast for ${data.resolvedAddress}`,
            },
          },
          scales: {
            x: {
              display: true,
              title: {
                display: true,
                text: 'Day',
              },
            },
            y: {
              position: 'left',
              title: {
                display: true,
                text: 'Temperature (°F)',
              },
              id: 'temperatureAxis',
              ticks: {
                beginAtZero: true,
              },
            },
            humidityAxis: {
              position: 'right',
              title: {
                display: true,
                text: 'Humidity (%)',
              },
              ticks: {
                beginAtZero: true,
              },
            },
            precipitationAxis: {
              position: 'right',
              title: {
                display: true,
                text: 'Precipitation (in)',
              },
              ticks: {
                beginAtZero: true,
              },
            },
            windSpeedAxis: {
              position: 'right',
              title: {
                display: true,
                text: 'Wind Speed (mph)',
              },
              ticks: {
                beginAtZero: true,
              },
            },
            pressureAxis: {
              position: 'right',
              title: {
                display: true,
                text: 'Pressure (mb)',
              },
              ticks: {
                beginAtZero: true,
              },
            },
            sunriseAxis: {
              position: 'right',
              title: {
                display: true,
                text: 'Pressure (mb)',
              },
              ticks: {
                beginAtZero: true,
              },
            },
            sunsetAxis: {
              position: 'right',
              title: {
                display: true,
                text: 'Pressure (mb)',
              },
              ticks: {
                beginAtZero: true,
              },
            },
          },
        },
      });
    })
    .catch(error => {
      console.error('Error fetching or parsing data:', error);
      // Optionally display an error message to the user
    });
});