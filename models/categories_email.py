from database import db
from peewee import UUIDField, CharField, TextField, BooleanField
import uuid

class EmailCategory(db.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)  
    title = CharField(max_length=100)                     
    body = TextField()                                    
    productive = BooleanField(default=False) 

