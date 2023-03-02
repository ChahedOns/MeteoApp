import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True



@app.route('/', methods=['GET', 'POST'])
def index():

    new_city = 'tunis'
    if request.method == 'POST':
        new_city = request.form.get('city')
        
        

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c55e67cedaed247dc52b01d6d84b7783'

    weather_data = []

    

    r = requests.get(url.format(new_city)).json()

    weather = {
            'city' : new_city ,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

    weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)