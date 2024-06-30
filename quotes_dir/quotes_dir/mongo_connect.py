import mongoengine
from .settings import env

def connect_to_mongo():
    mongoengine.connect(db=env('DB_NAME'),
                        host=env('DB_URL'))