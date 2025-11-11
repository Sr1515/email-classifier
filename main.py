import os
import google.generativeai as genai
from flask import Flask
from database import init_db
from dotenv import load_dotenv 

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY", "")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


DATABASE = {
    'name': 'email_category.db',
    'engine': 'peewee.SqliteDatabase'
}

app = Flask(__name__)
app.config.from_object(__name__) 

upload_files = "uploads"
os.makedirs(upload_files, exist_ok=True)

init_db(app)  

from models.categories_email import EmailCategory
from routes import *

if __name__ == '__main__':
    EmailCategory.create_table(safe=True)
    print("Tabela EmailCategory criada com sucesso!")

    if not gemini_api_key:
        print("\n[AVISO] A chave GEMINI_API_KEY não foi carregada do .env. Certifique-se de preenchê-la.")
    
    app.run(debug=True)