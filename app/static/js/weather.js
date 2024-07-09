const apiKey = 'NBRQYJ66AF3C6NLHLBJZ3SDYT' // this app uses the free tier of OpenWeather API, so to use this app, simply sign up for the free tier and enter the api key. (I deleted the original script.js file and replaced it with this one because I realized that I exposed my API key in the old one.)
let futureTempTime = new Array(7).fill(0)
let futureTemp = new Array(7).fill(0)
function usTime(x) {
    if (x == 0o0 ){
        return 12 + ' AM'
    } else if (x < 12) {
       return `${x.charAt(1)} AM`
    } else if (x == 12) {
        return `${x} PM`
    } else if (x > 12) {
        return `${x-12} PM`
    } else if (x == 24) {
        return `${x-12} AM`
    }
}

window.addEventListener('load', ()=> {
    navigator.geolocation.getCurrentPosition(position => {
        let lat = position.coords.latitude
        let long = position.coords.longitude
        console.log("Latitude: " + lat)
        console.log("Longitude: " + long)

        let currentWeatherApi = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${apiKey}&units=imperial`
        console.log(currentWeatherApi)
        fetch(currentWeatherApi)
            .then(response => {
                return response.json()
            })
            .then(data => {
                console.log(data)
                let currentTemp = document.getElementById('currentTemp')           
                let currentWeather = document.getElementById('currentWeather')   
                let currentWeatherText = `${data.weather[0].description.charAt(0).toUpperCase()}${data.weather[0].description.slice(1,data.weather[0].description.length)}`
                let weatherIcon = document.getElementById('weatherIcon')
                currentTemp.innerText = `The current temperature is: ${data.main.temp}°F`
                currentWeather.innerText = `The current weather is: ${currentWeatherText}`
                weatherIcon.src = `weather_icons/${data.weather[0].icon}.png`
            })
        let futureWeatherApi = `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${long}&appid=${apiKey}&units=imperial`
        fetch(futureWeatherApi)
            .then(response => {
                return response.json()
            })
            .then(data => {
                console.log(data)
                for (let i=0; i<=6; i++) {
                    futureTempTime[i] = usTime(data.list[i].dt_txt.slice(11,13))
                    futureTemp[i] = data.list[i].main.temp
                    chart.update()
                }
            }) 
    })
})

const weatherGraph = document.getElementById('weatherGraph')
const chart = new Chart(weatherGraph, {
    type: 'line',
    data: {
        labels: futureTempTime,
        datasets: [{
            label: 'Temperature (°F)',
            data: futureTemp,
            borderWidth: 2,
            lineTension: 0.3,
            responsive: true,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    },
})