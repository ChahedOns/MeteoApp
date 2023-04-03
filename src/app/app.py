from flask_login import LoginManager
from flask import Flask, Blueprint
from config import db_name, user_pwd,user_db
from flask_mongoengine import MongoEngine
from mongoengine import EmbeddedDocumentListField, ReferenceField, EmbeddedDocumentField, ListField
from flask import Flask, make_response, request, jsonify, render_template, send_file , url_for , session
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from config import api_key , secret_key
import json
import requests
from flask_login import UserMixin
from werkzeug.security import check_password_hash
import re
from flask_login import current_user
from wtforms import ValidationError
import datetime

# configurations !
app = Flask(__name__)
DB_URI ="mongodb+srv://admin:adminadmin@cluster0.ad4hkct.mongodb.net/MeteoApp?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI
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
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
    
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

    def to_json(self):
        return {
            "ID": self.id,
            "Mail":self.mail,
            "Name":self.name,
            "Birthday":self.birth_date,
            "location":self.location
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
    date=db.DateField(default=datetime.datetime.now)
    city=db.StringField()
    def to_json(self):
        return{
            "Data": self.data,
            "Date":self.date,
            "City":self.city
        }

class History (db.Document):
    city=db.StringField()
    data=db.DictField()
    date=db.DateField(default=datetime.datetime.now)
    def to_json(self):
        return{
            "Data": self.data,
            "Date":self.date,
            "City":self.city
        }

# App Routers

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
    if request.method == "GET":
        data= get_weather_data(api_key , request.form.get("city"))
        w= Weather(data=data,city=request.form.get("city"))
        h= History(city=request.form.get("city"),data=data)
        h.save()
        #Check if the place exist in our data base! 
        p = Place.objects(name=request.form.get("city")).first()
        if p == None:
            p=Place(name=request.form.get("city"),lat=float(data["coord"]["lat"]),lon=float(data["coord"]["lon"]))
            p.save() 
        w.save()
        return make_response(jsonify("le meteo de la ville ",request.form.get("city"),"est : ", data), 200)


@app.route("/history", methods=['GET'])
def get_history():
        city = request.form.get("city")
        E = History.objects(city=city)
        if E == "None":
            return make_response("Aucun Meteo sauvgardée pour cette ville", 201)
        else:
            return make_response(jsonify("L'Historique de météo de",city,"est : \n",E), 200)
        
@app.route("/forcast",methods=["get"])
def get_forcast():
    city=request.form.get("city")
    p= Place.objects(name=city).first()
    if p == "None":
        data= get_weather_data(api_key , city)
        w= Weather(data=data,city=request.form.get("city"))
        h= History(city=request.form.get("city"),data=data)
        p=Place(name=request.form.get("city"),lat=float(data["coord"]["lat"]),lon=float(data["coord"]["lon"]))
        p.save() 
        w.save()
        h.save()
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
        existing_user = User.objects(mail=mail).first()
        if existing_user is None:
            hashpass = generate_password_hash(pwd, method='sha256')
            u = User(mail=mail,pwd=hashpass,name=name,birth_date=birth_date,location=location)
            max_id = 0      #assign an id to the user
            for u in User.objects:
                if u.id > max_id:
                    max_id = u.id
            u.id = max_id + 1
            u.save()
            return make_response("Bienvenue à MeteoApp", 200)
        else:
            return make_response("Compte existant", 201)


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
   
    return login_user(check_user)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True}), 200       

    
@app.route("/", methods=['POST', 'GET'])
def hello():
    if "username" in session:
        return make_response("you are logged in : Dashboard! ", 200)
    else:
        return make_response("Hello",201)

if __name__ == '__main__':
    app.run()
    app.secret_key = secret_key
