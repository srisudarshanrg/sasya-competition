from . import app, db
from flask import render_template, redirect, url_for, request, flash
from .models import SolarPlans
import json
import random

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/all-solar-plans")
def all_solar_plans():
    plans = SolarPlans.query.filter_by().all()
    return render_template("all_solar_plans.html", plans=plans)

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
            query_energy_daily = 0.0
        if budget == None:
            query_budget = 999999999999999999999999999999999999
        if area_available == None:
            query_area_available = 1000000        
        
        suitable_rows = SolarPlans.query.filter(SolarPlans.energy_daily >= float(query_energy_daily), SolarPlans.cost <= int(query_budget), SolarPlans.area_required <= int(query_area_available)).all()
        if len(suitable_rows) == 0:
            return flash("No such plans exist for your requirements in our database.")
        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            graphData = {
                "labels": [plan.name for plan in suitable_rows],
                "energy": [plan.energy_daily for plan in suitable_rows],
                "cost": [plan.cost for plan in suitable_rows],
                "area_required": [plan.area_required for plan in suitable_rows],
                "color": [(r,g,b) for plan in suitable_rows],
            }

            jsonGraphData = json.dumps(graphData)   
            return render_template("solar_panel.html", plans=suitable_rows, energy_daily=energy_daily, budget=budget, area_available=area_available, graph_data=jsonGraphData)

    return render_template("solar_panel.html")
