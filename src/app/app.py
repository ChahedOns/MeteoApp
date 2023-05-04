import time
from flask import Flask, Blueprint, session, make_response, request, jsonify
from config import db_name, user_pwd,user_db
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import current_user, login_required, login_user, logout_user, UserMixin,LoginManager
from config import api_key, secret_key
import json
import requests
from werkzeug.security import check_password_hash
import datetime
from kafka import KafkaProducer ,KafkaConsumer
from flask_cors import CORS
import requests
import threading
from datetime import datetime as dt

# configurations !
app = Flask(__name__)
CORS(app)
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

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)

# Needed functions

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
    url= f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
def get_city_history(lat, lon, start_date, end_date):
    url = f"https://api.weatherbit.io/v2.0/history/daily?key=6f2c43a59b5a4476a4553686535896dd&lat={lat}&lon={lon}&start_date={start_date}&end_date={end_date}&units=M"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        return None

#Documents definitions

class User(db.Document, UserMixin):
    id = db.IntField(primary_key=True)
    mail = db.StringField(required=True)
    pwd= db.StringField(required=True)
    name = db.StringField()
    birth_date = db.DateField()
    location=db.StringField(required=True)
    cities = db.ListField()
    mail_alert = db.BooleanField(default=False)
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

class Weather(db.Document):
    data=db.DictField()
    date=db.DateTimeField(default=datetime.datetime.utcnow())
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
    date=db.DateTimeField(default=datetime.datetime.utcnow())

class History(db.Document):
    user_id=db.IntField()
    data=db.DictField()
    city=db.StringField()
    date=db.DateTimeField(default=datetime.datetime.utcnow())
# App Routers

class HistoryCity(db.Document):
    city_name=db.StringField()
    #data=db.DictField()
    date=db.DateField()
    weather=db.FloatField()
    

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
        # Check if the user_info is present in the POST request data
        if 'user_id' not in request.json:
            return "<h1>Paramètre manquant</h1>"

        # Load the user's data from the database
        user = User.objects(id=request.json['user_id']).first()

        data= get_weather_data(api_key , request.json.get("city").lower())
        #Add the searched weather to the user history
        w= Weather(data=data,city=request.json.get("city").lower())
        h=History(user_id=user.id,data=data,city=request.json.get("city").lower())
        h.save()
        #Check if the place exist in our data base ! (needed later in the notifications system)
        p = Place.objects(name=request.json.get("city").lower()).first()
        if p == None:
            p=Place(name=request.json.get("city").lower(),lat=float(data["coord"]["lat"]),lon=float(data["coord"]["lon"]))
            p.save()
        w.save()
        return make_response(jsonify("le meteo de la ville ",request.json.get("city"),"est : ", data), 200)
    else :
        Ls = []
        for r in Weather.objects(city=request.json.get("city").lower()):
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun meteo sauvgardées dans le systéme!", 201)
        else:
            now = datetime.datetime.now()
            today =now.strftime('%d')
            for data in Ls:
                date_str = data['date']
                d = date_str.strftime('%d')
                if int(today) - int(d) <= 15:
                    print("temperature : ", data['data'],"  date : ", data['date'])
            return make_response(jsonify("success"), 200)

@login_required
@app.route("/historique", methods=['GET','POST'])
def get_history():
    #Get the History of a specific city
    if request.method == "POST":
        c=request.json.get("city").lower()
        city=c.lower()
        u=User.objects(id=request.json['user_id']).first()
        print(u.id)
        print(city)
        hs = History.objects(user_id=u.id, city=city)
        print(hs)
        if hs == "None":
            return make_response("Aucun Meteo sauvgardée pour cette ville", 201)
        else:
            return make_response(jsonify(hs), 200)
    else:
        #Get all the user's history
        u=User.objects(id=request.args.get('user_id')).first()

        hs= History.objects(user_id=u.id)
        if hs == "None":
            return make_response("Aucun Historique pour vous", 201)
        else:
            return make_response(jsonify(hs), 200)

