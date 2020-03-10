"""
IGN Code Foo 10 Submission

Author: John Liu
Date: Monday, March 10, 2020
"""

from decimal import Decimal
import mysql.connector

global mysql_db
global db_cursor

def connect_database():
    """Connects to the MySQL database and returns a usable DB object."""
    global mysql_db
    global db_cursor
    # of course these values should be extracted out into .env files for production use
    mysql_db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password1234',
        auth_plugin='mysql_native_password',
        db='igncodefoo'
    )

    db_cursor = mysql_db.cursor()

    return mysql_db

def close():
    """Shutdown MySQL connection."""
    mysql_db.close()

def to_json(data, desc):
    """Converts a fetch query data and its description to a JSON-compatible dict.
    Usage:
        After calling a fetch using the cursor, e.g. data = db_cursor.fetchall()
        Then use to_json(data, db_cursor.description)
    """
    headers = [x[0] for x in db_cursor.description]
    # wrap data in a tuple if it is not already
    # this is since the data will be iterated over
    # however, whether or not the data was originally a list will
    # be noted for use later for the return
    is_list = True
    if isinstance(data, tuple):
        data = (data,)
        is_list = False
    
    # iterate through each element in data and each header and add it to a JSON dict
    json_data = []
    for elem in data:
        json_dict = {}
        for idx, header in enumerate(headers):
            if isinstance(elem[idx], Decimal):
                # Decimal objects are not JSON serializable and must be returned as a float
                json_dict[header] = float(elem[idx])
            else:
                json_dict[header] = elem[idx]
        json_data.append(json_dict)
    # appropriately return either a single object or list depending on the original data
    return json_data if is_list else json_data[0]

def wrap_json(data):
    """Wraps JSON data into a standarized envelope for consistency."""
    return { 'data': data }

def add_table(table_desc):
    """Adds a table to the MySQL database."""
    try:
        db_cursor.execute(table_desc)
    except mysql.connector.Error as err:
        print(f'Table creation failed: {err.msg}')

