from flask_peewee.db import Database

db = None 

def init_db(app):
    global db
    db = Database(app)
    return db
