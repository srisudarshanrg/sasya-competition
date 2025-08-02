from . import db

class SolarPlans(db.Model):
    __tablename__ = "solar_plans"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    energy_daily = db.Column(db.Float())
    cost = db.Column(db.Integer())
    area_required = db.Column(db.Integer())
    uses = db.Column(db.String())
    company = db.Column(db.String())