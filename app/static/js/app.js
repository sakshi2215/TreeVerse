console.log("Script is running!");

document.addEventListener('DOMContentLoaded', () => {
  const getWeatherButton = document.getElementById('get-weather');
  const locationInput = document.getElementById('location');
  const currentWeatherDiv = document.getElementById('current-weather');
  const weatherDiv = document.getElementById('weather');

  getWeatherButton.addEventListener('click', async () => {
    const location = locationInput.value;

    if (!location) {
      alert('Please enter a location.');
      return;
    }

    try {
      // Fetch current weather data from OpenWeather API
      const currentWeatherData = await fetch(`https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${locations}/last15days?elements=datetime%2CdatetimeEpoch%2Ctemp%2Ctempmax%2Ctempmin%2Cprecip%2Cwindspeed%2Cwindgust%2Cfeelslike%2Cfeelslikemax%2Cfeelslikemin%2Cpressure%2Cstations%2Cdegreedays%2Caccdegreedays&include=fcst%2Cobs%2Chistfcst%2Cstats%2Ccurrent%2Cdays%2Chours&key={""}&contentType=json`);
      // const currentWeatherData = await currentWeatherResponse.json();

      console.log('Current Weather Data:', currentWeatherData);

      // Check if current weather data is valid
      if (currentWeatherData.cod !== 200) {
        alert('Error fetching current weather data. Please check the location.');
        return;
      }

     

      // Display current weather
      currentWeatherDiv.innerHTML = `
        <p>Temperature: ${currentWeatherData.main.temp}°F</p>
        <p>Humidity: ${currentWeatherData.main.humidity}%</p>
        <p>Weather: ${currentWeatherData.weather[0].description}</p>
      `;


      // Show weather information
      weatherDiv.style.display = 'block';
    } catch (error) {
      alert('An error occurred while fetching weather data.');
      console.error(error);
    }
  });
});