@login_required
@app.route("/forcast",methods=["get"])
def get_forcast():
    city=request.form.get("city").lower()
    p= Place.objects(name=city).first()
    #si le cité en question n'existe pas dans la base on l'ajout de plus son meteo courant et on recupére son forcast!
    if p == "None":
        data= get_weather_data(api_key , city)
        w= Weather(data=data,city=city)
        data1 = get_city_data(api_key, city)
        p=Place(name=city,lat=float(data1[0]["lat"]),lon=float(data1[0]["lon"]))
        p.save() 
        w.save()
        forcast_data= get_forcast_data(api_key,float(data1[0]["lat"]),float(data1[0]["lon"]))
        return make_response(jsonify("forcast de la ville  ",city,"est : ", forcast_data), 200)
    else:
        #Si ca existe ! on affiche son forcast directement
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
        mail_alert = request.form.get("mail_alert")
        existing_user = User.objects(mail=mail).first()
        loc=location.lower()
        #Adding all the cities and location to place class
        if existing_user is None:
            p= Place.objects(name=loc).first()
            #si le cité en question n'existe pas dans la base on l'ajout de plus son meteo courant et on recupére son forcast!
            if p == None:
                data= get_city_data(api_key , location)
                if not data: #verification si location saisi par user est valide ou non
                    return make_response("location invalide", 201)
                p=Place(name=loc,lat=float(data[0]["lat"]),lon=float(data[0]["lon"]))
                p.save()
            cities1 = cities
            for i in range(len(cities)):
                cities1[i] = cities[i].lower()
            for c in cities1:
                p1= Place.objects(name=c).first()
                if p1 == None:
                    data1=get_city_data(api_key,c)
                    if not data1: #verification si location saisi par user est valide ou non
                        return make_response("city invalide", 201)
                    p1=Place(name=c,lat=float(data1[0]["lat"]),lon=float(data1[0]["lon"]))
                    p1.save()


            hashpass = generate_password_hash(pwd, method='sha256')
            v = User(mail=mail,pwd=hashpass,name=name,birth_date=birth_date,location=location, cities=cities, mail_alert = mail_alert)
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
    us_id = session['user_id']
    us_id_str = str(us_id)

    print(session['user_id'])
    print(us_id)
    print(us_id_str)

    login_user(check_user)
    return make_response(us_id_str, 200)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    # Remove session data
    session.pop('user_id', None)
    return make_response("Logged out!", 200)   

@app.route('/profile', methods=['POST'])
def profile():
    # Check if the user_info is present in the POST request data
    if 'user_id' not in request.json:
        return "<h1>Paramètre manquant</h1>"

    # Load the user's data from the database
    user = User.objects(id=request.json['user_id']).first()

    # Display the user's profile page
    return f"<h1>Bonjour, {user.name}!</h1>"

@login_required
@app.route('/notifications',methods=['GET'])
def get_notif():

    us_id = request.args.get('user_id')
    notifications = []
    for n in Notification.objects(user_id=us_id):
        notifications.append({'message': n.msg, 'location': n.location})
    return jsonify(notifications), 200



@app.route('/city/historique', methods=['GET'])
def get_city_hist():
    ps = []
    user = User.objects(id=request.args.get('user_id')).first()
    if user is None:
        return jsonify({'error': 'User not found.'}), 404
    loc = user.location

    # Add all the user's favorites and his own location
    if loc:
        p = Place.objects(name=loc.lower()).first()
        if p:
            ps.append(p)
    for c in user.cities:
        p = Place.objects(name=c.lower()).first()
        if p:
            ps.append(p)

    for t in ps:
        date_start = datetime.date.fromordinal(datetime.date.today().toordinal() - 15)
        history = get_city_history(t.lat, t.lon, date_start, datetime.date.today())
        data = HistoryCity.objects(city_name=t.name).first()
        if data is None:
            for i in range(15):
                data = HistoryCity(city_name=t.name, date= history['data'][i]['datetime'], weather=history['data'][i]['temp'])
                data.save()
    ls = []
    for i in HistoryCity.objects(city_name=loc.lower()):
        for j in range(16):
            if(datetime.date.fromordinal(datetime.date.today().toordinal() - j)==i.date):
                ls.append(i)
    # Tri des valeurs en fonction de leur date
    ls_trie = sorted(ls, key=lambda x: x.date, reverse=True)

    return make_response(jsonify(ls_trie), 200)




# ******************** KAFKA ************************
#Kafka-confluent Configs 
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'),bootstrap_servers=['pkc-4r297.europe-west1.gcp.confluent.cloud:9092'],
                         sasl_mechanism='PLAIN',
                         security_protocol='SASL_SSL',
                         sasl_plain_username='A4M2HY7ZEQB4ZQZM',
                         sasl_plain_password='yPAElfU0B9/xD9Xr+duSD5TWyK2cL1JRrcGuGFz2vBYPPkEop24vAZ8SHcDblyDf',
                         api_version=(2, 7, 0))
