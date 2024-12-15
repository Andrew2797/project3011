import os
import binascii

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.sql import or_ 
from werkzeug.security import generate_password_hash, check_password_hash

from data import data
from data.base import create_db
from data.base import Session
from data.models import Tour, User
from data.forms import  LoginForm, SingUpForm


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
login_manager = LoginManager()
login_manager.login_message = "Для купівлі туру увійдіть до системи"
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def get_user():
    with Session() as session:
        return session.query(User).where(User,id == id)



@app.context_processor
def global_data():
    with Session() as session:
        if current_user.is_authenticated:
            user = session.query(User).where (User.id == current_user.id).first()
            user_tours = user.tours
        else:
            user_tours = []

    return dict(
        departures=data.departures
    )


@app.get("/")
def index():
    with Session() as session:
        tours = session.query(Tour).all()
        return render_template("index.html", tours=tours)


@app.get("/tour/<int:id>")
def get_tour(id):
    with Session() as session:
        tour = session.query(Tour).where(Tour, id == id).first()
        return render_template("tour.html", tour=tour)


@app.get("/departure/<dep_eng>")
def departure(dep_eng):
    with Session() as session:
        tours = session.query(Tour).where(Tour.departure == dep_eng).all()

        return render_template("departure.html", tours=tours, dep_eng=dep_eng)


@app.post("/tour/reserve/<int:id>")
def reserve(id):
    with Session() as session:
        #name = request.form.get("name")
        #reserve_tour = Reserve(name=name, tour_id=id)
        #session.add(reserve_tour)
        #session.commit()
        return redirect(url_for("index"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        with Session() as session:
            user = session.query(User).where(or_(User.username == username, User.email == username)).first()
            if not user:
                flash("Такого користувача не існуєю. Зареєструйтесь")
                return redirect(url_for("singup"))
            
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("acount"))
            
            flash("Пароль не вірний.")

    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    create_db()
    #write_data_to_db()
    app.run(debug=True)
