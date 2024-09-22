from flask import Flask, jsonify
from dotenv import load_dotenv
from connectors.mysql_connector import connection

from sqlalchemy.orm import sessionmaker , session
from sqlalchemy import text, select
from models.product import Product
from models.review import Review

from controllers.product import product_routes
from controllers.user import user_routes
from controllers.review import review_routes
import os

from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from models.user import User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(product_routes)
app.register_blueprint(user_routes)
app.register_blueprint(review_routes)

# JSON Web Token
jwt = JWTManager(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(connection)
    s = Session()
    try:
        s.add(user_id)
        s.commit()
    except Exception as e:
        return s.query(User).get(int(user_id))
    finally: 
        s.close()
    
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route("/")
def hello_world():

    review_query = select(Review)
    Session = sessionmaker(connection)
    with Session() as s:
        result = s.execute(review_query)
        for row in result.scalars():
            print(f'ID: {row.id}, Name: {row.email}')

    return "Insert Sukses"