""" email controller file. """
from flask import request, jsonify
from ..models.db import DatabaseConnection

db = DatabaseConnection()
db.create_db_tables()

class PostController:
    """
    controller class for post.
    """

    def index(self):
        """ function for the index route."""
        return jsonify({
            'message': 'Welcome to the church API site.',
            'status': 200
        }), 200

    