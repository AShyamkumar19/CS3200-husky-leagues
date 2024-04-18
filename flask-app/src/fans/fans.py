from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


fans = Blueprint('fans', __name__)

# Adds a player to the who a fan is following
@fans.route('/fans/<fanID>/<memberID>', methods=['POST'])
def add_fan_player(fanID, memberID):
    cursor = db.get_db().cursor()
    cursor.execute(f"INSERT INTO follows_team_members (fanID, memberID) VALUES ({fanID}, {memberID})")
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New team member followed'), 200)

# Adds a team to who a fan is following
@fans.route('/fans/<fanID>/<teamID>/<sportID>', methods=['POST'])
def add_fan_team(fanID, teamID, sportID):
    cursor = db.get_db().cursor()
    cursor.execute(f"INSERT INTO follows_teams (fanID, teamID, sportID) VALUES ({fanID}, {teamID}, {sportID}); ")
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New team followed'), 200)

# Adds a sport to who a fan is following
@fans.route('/fans_sport/<fanID>/<sportID>', methods=['POST'])
def add_fan_sport(fanID, sportID):
    cursor = db.get_db().cursor()
    cursor.execute(f"INSERT INTO follows_sports (fanID, sportID) VALUES ({fanID}, {sportID});")
    
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
def update_specific_fan(fanID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   UPDATE fans
                   SET email = %s
                   WHERE fanID = %s;
                   ''', (request.json['email'], fanID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Fan updated'), 200)

# Get all team members a fan follows from the DB
@fans.route('/fans/<fanID>', methods=['GET'])
def get_team_members_fan(fanID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT firstName, lastName, email
                   FROM follows_team_members
                   JOIN team_members
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

# Get all fans
@fans.route('/fans', methods=['GET'])
def get_fans():
    cursor = db.get_db().cursor()
    cursor.execute(" SELECT fanID, firstName, lastName FROM fans ")
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response