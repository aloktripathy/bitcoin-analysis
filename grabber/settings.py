from datetime import datetime
from mongoengine import connect
import pytz

import keys
import constants

connect(
    db=keys.MONGO_DB_NAME,
    username=keys.MONGO_DB_USER,
    password=keys.MONGO_DB_PASSWORD,
    host=keys.MONGO_DB_HOST,
    port=keys.MONGO_DB_PORT
)
