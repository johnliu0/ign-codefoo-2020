"""
IGN Code Foo 10 Submission

Author: John Liu
Date: Monday, March 10, 2020
"""

import html
import time
import db
from datetime import datetime
from tables import tables
import csv
import mysql.connector

class CSVReader:
    """Utility for importing CSV files according of the form:
    ['id', 'media_type', 'name', 'short_name', 'long_description', 'short_description', 
    'created_at', 'updated_at', 'review_url', 'review_score', 'slug', 'genres',
    'created_by', 'published_by', 'franchises', 'regions']

    CSVReader loads and sanitizes this data before placing it in a MySQL database.

    Usage:
        csv_reader = CSVReader()
        csv_reader.load('cfgames.csv')
    """

    def __init__(self, mysql_db):
        """Initializes the reader."""
        # these headers were manually extracted from the csv
        self.mysql_db = mysql_db
        self.header_data = ['id', 'media_type', 'name', 'short_name', 'long_description', 'short_description', 'created_at', 'updated_at', 'review_url', 'review_score', 'slug', 'genres', 'created_by', 'published_by', 'franchises', 'regions']
    
    def parse_list(self, s):
        """Parses a list from the CSV.
        Lists are in the form {x,y,z}
        """
        
        if len(s) <= 2:
            return []
        if s[0] != '{' or s[-1] != '}':
            return []
        # extract the body of the string; exclude the braces
        data = s[1:-1]
        # extract tokens with a comma delimiter
        tokens = []
        token = ''
        for c in data:
            if c == ',':
                # remove leading and trailing whitespace before appending
                tokens.append(token.strip())
                token = ''
            else:
                token += c
        if len(token) != 0:
            tokens.append(token)
        return tokens

    def load(self, file_name):
        """Loads a CSV file."""

        for table in tables:
            db.add_table(tables[table])

        body_data = []
        with open(file_name, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            # skip header
            next(reader)
            # read body data
            for row in reader:
                body_data.append(row)
        
        # header data is of the form; this is manually taken from the csv file
        # 0: 'id'
        # 1: 'media_type'
        # 2: 'name'
        # 3: 'short_name'
        # 4: 'long_description'
        # 5: 'short_description'
        # 6: 'created_at'
        # 7: 'updated_at'
        # 8: 'review_url'
        # 9: 'review_score'
        # 10: 'slug'
        # 11: 'genres'
        # 12: 'created_by'
        # 13: 'published_by'
        # 14: 'franchises'
        # 15: 'regions'
         
        # for the strings, the following characters must be escaped: < > ' " &
        # for header indices 11 through 15, these are lists of comma separated data surrounded by curly braces
        # these must be separated and put in the appropriate MySQL table

        # process each row
        for row in body_data:
            # id is skipped as a new id will be created by MySQL
            # media type is a simple string: 'Movie', 'Show', 'Comic'
            media_type = row[1]
            # full name of the item
            name = html.escape(row[2])
            # shortened name of the item
            short_name = html.escape(row[3])
            # short and long descriptions are both raw HTML elements and must be escaped for safety
            long_desc = html.escape(row[4])
            short_desc = html.escape(row[5])
            # create/update timestamps are not extracted as they will be automatically inserted by MySQL
            # the link is escaped as well for safety; though this may cause corruption
            review_url = html.escape(row[8])
            # the review score is a decimal number from 0.0 to 10.0
            review_score = float(row[9])
            # extract the slug
            slug = html.escape(row[10])
            # parse the list of genres
            genres = self.parse_list(row[11])
            # parse the list of studios
            studios = self.parse_list(row[12])
            # parse the list of publishers
            publishers = self.parse_list(row[13])
            # parse the list of franchises
            franchises = self.parse_list(row[14])
            # parse the list of regions
            regions = self.parse_list(row[15])

            # check if this item already exists by name
            if db.get_one_item(name=name) != None:
                continue

            item_id = db.insert_item(media_type, name, short_name, long_desc, short_desc, review_url, review_score, slug)
            db.insert_genre_item_joins(genres, item_id)
            db.insert_studio_item_joins(studios, item_id)
            db.insert_publisher_item_joins(publishers, item_id)
            db.insert_franchise_item_joins(franchises, item_id)
            db.insert_region_item_joins(regions, item_id)

if __name__ == '__main__':
    mysql_db = db.connect_database()
    csv_reader = CSVReader(mysql_db)
    csv_reader.load('cfgames.csv')
    db.close()