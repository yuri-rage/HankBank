"""
    helper script - run this to re-initialize the database
"""

from app import db, create_app
db.create_all(app=create_app())
