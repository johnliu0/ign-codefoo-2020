"""
IGN Code Foo 10 Submission

Author: John Liu
Date: Monday, March 10, 2020
"""

tables = {}

"""An item is any piece of entertainment such as a movie, show, or game.
Items can have any number of genres, studios, franchises, publishers, and regions associated with them.
"""
tables['items'] = (
    'CREATE TABLE items ('
    '`id` INT AUTO_INCREMENT PRIMARY KEY,'
    # Game, Movie, Show, Comic
    '`media_type` VARCHAR(10),'
    '`name` VARCHAR(100),'
    '`short_name` VARCHAR(100),'
    '`long_description` VARCHAR(8000),'
    '`short_description` VARCHAR(2000),'
    # create/update timestamps
    '`updated_at` TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),'
    '`created_at` TIMESTAMP NOT NULL DEFAULT NOW(),'
    '`review_url` VARCHAR(300),'
    # to hold review scores from 0.0 to 10.0
    '`review_score` DECIMAL(3, 1),'
    '`slug` VARCHAR(100)'
    ')'
)

"""A genre."""
tables['genres'] = (
    'CREATE TABLE genres ('
    '`name` VARCHAR(50) NOT NULL PRIMARY KEY'
    ')'
)

"""Join table for genre and item."""
tables['genre_item'] = (
    'CREATE TABLE genre_item ('
    '`item_id` INT NOT NULL,'
    '`name` VARCHAR(50) NOT NULL,'
    'PRIMARY KEY(`item_id`, `name`)'
    ')'
)

"""Studios produce items."""
tables['studios'] = (
    'CREATE TABLE studios ('
    '`name` VARCHAR(50) NOT NULL PRIMARY KEY'
    ')'
)

"""Join table for studio and item."""
tables['studio_item'] = (
    'CREATE TABLE studio_item ('
    '`item_id` INT NOT NULL,'
    '`name` VARCHAR(50) NOT NULL,'
    'PRIMARY KEY(`item_id`, `name`)'
    ')'
)

"""Franchises are collections of items."""
tables['franchises'] = (
    'CREATE TABLE franchises ('
    '`name` VARCHAR(50) NOT NULL PRIMARY KEY'
    ')'
)

"""Join table for franchise and item."""
tables['franchise_item'] = (
    'CREATE TABLE franchise_item ('
    '`item_id` INT NOT NULL,'
    '`name` VARCHAR(50) NOT NULL,'
    'PRIMARY KEY(`item_id`, `name`)'
    ')'
)

"""Publishers publish items."""
tables['publishers'] = (
    'CREATE TABLE publishers ('
    '`name` VARCHAR(50) NOT NULL PRIMARY KEY'
    ')'
)

"""Join table for publisher and item."""
tables['publisher_item'] = (
    'CREATE TABLE publisher_item ('
    '`item_id` INT NOT NULL,'
    '`name` VARCHAR(50) NOT NULL,'
    'PRIMARY KEY(`item_id`, `name`)'
    ')'
)

"""Regions are regions that an item are available in."""
tables['regions'] = (
    'CREATE TABLE regions ('
    '`name` VARCHAR(50) NOT NULL PRIMARY KEY'
    ')'
)

"""Join table for region and item."""
tables['region_item'] = (
    'CREATE TABLE region_item ('
    '`item_id` INT NOT NULL,'
    '`name` VARCHAR(50) NOT NULL,'
    'PRIMARY KEY(`item_id`, `name`)'
    ')'
)