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

import db_functions # functions for interacting with the database

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify

import logging

# Date handling
import arrow

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

###
# Initialize database connection
###
db_functions.connect()

###
# Pages
###
@app.route("/")
@app.route("/index")
def index():
    g.memos = db_functions.get_memos()
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
        db_functions.create(text, date)
        return jsonify({ 'success': True })
    except:
        return jsonify({ 'success': False })

@app.route('/_remove_memo')
def _remove_memo():
    global collection
    try:
        memo_id = request.args.get('_id', type=str)
        db_functions.remove(memo_id)
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
    tz_offset = int(request.cookies.get('tz_offset'))

    try:
        then = arrow.get(date).to('local').replace(hours=0, minutes=0, seconds=0)
        now = arrow.utcnow().to('local').replace(hours=0, minutes=0, seconds=0)

        time = str(now.time()).split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(float(time[2]))
        then = then.replace(hours=hour, minutes=minute, seconds=second)

        if then.date() == now.date():
            human = "today"
        elif then.date() == now.replace(days=+1).date():
            human = "tomorrow"
        elif then.date() == now.replace(days=-1).date():
            human = "yesterday"
        else:
            human = then.humanize(now)
            if human == "in a day":
                human = "tomorrow"
    except:
        human = date
    return human

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")
