from sasya_project import app, db
from sasya_project.models import SolarPlans
import csv

if __name__ == "__main__":
    with app.app_context():        
        db.create_all()
        # with open("plans.csv", "r") as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         plan = SolarPlans(name=row["name"], energy_daily=row["energy_daily"], cost=row["cost"], area_required=row["area_required"], uses=row["uses"], company=row["company"])
        #         db.session.add(plan)
        #     db.session.commit()
    app.run(debug=True, port=10000)