consumer = KafkaConsumer ('check_notif', group_id = 'group1',bootstrap_servers = ['pkc-4r297.europe-west1.gcp.confluent.cloud:9092'],
                          sasl_mechanism='PLAIN',security_protocol='SASL_SSL',sasl_plain_username='A4M2HY7ZEQB4ZQZM',
                          sasl_plain_password='yPAElfU0B9/xD9Xr+duSD5TWyK2cL1JRrcGuGFz2vBYPPkEop24vAZ8SHcDblyDf',auto_offset_reset = 'earliest',
                          value_deserializer=lambda m: json.loads(m.decode('ascii')))

consumer.subscribe(['check_notif'])

#The producer function 
def produce_weather_data(topic, msg ,location):
    # Convert data to dictionary
    data={"msg":msg, "location":location}
    # Send data to Kafka topic
    producer.send(topic, value=data)
    producer.flush()
    print(f'Production processing on "{topic}": {msg} , {location}')


def check_weather_alerts(weather_data):
    msg = ""
    
    if weather_data["weather"][0]["main"] == "Thunderstorm":
        msg = "Alert: Thunderstorm detected! Please stay indoors and avoid exposed areas."    
    elif weather_data["weather"][0]["main"] == "Tornado":
        msg = " Alert: Tornado detected! Seek shelter immediately in a basement or interior room on the lowest floor."   
    elif weather_data["weather"][0]["main"] == "Squall":
        msg = " Alert: Squall detected! Avoid going outside and secure all loose objects."   
    elif weather_data["weather"][0]["main"] in ["Haze", "Smoke", "Dust", "Ash"]:
        msg = " Alert: Poor air quality detected! Avoid outdoor activities if possible."    
    elif weather_data["weather"][0]["main"] in ["Fog", "Mist"]:
        msg = " Alert: Reduced visibility detected! Use caution while driving and be aware of your surroundings."
    
    # Check for extreme temperatures
    elif weather_data["main"]["temp"] < -10:
        msg = "Alert: Extremely low temperatures detected! Dress in multiple layers and cover all exposed skin to prevent frostbite. Avoid prolonged outdoor exposure and stay hydrated."
    elif weather_data["main"]["temp"] > 40:
        msg = " Alert: Extremely high temperatures detected! Wear light, loose-fitting clothing and a hat to stay cool. Stay hydrated and avoid prolonged outdoor exposure during peak sun hours."
    
    # Check for heavy precipitation
    elif weather_data["weather"][0]["main"] == "Rain":
            msg = "Alert: Heavy rain detected! Use caution while driving and be aware of potential flooding in low-lying areas."
    elif weather_data["weather"][0]["main"] == "Snow":
            msg = "Alert: Heavy snow detected! Use caution while driving and be aware of reduced visibility and slippery road conditions."    
    else:
            msg = "No severe weather conditions detected."
    
    return msg

#The con job function 
def check_changes():
    while True:
        #Check all the cities
        ps= Place.objects()
        for p in ps:
            if p.name != None:
                weather_data = get_weather_data(api_key, p.name)
                if weather_data is not None:
                    alert_msg = check_weather_alerts(weather_data)                
                    produce_weather_data('check_notif',alert_msg,p.name)
                else:
                    print('Error retrieving weather data.')
        time.sleep(60)

#The consumer function 
def consume_notification():
    try:
        while True:
            Notification.objects.delete()
            print("Consuming processing ...")
            for message in consumer:
                # read single message at a time
                if message is None:
                    print("msg vide")
                else:
                    #Search all users that are interessted in that location
                    users= User.objects()
                    for u in users:
                        #Create for each user a new notification 
                        #Specific notification for the user's location 
                        loc =u.location
                        if loc.lower() == message.value["location"]:
                            n=Notification(user_id=u.id,msg=message.value["msg"],location=message.value["location"])
                            n.save()
                        #Specific notification for the user's favorite cities
                        else:
                            for city in u.cities:
                                if city.lower() == message.value["location"]:
                                    n=Notification(user_id=u.id,msg=message.value["msg"],location=city)
                                    n.save()
            consumer.commit()
            time.sleep(1)
    except Exception as ex:
        print(f"Kafka Exception : { ex}")

    finally:
        print("closing consumer")
        consumer.close()

if __name__ == '__main__':

    #start the producer and consumer  in a separate threads
    producer_thread = threading.Thread(target=check_changes)
    producer_thread.start()
    consumer_thread = threading.Thread(target=consume_notification)
    consumer_thread.start()

    # start the Flask application
    app.run()