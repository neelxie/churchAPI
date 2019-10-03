""" Church controller file. """
from flask import request, jsonify
from ..models.db import DatabaseConnection

db = DatabaseConnection()
db.create_db_tables()

class ChurchController:
    """
    This is a controller class for church.
    """

    def add_church(self):
        """ This method will create a new church."""
        
        data = request.get_json()

        name = data.get("church_name")

        error = self.church_validation.validate_string(name)

        if error is False:
            return jsonify({
                'error': "church name is invalid.",
                "status": 400
            }), 400

        from_token = user_identity()
        created_by = from_token.get('user_id')
        
        church = db.create_church(name, created_by, 'admin')

        return jsonify({
            "status": 201,
            "data": [church]
        }), 201

    def all_churchs(self):
        """ Retrieve all churchs. """

        churchs = db.all_churches()

        if churchs:
            return jsonify({
                "data": [church for church in churchs],
                "status": 200
            }), 200

        return jsonify({
            "status": 404,
            "error": "No churches yet."
        }), 404
