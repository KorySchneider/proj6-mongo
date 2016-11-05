import uuid, arrow
from operator import itemgetter

from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets

MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port,
    secrets.client_secrets.db)

collection = None

def connect():
    global MONGO_CLIENT_URL
    global collection
    try:
        dbclient = MongoClient(MONGO_CLIENT_URL)
        db = getattr(dbclient, secrets.client_secrets.db)
        collection = db.dated
        return collection
    except:
        print("Failure opening database.  Is Mongo running? Correct password?")
        sys.exit(1)

def create(text, date):
    global collection
    collection.insert({ 'text': text, 'date': date, '_id': str(uuid.uuid4()), 'type': 'dated_memo' })

def remove(uid):
    global collection
    collection.remove({ '_id': uid })

def get_memos():
    """
    Returns all memos in the database, sorted oldest to newest
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = arrow.get(record['date']).isoformat()
        records.append(record)
    sorted_records = sorted(records, key=itemgetter('date'))
    return sorted_records
