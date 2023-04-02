import requests
from flask_login import LoginManager
from flask import Flask, Blueprint
from config import db_name, user_pwd,user_db
from flask_mongoengine import MongoEngine
from mongoengine import EmbeddedDocumentListField, ReferenceField, EmbeddedDocumentField, ListField

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
#Database setup
db = MongoEngine()
db.init_app(app)
#Blueprint setup
routes_BP= Blueprint('routes', __name__)
app.register_blueprint(routes_BP)
# Login manager setup
login_manager = LoginManager()

if __name__ == '__main__':
    app.run()
