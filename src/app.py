import datetime
import requests
from flask import Flask, make_response, request, jsonify, render_template, send_file , url_for
from flask_mongoengine import MongoEngine
from mongoengine import EmbeddedDocumentListField, ReferenceField, EmbeddedDocumentField, ListField
from APIConst import db_name, user_pwd, api_key
import json

# configurations !
app = Flask(__name__)
DB_URI = f"mongodb+srv://{user}:{user_pwd}@cluster0.ad4hkct.mongodb.net/{db_name}?retryWrites=true&w=majority"
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
    id = db.StringField()
    mail = db.StringField(required=True)
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
    id=db.StringField()
    name=db.StringField(required=True)
    lat=db.FloatField()
    lon=db.StringField()

    def to_json(self):
        return{
            "ID": self.id,
            "Name": self.name,
            "Lat":self.lat,
            "Lon":self.lon
        }

class weather(db.Document):
    id=db.StringField()
    data=db.DictField()
    date=db.DateTimeField(default=datetime.utcnow)
    city=db.StringField()
    def to_json(self):
        return{
            "ID": self.id,
            "Data": self.data,
            "Date":self.date,
            "City":self.city
        }
    
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


@app.route("/cite", methods=["POST", 'GET'])
def set_cite():
    if request.method == "POST":
        with open('json/cities.json', 'r') as f:
            data = json.load(f)
            i = 0
            while i < len(data):
                D = Dept.objects(code_dept=data[i]["department_code"]).first
                if D == None:
                    return make_response("Departement inexistant", 201)
                else:
                    C = Cities(id_cite=int(data[i]["id"]), dept=data[i]["department_code"], nom_cite=data[i]["name"],
                               lat=float(data[i]["gps_lat"]), slug_cite=data[i]["slug"],
                               lng=float(data[i]["gps_lng"]))
                    C.save()
                i = i + 1

            return make_response("Ajout de tous les départements avec succés", 200)
    else:
        Ls = []
        for r in Cities.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun cite dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les cites sont : ", Ls), 200)
