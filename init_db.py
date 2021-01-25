"""
    helper script - run this to re-initialize the database (overwrites any existing db.sqlite)
"""

from app import db, create_app
db.create_all(app=create_app())
