import time
from flask import Flask, Blueprint, session, make_response, request, jsonify
from config import db_name, user_pwd,user_db
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import current_user, login_required, login_user, logout_user, UserMixin,LoginManager
from config import api_key, secret_key
import json
from json import loads
import requests
from werkzeug.security import check_password_hash
import re
from wtforms import ValidationError
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from kafka import KafkaProducer ,KafkaConsumer
from confluent_kafka import Consumer
import requests
import threading


# configurations !
app = Flask(__name__)
DB_URI ="mongodb+srv://admin:adminadmin@cluster0.ad4hkct.mongodb.net/MeteoApp?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
app.config['SECRET_KEY'] = secret_key


app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='localhost',
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=None,
    MAIL_PASSWORD=None,
))
#Database setup
db = MongoEngine()
db.init_app(app)
#Blueprint setup
routes_BP= Blueprint('routes', __name__)
app.register_blueprint(routes_BP)
# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
#schedular Setting : the one that will check the weather data frecuntly!
# initialize scheduler
SCHEDULER_API_ENABLED = True
SCHEDULER_TIMEZONE = "Europe/Berlin"
scheduler = BackgroundScheduler()
scheduler.start()
trigger = CronTrigger( year="*", month="*", day="*", hour="*", minute="2", second="5")


# Needed functions


def safe_string():
    """Validates that the field matches some safe requirements
    Used to make sure our user's username is safe and readable
    Requirements:
    - contains only letters, numbers, dashes and underscores
    """

    def validation(form, field):
        string = field.data.lower()
        pattern = re.compile(r"^[a-z0-9_-]+$")
        match = pattern.match(string)
        if not match:
            message = "Must contain only letters, numbers, dashes and underscores."
            raise ValidationError(message)

    return validation


def unique_or_current_user_field(message=None):
    """Validates that a field is either equal to user's current field
    or doesn't exist in the database
    Used for username and email fields
    """

    def validation(form, field):
        kwargs = {field.name: field.data}
        if (
            hasattr(current_user, field.name)
            and getattr(current_user, field.name) == field.data
        ):
            return
        if User.objects(**kwargs).first():
            raise ValidationError(message)

    return validation

def get_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_forcast_data(api_key,lat,lon):
    url = f"api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
def get_city_data(api_key,city):
    url= f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

#Documents definitions

class User(db.Document, UserMixin):
    id = db.IntField(primary_key=True)
    mail = db.StringField(required=True)
    pwd= db.StringField(required=True)
    name = db.StringField()
    birth_date = db.DateTimeField()
    location=db.StringField(required=True)
    cities = db.ListField(db.StringField())
    def to_json(self):
        return {
            "ID": self.id,
            "Mail":self.mail,
            "Name":self.name,
            "Birthday":self.birth_date,
            "Location":self.location,
        }
    def check_password(self, password):
        """Checks that the pw provided hashes to the stored pw hash value"""
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
            """Define what is printed for the user object"""
            return f"Username: {self.username} id: {self.id}"
    
class Place(db.Document):
    name=db.StringField(required=True)
    lat=db.FloatField()
    lon=db.FloatField()

    def to_json(self):
        return{
            "Name": self.name,
            "Lat":self.lat,
            "Lon":self.lon
        }

class Weather(db.Document):
    data=db.DictField()
    date=db.DateField(default=datetime.datetime.now())
    city=db.StringField()
    def to_json(self):
        return{
            "Data": self.data,
            "Date":self.date,
            "City":self.city
        }


class Notification(db.Document):
    user_id=db.IntField()
    msg=db.StringField()
    location=db.StringField()
    date=db.DateField(default=datetime.datetime.today())

# App Routers
# needed user id later in the notifications system!

@app.route("/cities", methods=['POST', 'GET'])
def get_places():
    if request.method == 'GET':
        Ls = []
        for r in Place.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun cite dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les cites sont : ", Ls), 200)
    