def insert_item(media_type, name, short_name, long_desc, short_desc, review_url, review_score, slug):
    """Inserts an item into the table. Returns the id of the inserted object."""
    cmd = (
        'INSERT INTO items (media_type, name, short_name, long_description, short_description, review_url, review_score, slug) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
    values = (media_type, name, short_name, long_desc, short_desc, review_url, review_score, slug)
    db_cursor.execute(cmd, values)
    mysql_db.commit()
    return db_cursor.lastrowid

def get_items(mediatype=None, reviewmin=3, reviewmax=5.0, sort='nameasc'):
    """Queries for multiple items.
    
    Allowed Parameters:
        mediatype: can be one of 'Movie', 'Show', 'Comic', or 'Game', defaults to none
        reviewmin: minimum review score (inclusive)
        reviewmax: maximum review score (inclusive)
        sort: can be 'nameasc', 'namedesc', 'reviewasc', or reviewdesc'
    """

    # build initial command
    cmd = (
        'SELECT * '
        'FROM items '
        'WHERE ')
    
    # generate where clauses
    where_clauses = [
        f'review_score >= {reviewmin}',
        f'review_score <= {reviewmax}']
    if mediatype != None:
        where_clauses.append(f'media_type = \'{mediatype}\'')
    
    # connect where clauses with the AND
    cmd += ' AND '.join(where_clauses) + ' '
    
    # check for sorting type
    if sort == 'namedesc':
        cmd += 'ORDER BY name DESC'
    elif sort == 'reviewasc':
        cmd += 'ORDER BY review_score ASC'
    elif sort == 'reviewdesc':
        cmd += 'ORDER BY review_score DESC'
    else:
        cmd += 'ORDER BY name ASC'

    db_cursor.execute(cmd)
    items = db_cursor.fetchall()
    return to_json(items, db_cursor.description)

def get_one_item(id=None, name=None):
    """Searches for a single item by name or id."""
    # admittedly, I have little experience with SQL; I'm much more accustomed to NoSQL database such as MongoDB
    # this is likely not an optimal way of referencing other tables

    # selects genres, an item may have 0 or more genres
    cmd_genres = (f'SELECT g.* FROM items i INNER JOIN genre_item gi ON gi.item_id = i.id INNER JOIN genres g ON g.name = gi.name WHERE i.name = \'{name}\'')
    db_cursor.execute(cmd_genres)
    fetch = db_cursor.fetchall()
    # an empty search will return None; which should be an empty list, otherwise extract the elements
    genres = [elem[0] for elem in fetch] if fetch != None else []
    
    cmd_studios = (f'SELECT s.* FROM items i INNER JOIN studio_item si ON si.item_id = i.id INNER JOIN studios s ON s.name = si.name WHERE i.name = \'{name}\'')
    db_cursor.execute(cmd_studios)
    fetch = db_cursor.fetchall()
    studios = [elem[0] for elem in fetch] if fetch != None else []

    cmd_publishers = (f'SELECT p.* FROM items i INNER JOIN publisher_item pi ON pi.item_id = i.id INNER JOIN publishers p ON p.name = pi.name WHERE i.name = \'{name}\'')
    db_cursor.execute(cmd_publishers)
    fetch = db_cursor.fetchall()
    publishers = [elem[0] for elem in fetch] if fetch != None else []

    cmd_franchises = (f'SELECT f.* FROM items i INNER JOIN franchise_item fi ON fi.item_id = i.id INNER JOIN franchises f ON f.name = fi.name WHERE i.name = \'{name}\'')
    db_cursor.execute(cmd_franchises)
    fetch = db_cursor.fetchall()
    franchises = [elem[0] for elem in fetch] if fetch != None else []
    
    cmd_regions = (f'SELECT r.* FROM items i INNER JOIN region_item ri ON ri.item_id = i.id INNER JOIN regions r ON r.name = ri.name WHERE i.name = \'{name}\'')
    db_cursor.execute(cmd_regions)
    fetch = db_cursor.fetchall()
    regions = [elem[0] for elem in fetch] if fetch != None else []

    # finally query the item itself
    cmd = (f'SELECT * FROM items WHERE id=\'{id}\' OR name=\'{name}\' ')
    db_cursor.execute(cmd)
    item = db_cursor.fetchone()
    if item == None:
        return {}
    
    # attach the other fields to the item
    json_item = to_json(item, db_cursor.description)
    json_item['genres'] = genres
    json_item['studios'] = studios
    json_item['publishers'] = publishers
    json_item['franchises'] = franchises
    json_item['regions'] = regions
    return json_item

def insert_genre_item_joins(genres, item_id):
    """Inserts a list of genres associated with an item."""
    if len(genres) == 0:
        return

    # first insert the genres to ensure they exist
    try:
        cmd = ('INSERT INTO genres (name) VALUES (%s)')
        db_cursor.executemany(cmd, [(g,) for g in genres])
        mysql_db.commit()
    except:
        # quick fix for catching duplicate key error
        pass

    # then insert the join
    cmd = ('INSERT INTO genre_item (item_id, name) VALUES (%s, %s)')
    values = [(item_id, g) for g in genres]
    db_cursor.executemany(cmd, values)
    mysql_db.commit()

def get_genres():
    """Fetches available genres."""
    db_cursor.execute('SELECT * FROM genres')
    genres = db_cursor.fetchall()
    return to_json(genres, db_cursor.description)

def insert_studio_item_joins(studios, item_id):
    """Inserts a list of studios associated with an item."""
    if len(studios) == 0:
        return
    
    # first insert the studios to ensure they exist
    try:
        cmd = ('INSERT INTO studios (name) VALUES (%s)')
        db_cursor.executemany(cmd, [(s,) for s in studios])
        mysql_db.commit()
    except:
        # quick fix for catching duplicate key error
        pass

    # then insert the join
    cmd = ('INSERT INTO studio_item (item_id, name) VALUES (%s, %s)')
    values = [(item_id, s) for s in studios]
    db_cursor.executemany(cmd, values)
    mysql_db.commit()

def get_studios():
    """Fetches available studios."""
    db_cursor.execute('SELECT * FROM studios')
    studios = db_cursor.fetchall()
    return to_json(studios, db_cursor.description)

def insert_publisher_item_joins(publishers, item_id):
    """Inserts a list of publishers associated with an item."""
    if len(publishers) == 0:
        return

    # first insert the publishers to ensure they exist
    try:
        cmd = ('INSERT INTO publishers (name) VALUES (%s)')
        db_cursor.executemany(cmd, [(p,) for p in publishers])
        mysql_db.commit()
    except:
        # quick fix for catching duplicate key error
        pass

    # then insert the join
    cmd = ('INSERT INTO publisher_item (item_id, name) VALUES (%s, %s)')
    values = [(item_id, p) for p in publishers]
    db_cursor.executemany(cmd, values)
    mysql_db.commit()

def get_publishers():
    """Fetches available publishers."""
    db_cursor.execute('SELECT * FROM publishers')
    publishers = db_cursor.fetchall()
    return to_json(publishers, db_cursor.description)

def insert_franchise_item_joins(franchises, item_id):
    """Inserts a list of franchises associated with an item."""
    if len(franchises) == 0:
        return

    # first insert the franchises to ensure they exist
    try:
        cmd = ('INSERT INTO franchises (name) VALUES (%s)')
        db_cursor.executemany(cmd, [(f,) for f in franchises])
        mysql_db.commit()
    except:
        # quick fix for catching duplicate key error
        pass

    # then insert the join
    cmd = ('INSERT INTO franchise_item (item_id, name) VALUES (%s, %s)')
    values = [(item_id, f) for f in franchises]
    db_cursor.executemany(cmd, values)
    mysql_db.commit()

def get_franchises():
    """Fetches available franchises."""
    db_cursor.execute('SELECT * FROM franchises')
    franchises = db_cursor.fetchall()
    return to_json(franchises, db_cursor.description)

def insert_region_item_joins(regions, item_id):
    """Inserts a list of regions associated with an item."""
    if len(regions) == 0:
        return

    # first insert the regions to ensure they exist
    try:
        cmd = ('INSERT INTO regions (name) VALUES (%s)')
        db_cursor.executemany(cmd, [(r,) for r in regions])
        mysql_db.commit()
    except:
        # quick fix for catching duplicate key error
        pass

    # then insert the join
    cmd = ('INSERT INTO region_item (item_id, name) VALUES (%s, %s)')
    values = [(item_id, r) for r in regions]
    db_cursor.executemany(cmd, values)
    mysql_db.commit()

def get_regions():
    """Fetches available regions."""
    db_cursor.execute('SELECT * FROM regions')
    regions = db_cursor.fetchall()
    return to_json(regions, db_cursor.description)