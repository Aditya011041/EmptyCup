from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import json
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite as the database
db = SQLAlchemy(app)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    projects = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/listings')
def api_listings():
    try:
        # Fetch data from the database
        listings = Listing.query.all()
        data = {"listings": []}

        for listing in listings:
            data["listings"].append({
                "name": listing.name,
                "projects": listing.projects,
                "experience": listing.experience,
                "phone": listing.phone,
                "price": listing.price
            })

        return jsonify(data)

    except Exception as e:
        print("Error fetching data from the database:", e)
        return jsonify({"error": "Internal Server Error"}), 500

# Function to add sample data to the database
def add_sample_data():
    # Check if there are existing records
    existing_records = Listing.query.all()
    if not existing_records:
        epic_designs = Listing(
            name="Epic Designs",
            projects=43,
            experience=4,
            phone="+91-984532853",
            price=4
        )

        empty_cup = Listing(
            name="Emp Cup",
            projects=43,
            experience=4,
            phone="+91-984532853",
            price=4
        )

        # Add instances to the database session
        db.session.add(epic_designs)
        db.session.add(empty_cup)

        # Commit the changes to the database
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables before running the app
        db.create_all()

        # Check if the "--empty" command-line argument is provided
        if "--empty" in sys.argv:
            print("Using an empty database.")
        else:
            # Add sample data to the database if it's empty
            add_sample_data()
            print("Sample data added to the database.")

    # Run the app
    app.run(debug=Falsw)
