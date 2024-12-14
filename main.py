from flask import Flask, render_template, request, redirect, url_for

from data import data
from data.base import create_db
#from data.data_to_db import write_data_to_db
from data.base import Session
from data.models import Reserve, Tour


app = Flask(__name__)


@app.context_processor
def global_data():
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


if __name__ == "__main__":
    create_db()
    #write_data_to_db()
    app.run(debug=True)
