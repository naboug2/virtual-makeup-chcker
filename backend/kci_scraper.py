from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as translate
import os

# Flask app and database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ingredients.db'  # Or use another database
db = SQLAlchemy(app)

# Define the Ingredient model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    name_korean = db.Column(db.String(100))
    name_english = db.Column(db.String(100))
    cas_no = db.Column(db.String(20))
    definition_korean = db.Column(db.Text)
    definition_english = db.Column(db.Text)
    mixing_purpose_korean = db.Column(db.Text)  
    mixing_purpose_english = db.Column(db.Text)

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\nuhaa\Desktop\virtual makeup checker\docs\cloud_translate_service_acount.json"
translate_client = translate.Client()


def translate_text(text, target_language="en"):
    """Translates text into the target language."""
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def safe_get_text(soup, selector):
    """Safely get text from an element, return 'N/A' if the element is not found."""
    element = soup.select_one(selector)
    return element.get_text(strip=True) if element else "N/A"

# Iterate over a range of ingredient IDs
for ingredient_id in range(1, 19180):  # Adjust the range as needed
    url = f'https://kcia.or.kr/cid/search/ingd_view.php?no={ingredient_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Use safe_get_text to avoid AttributeError
    ingredient_code = safe_get_text(soup, '#content > div > div.sub_content > div > div > table:nth-child(3) > tbody > tr:nth-child(1) > td > p')
    ingredient_name_korean = safe_get_text(soup, '#content > div > div.sub_content > div > div > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2) > p > b')
    ingredient_name_english = safe_get_text(soup, '#content > div > div.sub_content > div > div > table:nth-child(3) > tbody > tr:nth-child(3) > td > p:nth-child(1)')
    cas_no = safe_get_text(soup, '#content > div > div.sub_content > div > div > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2) > p')
    definition_korean = safe_get_text(soup, '#content > div > div.sub_content > div > div > table:nth-child(3) > tbody > tr:nth-child(5) > td > p')
    mixing_purpose_korean = safe_get_text(soup, '#content > div > div.sub_content > div > div > table:nth-child(3) > tbody > tr:nth-child(8) > td > p')
    # Translate the Korean text if available
    definition_english = translate_text(definition_korean) if definition_korean != "N/A" else "N/A"
    mixing_purpose_english = translate_text(mixing_purpose_korean) if mixing_purpose_korean != "N/A" else "N/A"

    # Store the data in the database
    new_ingredient = Ingredient(
        code=ingredient_code,
        name_korean=ingredient_name_korean,
        name_english=ingredient_name_english,
        cas_no=cas_no,
        definition_korean=definition_korean,
        definition_english=definition_english,
        mixing_purpose_korean=mixing_purpose_korean,  
        mixing_purpose_english=mixing_purpose_english
    )

    with app.app_context():
        db.session.add(new_ingredient)
        db.session.commit()

    print(f"Stored ingredient: {ingredient_name_english}")
