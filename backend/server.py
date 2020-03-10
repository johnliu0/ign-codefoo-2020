"""
IGN Code Foo 10 Submission

Author: John Liu
Date: Monday, March 10, 2020
"""

import db
from flask import (
    Flask,
    request)

# initialize app and connect to MySQL database
app = Flask(__name__)
mysql_db = db.connect_database()

@app.route('/')
def index():
    return 'Hey, this is my solution for IGN Code Foo Summer 2020! API documentation is available in the code.'

@app.route('/items')
def get_items():
    """Retrieves items."""
    mediatype = request.args.get('mediatype', None)
    reviewmin = request.args.get('reviewmin', 0)
    reviewmax = request.args.get('reviewmax', 10)
    sort = request.args.get('sort', 'nameasc')
    return db.wrap_json(db.get_items(mediatype=mediatype, reviewmin=reviewmin, reviewmax=reviewmax, sort=sort))

@app.route('/items/<name>')
def get_item_by_name(name):
    """Gets an item by name."""
    return db.wrap_json(db.get_one_item(name=name))

@app.route('/genres')
def get_genres():
    """Retrieves all available genres."""
    return db.wrap_json(db.get_genres())

@app.route('/studios')
def get_studios():
    """Retrieves all available studios."""
    return db.wrap_json(db.get_studios())

@app.route('/publishers')
def get_publishers():
    """Retrieves all available publishers."""
    return db.wrap_json(db.get_publishers())

@app.route('/franchises')
def get_franchises():
    """Retrieves all available franchises."""
    return db.wrap_json(db.get_franchises())

@app.route('/regions')
def get_regions():
    """Retrieves all available regions."""
    return db.wrap_json(db.get_regions())