@app.route("/weather", methods=['POST', 'GET'])
def set_weather():
    if request.method == "POST":
        data= get_weather_data(api_key , request.form.get("city"))
        w= Weather(data=data,city=request.form.get("city"))
        #Check if the place exist in our data base! 
        p = Place.objects(name=request.form.get("city")).first()
        if p == None:
            p=Place(name=request.form.get("city"),lat=float(data["coord"]["lat"]),lon=float(data["coord"]["lon"]))
            p.save() 
        w.save()
        return make_response(jsonify("le meteo de la ville ",request.form.get("city"),"est : ", data), 200)
    else :  
        Ls = []
        for r in Weather.objects(city=request.form.get("city")):
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun meteo sauvgardées dans le systéme!", 201)
        else:
            return make_response(jsonify("les meteos sauvgardées sont : ", Ls), 200)

@login_required
@app.route("/historique", methods=['GET'])
def get_history():
    city = request.form.get("city")
    E = Weather.objects(city=city)
    if E == "None":
        return make_response("Aucun Meteo sauvgardée pour cette ville", 201)
    else:
        return make_response(jsonify("L'Historique de météo de",city,"est : \n",E), 200)

@login_required
@app.route("/forcast",methods=["get"])
def get_forcast():
    city=request.form.get("city")
    p= Place.objects(name=city).first()
    if p == "None":
        data= get_weather_data(api_key , city)
        w= Weather(data=data,city=request.form.get("city"))
        p=Place(name=request.form.get("city"),lat=float(data["coord"]["lat"]),lon=float(data["coord"]["lon"]))
        p.save() 
        w.save()
        forcast_data= get_forcast_data(api_key,float(data["coord"]["lat"]),float(data["coord"]["lon"]))
        return make_response(jsonify("forcast de la ville  ",city,"est : ", forcast_data), 200)
    else:
        lat=p.lat
        lon =p.lon
        forcast_data= get_forcast_data(api_key,lat,lon)
        return make_response(jsonify("forcast de la ville  ",city,"est : ", forcast_data), 200)

@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        mail = request.form.get("mail")
        name = request.form.get("name")
        pwd = request.form.get("pwd")
        birth_date = request.form.get("birth_date")
        location = request.form.get("location")
        cities = request.form.get("cities").split(':')  # split the : separated list into a Python list --> city1:city2:city3....
        existing_user = User.objects(mail=mail).first()
        if existing_user is None:
            if not get_city_data(api_key,location):#verification si location saisi par user est valide ou non
                return make_response("location invalide", 201)
            
            for c in cities:
                if not get_city_data(api_key,c):
                    return make_response("location invalide", 201)
                
            hashpass = generate_password_hash(pwd, method='sha256')
            v = User(mail=mail,pwd=hashpass,name=name,birth_date=birth_date,location=location, cities=cities)
            max_id = 0      #assign an id to the user
            for u in User.objects:
                if u.id > max_id:
                    max_id = u.id
            v.id = max_id + 1
            v.save()
            return make_response("Bienvenue à MeteoApp", 200)
        else:
            return make_response("Compte existant", 201)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first

@app.route('/login', methods=['POST'])
def login():
    logout_user()
    mail = request.form.get("mail")
    pwd = request.form.get("pwd")
    check_user = User.objects(mail=mail).first()
    if not check_user:
        return make_response("Mail invalide", 201)

    # Vérifier que le mot de passe est correct
    if not check_password_hash(check_user['pwd'], pwd):
        return make_response("Mot de passe invalide", 201)

    # Set session data
    session['user_id'] = check_user['id']

    login_user(check_user)
    return make_response("logged In successfully!", 200)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    # Remove session data
    session.pop('user_id', None)
    return make_response("Logged out!", 200)   

@app.route('/profile', methods=['POST'])
def profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        return "<h1>Vous n'êtes pas connecté</h1>"

    # Load the user's data from the database
    user = User.objects(id=session['user_id']).first()

    # Display the user's profile page
    return f"<h1>Bonjour, {user.name}!</h1>"  

