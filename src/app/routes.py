from flask import flash,make_response
from models import User , Weather , Place
from flask import Flask, make_response, request, jsonify, render_template, send_file , url_for
from werkzeug.security import generate_password_hash ,check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from config import api_key
from app import login_manager , routes_BP
import json
import requests


def get_weather_data(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return json.dumps(data, indent = 3)
    else:
        return None

# App Routers

@routes_BP.route("/cities", methods=["POST", 'GET'])
def set_place():
    if request.method == "POST":
        with open('../../json/cities.json', 'r') as f:
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
def set_weather():
    if request.method == "POST":
        data= get_weather_data(api_key , request.data.get("city"))
        w= Weather(data=data,city=request.data.get("city"))
        #Check if the place exist in our data base! 
        p = Place.objects(name=request.data.get("city")).first()
        if p == None:
            p=Place(name=request.data.get("city"),lat=data["coord"]["lat"],lon=data["coord"]["lon"])
            p.save() 
        w.save()
        return make_response("Ajout du météo avec succées! ", 200)

@routes_BP.route('/register', methods=['POST'])
def register():
    mail = request.form.get("mail")
    name = request.form.get("name")
    pwd = request.form.get("pwd")
    birth_date = request.form.get("birth_date")
    location = request.form.get("location")

    existing_user = User.objects(mail=mail).first()
    if existing_user is None:
        hashpass = generate_password_hash(pwd, method='sha256')

        u = User(mail=mail, pwd=hashpass, name=name, birth_date=birth_date,
                        location=location)

        max_id = 0      #assign an id to the user
        for u in User.objects:
            if u.id > max_id:
                max_id = u.id
        u.id = max_id + 1
        u.save()
        return make_response("Bienvenue à MeteoApp", 200)
    else:
        return make_response("Compte existant", 201)


@routes_BP.route('/login', methods=['POST'])
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

@routes_BP.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True}), 200