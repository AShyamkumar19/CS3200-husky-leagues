from flask import Blueprint, current_app, request, jsonify, make_response
import json
from src import db

roles = Blueprint('roles', __name__)

# Get all roles from the DB
@roles.route('/roles', methods=['GET'])
def get_roles():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT name, description
                   FROM roles
                   ''')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update information for a specific role
@roles.route('/roles/<roleID>', methods=['PUT'])
def update_specific_role(roleID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   UPDATE roles
                   SET name = %s, description = %s
                   WHERE roleID = %s;
                   ''', (request.json['name'], request.json['description'], roleID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Rule updated'), 200)

# Add a new role to the DB
@roles.route('/roles', methods=['POST'])
def add_role():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   INSERT INTO roles (name, description)
                   VALUES (%s, %s);
                   ''', (request.json['name'], request.json['description']))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New role added'), 200)

# Delete a role from the DB
@roles.route('/roles/<roleID>', methods=['DELETE'])
def delete_role(roleID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE 
                   FROM roles as r
                   WHERE r.roleID = %s;
                   ''', roleID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Role deleted'), 200)

# Get description of a certain role
@roles.route('/roles/<roleID>', methods=['GET'])
def get_role_desc(roleID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT description
                   FROM roles
                   WHERE roleID = %s
                   ''', roleID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update roleID
@roles.route('/roles/<roleID>', methods=['PUT'])
def update_specific_role(roleID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   UPDATE roles
                   SET roleID = %s
                   WHERE roleID = %s;
                   ''', (request.json['roleID'], roleID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Rule updated'), 200)