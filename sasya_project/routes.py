from . import app, db
from flask import render_template, redirect, url_for, request
from .models import SolarPlans

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/solar_panel", methods=["GET", "POST"])
def solar_panel():
    if request.method == "POST":
        energy_daily = request.form.get("energy_daily")
        budget = request.form.get("budget")
        area_available = request.form.get("area_available")

        query_energy_daily = energy_daily
        query_budget = budget
        query_area_available = area_available

        if energy_daily == None:
            query_energy_daily = 0
            display_energy = "Not Specified"
        if budget == None:
            query_budget = 999999999999999999999999999999999999
            display_budget = "Not Specified"
        if area_available == None:
            query_area_available = 1000000
            display_area_available = "Not Specified"
        
        suitable_rows = SolarPlans.query.filter(SolarPlans.energy_daily >= float(query_energy_daily), SolarPlans.cost <= query_budget, SolarPlans.area_required <= query_area_available).all()   

        return render_template("solar_panel.html", plans=suitable_rows, energy_daily=energy_daily, budget=budget, area_available=area_available)

    return render_template("solar_panel.html")
