from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/kiddsyles/documents/street_fighter_flask_app/instance/fighters.db'
db = SQLAlchemy(app)

# Define Fighter model
class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    special_move = db.Column(db.String(100))

    def __repr__(self):
        return f"Fighter(id={self.id}, name={self.name}, origin={self.origin})"

# Function to seed initial data
def seed_database():
    with app.app_context():  # Use app context to interact with the app
        fighters_data = [
            {'name': 'RYU', 'origin': 'Japan', 'special_move': 'Hadouken'},
            {'name': 'KEN', 'origin': 'USA', 'special_move': 'Shoryuken'},
            {'name': 'CHUN-LI', 'origin': 'China', 'special_move': 'Spinning Bird Kick'},
            {'name': 'JURI', 'origin': 'South Korea', 'special_move': 'Feng Shui Engine'},
            {'name': 'ZEKU', 'origin': 'Japan', 'special_move': 'Bushin Gram Koku'},
            {'name': 'JAMIE', 'origin': 'Hong Kong', 'special_move': 'Freeflow Strikes'}
        ]

        for fighter_data in fighters_data:
            fighter = Fighter(**fighter_data)
            db.session.add(fighter)

        db.session.commit()

# Root route
@app.route('/')
def home():
    return "Welcome to the Street Fighter Database!"

# Create routes for CRUD operations
@app.route('/fighters', methods=['GET'])
def get_fighters():
    fighters = Fighter.query.all()
    return jsonify([{'id': fighter.id, 'name': fighter.name, 'origin': fighter.origin} for fighter in fighters]), 200


@app.route('/fighters/<int:fighter_id>', methods=['GET'])
def get_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)
    return jsonify({'id': fighter.id, 'name': fighter.name, 'origin': fighter.origin}), 200

@app.route('/fighters', methods=['POST'])
def create_fighter():
    # Get JSON data from the request body
    data_list = request.get_json()

    # Iterate through each item in the list (assuming it's a list of fighter data)
    for data in data_list:
        # Extract name, origin, and special_move from each item in the list
        name = data.get('name')
        origin = data.get('origin')
        special_move = data.get('special_move')

        # Create a new Fighter instance
        new_fighter = Fighter(name=name, origin=origin, special_move=special_move)

        # Add the new fighter to the database
        db.session.add(new_fighter)

    # Commit all changes to the database
    db.session.commit()

    # Return a response indicating success
    return jsonify({'message': 'Fighters created successfully'}), 201


@app.route('/fighters/<int:fighter_id>', methods=['PUT'])
def update_fighter(fighter_id):
    # Retrieve the fighter from the database using the provided fighter_id
    fighter = Fighter.query.get_or_404(fighter_id)

    # Get JSON data from the request body
    data = request.get_json()

    # Update fighter attributes if provided in the JSON request
    fighter.name = data.get('name', fighter.name)
    fighter.origin = data.get('origin', fighter.origin)
    fighter.special_move = data.get('special_move', fighter.special_move)

    # Commit changes to the database
    db.session.commit()

    # Return a response indicating success
    return jsonify({'message': 'Fighter updated successfully'}), 200


@app.route('/fighters/<int:fighter_id>', methods=['DELETE'])
def delete_fighter(fighter_id):
    fighter = Fighter.query.get_or_404(fighter_id)

    # Delete the fighter from the database
    db.session.delete(fighter)
    db.session.commit()

    # Return a response indicating success
    return jsonify({'message': 'Fighter deleted successfully'}), 200

if __name__ == '__main__':
    # Seed initial data into the database
    seed_database()

    # Run the Flask application
    app.run(debug=True)
