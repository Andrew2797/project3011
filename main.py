from flask import Flask, render_template

from data import data


app = Flask(__name__)
NAVIGATION = data.departures


@app.get("/")
def index():
    return render_template("index.html", departures=NAVIGATION, tours=data.tours)


@app.get("/tour/<int:id>")
def get_tour(id):
    tour = data.tours.get(id)
    return render_template("tour.html", departures=NAVIGATION, tour=tour)


@app.get("/departure/<dep_eng>")
def departure(dep_eng):
    tours = {}
    for id, tour in data.tours.items():
        if tour["departure"] ==dep_eng:
            tours[id] = tour
    
    return render_template("departure.html", departures=NAVIGATION, tours=tours)


if __name__ == "__main__":
    app.run(debug=True)
