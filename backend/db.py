"""
IGN Code Foo 10 Submission

Author: John Liu
Date: Monday, March 10, 2020
"""

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

def add_table(table_desc):
    """Adds a table to the MySQL database."""
    try:
        db_cursor.execute(table_desc)
    except mysql.connector.Error as err:
        print(f'Table creation failed: {err.msg}')

def get_one_item(id=None, name=None):
    """Searches for a single item by name or id."""
    if id != None:
        db_cursor.execute(f'SELECT * FROM items WHERE id=\'{id}\'')
        return db_cursor.fetchone()
    elif name != None:
        db_cursor.execute(f'SELECT * FROM items WHERE name=\'{name}\'')
        return db_cursor.fetchone()
    else:
        return None

def insert_item(media_type, name, short_name, long_desc, short_desc, review_url, review_score, slug):
    """Inserts an item into the table. Returns the id of the inserted object."""
    cmd = (
        'INSERT INTO items (media_type, name, short_name, long_description, short_description, review_url, review_score, slug) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
    values = (media_type, name, short_name, long_desc, short_desc, review_url, review_score, slug)
    db_cursor.execute(cmd, values)
    mysql_db.commit()
    return db_cursor.lastrowid

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