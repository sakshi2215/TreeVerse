async function getWeather(cityInputValue) {
  var apiKey = "NBRQYJ66AF3C6NLHLBJZ3SDYT"; // Ensure this is your correct API key
  var unit = "metric";
  var apiUrl = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${city}?unitGroup=us&key=NBRQYJ66AF3C6NLHLBJZ3SDYT&contentType=json`;

  try {
    var response = await fetch(apiUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    var data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("Error fetching weather data:", error);
  }
}

// Example usage
var city = "London";
getWeather(city);
