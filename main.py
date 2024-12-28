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
from data.forms import  LoginForm, SignUpForm


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
login_manager = LoginManager()
login_manager.login_message = "Для купівлі туру увійдіть до системи"
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def get_user(user_id):
    with Session() as session:
        return session.query(User).where(User.id == user_id).first()



@app.context_processor
def global_data():
    with Session() as session:
        if current_user.is_authenticated:
            user = session.query(User).where (User.id == current_user.id).first()
            user_tours = user.tours
        else:
            user_tours = []

        return dict(
        departures=data.departures,
        user_tours=user_tours
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


@app.post("/tour/reserve/<int:tour_id>")
@login_required
def reserve(tour_id):
    with Session() as session:
        tour = session.query(Tour).where(Tour.id == tour_id).first()
        user = session.query(User).where(User.id == current_user.id).first()
        user.tours.append(tour)
        session.commit()
        return redirect(url_for("account"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        with Session() as session:
            user = session.query(User).where(or_(User.username == username, User.email == username)).first()
            if not user or not check_password_hash(user.password, password):
                flash("Логін або пароль невірний.")
                return redirect(url_for("signup"))
            
            login_user(user)
            return redirect(url_for("acount"))

    return render_template("login.html", form=login_form)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    signup_form = SignUpForm()
    
    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password.data

        with Session() as session:
            user=session.query(User).where(or_(User.email == username, User.username == username)).first()
            if user:
                flash("Такий користувач вже зареєстрований. Увійдіть до системи")
                return redirect(url_for("login"))
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            session.add(user)
            session.commit()
            return redirect(url_for("login"))


    return render_template("signup.html", form=signup_form)

@app.get("/account/")
@login_required
def account():
    return render_template("account.html")


@app.get("/logout/")
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли із системи")
    return redirect(url_for("index"))


if __name__ == "__main__":
    create_db()
    #write_data_to_db()
    app.run(debug=True)
