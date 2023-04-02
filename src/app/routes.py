from flask import flash,make_response,redirect
from models import User , Weather , Place
from flask import Flask, make_response, request, jsonify, render_template, send_file , url_for
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from config import api_key
from app import login_manager , routes_BP
import json
import requests


def login_and_redirect(user):
    """Logs in user, flashes welcome message and redirects to index"""
    login_user(user)
    flash(f"Welcome {user.username}!", category="success")
    return redirect(url_for("core.index"))

@login_manager.user_loader
def load_user(user_id):
    """Load the user object from the user ID stored in the session"""
    return User.objects(pk=user_id).first()

@routes_BP.route("/")
def test():
    return "hello world"


def get_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data, indent = 3)
    else:
        return None

# App Routers
@routes_BP.route("/")
def hello_world():
    return "<h1> Hello, World!</h1>"


@routes_BP.route("/cites", methods=["POST", 'GET'])
def set_place():
    if request.method == "POST":
        with open('../json/cities.json', 'r') as f:
            data = json.load(f)
            i = 0
            while i < len(data):
                C = Place( name=data[i]["name"],
                            lat=float(data[i]["gps_lat"]),
                            lon=float(data[i]["gps_lng"]))
                C.save()
                i = i + 1
            return make_response("Tous les cités sont ajoutés avec succées! ", 200)
    else:
        Ls = []
        for r in Place.objects():
            Ls.append(r)
        if Ls == []:
            return make_response("Aucun cite dans le systéme!", 201)
        else:
            return make_response(jsonify("tous les cites sont : ", Ls), 200)
    

    

@routes_BP.route("/weather", methods=["POST", 'GET'])
def set_weather(city=None):
    if request.method == "POST":
        data= get_weather_data(api_key , city)
        w= Weather(data=data,city=city)
        #Check if the place exist in our data base! 
        p = Place.objects(name=city).first()
        if p == None:
            p=Place(name=city,lat=data["coord"]["lat"],lon=data["coord"]["lon"])
            p.save() 
        w.save()
        return make_response("Ajout du météo avec succées! ", 200)


@routes_BP.route("/register", methods=["POST"])
def register(data):
    """Registers the user with username, email and password hash in database"""
    logout_user()
    password_hash = generate_password_hash(data.password)
    user = User(username=data.username,name=data.name,email=data.mail,password=password_hash,
                birth_date=data.birthday,location=data.location)
    user.save()
    flash("Thanks for registering!", category="success")
    return login_and_redirect(user)

@routes_BP.route("/login", methods=["GET", "POST"])
def login(data):
    """Logs the user in through username/password"""
    logout_user()
    # Grab the user from a user model lookup
    username_or_email = data.username
    if "@" in username_or_email:
        user = User.objects(email=username_or_email).first()
    else:
        user = User.objects(username=username_or_email).first()


    if user is not None and user.check_password(data.password):
        # User validates (user object found and password for that
        # user matched the password provided by the user)
        return login_and_redirect(user)
    else:
        flash("(email or username)/password combination not found", category="error")
        return make_response("ERROR WHILE LOGGIN ", 201)

@routes_BP.route("/logout")
@login_required
def logout():
    """Log out the current user"""
    logout_user()
    flash("You have logged out.", category="success")
    return make_response("Login out succesfully", 200)