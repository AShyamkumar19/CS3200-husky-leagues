from flask import Blueprint, current_app, request, jsonify, make_response
import json
from src import db

sports = Blueprint('sports', __name__)

# Get all sports from the DB
@sports.route('/sports', methods=['GET'])
def get_sports():
    cursor = db.get_db().cursor()
    cursor.execute('select * from sports')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get sport details for a specific sport
@sports.route('/sports/<sportID>', methods=['GET'])
def get_specific_sport(sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT name AS Sport_Name, rules
                   FROM sports as s
                   WHERE s.sportID = %s;
                   ''', sportID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update sport information for a specific sport
@sports.route('/sports/<sportID>', methods=['PUT'])
def update_specific_sport(sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   UPDATE sports
                   SET name = %s, rules = %s
                   WHERE sportID = %s;
                   ''', (request.json['name'], request.json['rules'], sportID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Sport updated'), 200)

# Add a new sport to the DB
@sports.route('/sports', methods=['POST'])
def add_sport():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   INSERT INTO sports (name, rules)
                   VALUES (%s, %s);
                   ''', (request.json['name'], request.json['rules']))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('New Sport added'), 200)

# Delete a sport from the DB
@sports.route('/sports/<sportID>', methods=['DELETE'])
def delete_sport(sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE 
                   FROM sports as s
                   WHERE s.sportID = %s;
                   ''', sportID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Sport deleted'), 200)

# Get all teams for a specific sport
@sports.route('/sports/<sportID>/teams', methods=['GET'])
def get_teams_for_sport(sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT *
                   FROM teams 
                   WHERE teams.sportID = %s;
                   ''', sportID)
    teams = cursor.fetchall()

    cursor = db.get_db().cursor()
    return jsonify(teams)
