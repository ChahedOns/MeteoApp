import json
import time
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers=['pkc-03vj5.europe-west8.gcp.confluent.cloud:9092'],
                         sasl_mechanism='PLAIN',
                         security_protocol='SASL_SSL',
                         sasl_plain_username='EEVMZ6X54FESIITW',
                         sasl_plain_password='SoeBfjdTAm/MhA06GQzm5B77+1c2+RLlymtwtohuSaRXXIhDAF55NGT3Ejj9ukG/',
                         api_version=(2, 7, 0))

def get_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def produce_weather_data(topic, weather_data):
    # Convert dictionary to JSON string
    json_str = json.dumps(weather_data)
    # Encode JSON string as bytes
    value_bytes = json_str.encode('utf-8')
    # Send data to Kafka topic
    producer.send(topic, value=value_bytes)
    producer.flush()
    print(f'Sent data to topic "{topic}": {weather_data}')

while True:
    weather_data = get_weather_data('e1d249091bc4e5afc3580b698bdecc7c', 'london')
    if weather_data is not None:
        produce_weather_data('meteo1', weather_data)
        print('Weather data produced to Kafka topic.')
    else:
        print('Error retrieving weather data.')
    time.sleep(10) # sleep for 5 minutes