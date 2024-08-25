from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning from SQLAlchemy

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=True)  # Column for ingredient code
    name_korean = db.Column(db.String(100), nullable=True)  # Column for the Korean name
    name_english = db.Column(db.String(100), nullable=True)  # Column for the English name
    cas_no = db.Column(db.String(20), nullable=True)  # Column for CAS number
    definition_korean = db.Column(db.Text, nullable=True)  # Column for the Korean definition
    definition_english = db.Column(db.Text, nullable=True)  # Column for the English definition
    mixing_purpose_korean = db.Column(db.Text, nullable=True) 
    mixing_purpose_english = db.Column(db.Text, nullable=True)  
    
@app.route('/analyze', methods=['POST'])
def analyze_ingredients():
    ingredients = request.json.get('ingredients', [])
    response = []

    for ingredient_name in ingredients:
        ingredient = Ingredient.query.filter_by(name_english=ingredient_name).first()
        if ingredient:
            response.append({
                'name': ingredient.name_english,
                'code': ingredient.code,
                'cas_no': ingredient.cas_no,
                'definition_korean': ingredient.definition_korean,
                'definition_english': ingredient.definition_english,
                'mixing_purpose_korean': ingredient.mixing_purpose_korean,
                'mixing_purpose_english': ingredient.mixing_purpose_english
            })
        else:
            response.append({
                'name': ingredient_name,
                'description': 'Ingredient not found in database',
            })
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
