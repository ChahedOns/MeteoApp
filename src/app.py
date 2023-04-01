import datetime
import requests
from flask import Flask, make_response, request, jsonify, render_template, send_file , url_for
from flask_mongoengine import MongoEngine
from mongoengine import EmbeddedDocumentListField, ReferenceField, EmbeddedDocumentField, ListField
from config import db_name, user_pwd, api_key,user_db
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import json
#from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp

# configurations !
app = Flask(__name__)
DB_URI = f"mongodb+srv://{user_db}:{user_pwd}@cluster0.ad4hkct.mongodb.net/{db_name}?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='localhost',
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=None,
    MAIL_PASSWORD=None,
))

db = MongoEngine()
db.init_app(app)
#database definition
class user(db.Document):
    mail = db.StringField(required=True)
    pwd= db.StringField(required=True)
    name = db.StringField(required=True)
    birth_date = db.DateTimeField(required=True)
    location=db.StringField(required=True)
    def to_json(self):
        return {
            "ID": self.ref,
            "Mail":self.mail,
            "Name":self.name,
            "Birthday":self.birth_date,
            "Location":self.location
        }
    
class place(db.Document):
    name=db.StringField(required=True)
    lat=db.FloatField()
    lon=db.StringField()

    def to_json(self):
        return{
            "Name": self.name,
            "Lat":self.lat,
            "Lon":self.lon
        }

class weather(db.Document):
    data=db.DictField()
    date=db.DateField(default=datetime.datetime.now)
    city=db.StringField()
    def to_json(self):
        return{
            "Data": self.data,
            "Date":self.date,
            "City":self.city
        }




#NEEDS

"""def authenticate(mail, password):
    user = user.objects(mail=mail)
    if user and safe_str_cmp(user.pwd.encode('utf-8'), password.encode('utf-8')):
        return user  """


def get_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data, indent = 3)
    else:
        return None

# App Routers
@app.route("/")
def hello_world():
    return "<h1> Hello, World!</h1>"


@app.route("/cites", methods=["POST", 'GET'])
def set_place():
    if request.method == "POST":
        with open('../json/cities.json', 'r') as f:
            data = json.load(f)
            i = 0
            while i < len(data):
                C = place( name=data[i]["name"],
                            lat=float(data[i]["gps_lat"]),
                            lon=float(data[i]["gps_lng"]))
                C.save()
                i = i + 1
            return make_response("Tous les cités sont ajoutés avec succées! ", 200)
    else:
        Ls = []
        for r in place.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun cite dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les cites sont : ", Ls), 200)
    

    

@app.route("/weather", methods=["POST", 'GET'])
def set_weather(city=None):
    if request.method == "POST":
        data= get_weather_data(api_key , city)
        w= weather(data=data,city=city)
        #Check if the place exist in our data base! 
        p = place.objects(name=city).first()
        if p == None:
            p=place(name=city,lat=data["coord"]["lat"],lon=data["coord"]["lon"])
            p.save() 
        w.save()
        return make_response("Ajout du météo avec succées! ", 200)
        
        

