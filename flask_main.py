"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates:
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will
   - User input/output is in local (to the server) time.
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify

import json
import logging
import uuid
from operator import itemgetter

# Date handling
import arrow    # Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port,
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

###
# Database connection per server process
###
try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

###
# Pages
###
@app.route("/")
@app.route("/index")
def index():
    g.memos = get_memos()
    return flask.render_template('index.html')

@app.route("/create")
def create():
    return flask.render_template('create.html')

###
# Error handling
###
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

###
# AJAX request handlers
###
@app.route('/_create_memo')
def _create_memo():
    global collection

    text = request.args.get('text', type=str)
    date = request.args.get('date', type=str)
    try:
        collection.insert({ 'text': text, 'date': date, '_id': str(uuid.uuid4()), 'type': 'dated_memo' })
        return jsonify({ 'success': True })
    except:
        return jsonify({ 'success': False })

@app.route('/_remove_memo')
def _remove_memo():
    global collection
    try:
        memo_id = request.args.get('_id', type=str)
        collection.remove({ '_id': memo_id })
        return jsonify({ 'success': True })
    except:
        return jsonify({ 'success': False })

###
# Functions used within the templates
###
@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case.
    """
    try:
        then = arrow.get(date).to('local')
        now = arrow.utcnow().to('local')
        if then.date() == now.date():
            human = "Today"
        else:
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
    except:
        human = date
    return human

###
# Functions available to the page code above
###
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = arrow.get(record['date']).isoformat()
        records.append(record)
    sorted_records = sorted(records, key=itemgetter('date'))
    return sorted_records

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")
