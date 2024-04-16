from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


fans = Blueprint('fans', __name__)

# Adds a player to the who a fan is following
@fans.route('/fans/<fanID, memberID>', methods=['POST'])
def add_team_member(fanID, memberID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   INSERT INTO fans (fanID, memberID)
                   VALUES (%s, %s);
                   ''', fanID, memberID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New team member followed'), 200)

# Adds a team to who a fan is following
@fans.route('/fans/<fanID, teamID, sportID>', methods=['POST'])
def add_team_member(fanID, teamID, sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   INSERT INTO fans (fanID, teamID, sportID)
                   VALUES (%s, %s);
                   ''', fanID, teamID, sportID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New team followed'), 200)

# Adds a sport to who a fan is following
@fans.route('/fans/<fanID, sportID>', methods=['POST'])
def add_team_member(fanID, sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   INSERT INTO fans (fanID, sportID)
                   VALUES (%s, %s);
                   ''', fanID, sportID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New sport followed'), 200)

# Deletes a fan
@fans.route('/fans/<fanID>', methods=['DELETE'])
def delete_fan(fanID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE 
                   FROM fans as f
                   WHERE f.fanID = %s;
                   ''', fanID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Fan deleted'), 200)

# Updates a fan email
@fans.route('/fans/<fanID>', methods=['PUT'])
def update_specific_role(fanID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   UPDATE fans
                   SET email = %s
                   WHERE fanID = %s;
                   ''', (request.json['email'], fanID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Fan updated'), 200)

# Get all team members a fan follows from the DB
@fans.route('/fans,<fanID>', methods=['GET'])
def get_roles(fanID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT name, description
                   FROM follows_team_members
                   WHERE fanID = %s
                   ''', fanID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response