@login_required
@app.route('/notifications',methods=['GET'])
def get_notif():
    E = Notification.objects()
    if E == "None":
        return make_response("Aucune Notification sauvgardée pour cet utilisateur", 201)
    else:
        return make_response(jsonify("Les notifications sont : \n",E), 200)

# *********************************** KAFKA ************************
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('utf-8'),bootstrap_servers=['pkc-4r297.europe-west1.gcp.confluent.cloud:9092'],
                        sasl_mechanism='PLAIN',
                        security_protocol='SASL_SSL',
                        sasl_plain_username='W2W37CHYQAEEQ55R',
                        sasl_plain_password='QhTHq8ufGEqiNZGfUaJVeVkc6FUtCV8zYj8zY7RFrtlVGSE/BnCshVnEBbGyXPX1',
                        api_version=(2, 7, 0))
consumer = KafkaConsumer ('Check_notif', group_id = 'group1',bootstrap_servers = ['pkc-4r297.europe-west1.gcp.confluent.cloud:9092'],
sasl_mechanism='PLAIN',security_protocol='SASL_SSL',sasl_plain_username='W2W37CHYQAEEQ55R',
sasl_plain_password='QhTHq8ufGEqiNZGfUaJVeVkc6FUtCV8zYj8zY7RFrtlVGSE/BnCshVnEBbGyXPX1',auto_offset_reset = 'earliest',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe(['Check_notif'])

def produce_weather_data(topic, msg ,location):
    # Convert data to dictionary
    data={"msg":msg, "location":location}
    # Send data to Kafka topic
    producer.send(topic, value=data)
    producer.flush()
    print(f'Sent data to topic "{topic}": {msg} , {location}')

def check_changes():
    while True:
        ps= Place.objects()
        for p in ps:
            weather_data = get_weather_data(api_key, p.name)
            if weather_data is not None:
                #Prepare the msg! 
                weatherStatus= weather_data["weather"][0]["main"]
                if weatherStatus == "snow":
                    msg = "Snowy Day Alert !Stay at home, drink something warm! Snowy Day!"
                elif weatherStatus == "rain" or weatherStatus=="shower rain" or weatherStatus=="thunderstorm":
                    msg = "Rainy Day Alert !Don't forget your umbrella! it may rains today!"
                elif weatherStatus == "mist":
                    msg = "Becareful and drive slowly today!"
                elif weatherStatus== "clouds":
                    msg="Grey Day Alert It may be a sad weather today! Be productive"
                else:
                    msg=weatherStatus
                #Check the last notification on that location!
                last_notif = Notification.objects(date=datetime.date.today(),location=p.name).first()

                if last_notif is not None:
                    if msg != last_notif.msg:
                        #Sending new notifiction with changes
                        print("Detecting changes!")
                        produce_weather_data('Check_notif',msg,p.name)
                else:
                    #Produce new notification! 
                    produce_weather_data('Check_notif',msg,p.name)
            else:
                print('Error retrieving weather data.')
        time.sleep(15)
#launch the producer and consumer ! 
"""while True:
    check_changes()
    time.sleep(15)"""
def consume_notification():
    try:
        while True:
            print("Listening")
            for message in consumer:
                # read single message at a time
                if message is None:
                    print("msg vide")
                else:
                # You can parse message and save to data base here
                    users= User.objects(location=message.value["location"])
                    for u in users:
                        n=Notification(user_id=u.id,msg=message.value["msg"],location=message.value["location"])
                        n.save()
            consumer.commit()
            time.sleep(1)
    except Exception as ex:
        print(f"Kafka Exception : { ex}")

    finally:
        print("closing consumer")
        consumer.close()


if __name__ == '__main__':
    

    # start the producer in a separate thread
    producer_thread = threading.Thread(target=check_changes)
    producer_thread.start()

    consumer_thread = threading.Thread(target=consume_notification)
    consumer_thread.start()

    # start the Flask application
    app.run()