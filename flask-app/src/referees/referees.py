from flask import Blueprint, current_app, request, jsonify, make_response
import json
from src import db

referees = Blueprint('referees', __name__)

# Get all referees from the DB
@referees.route('/referees', methods=['GET'])
def get_referees():
    cursor = db.get_db().cursor()
    cursor.execute('select * from referees')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response 

# Get referee details for a specific game
@referees.route('/referees/<gameID>', methods=['GET'])
def get_game_referee(gameID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT firstName AS First_Name, lastName as 'Last_Name', email
                   FROM referees as r
                   JOIN officiates o ON r.refID = o.refID
                   JOIN games g ON o.gameID = g.gameID
                   WHERE g.gameID = %s;
                   ''', gameID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get details of a referee with a specific refID
@referees.route('/referees/<refID>', methods=['GET'])
def get_referee(refID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT firstName AS First_Name, lastName as 'Last_Name', email
                   FROM referees as r
                   WHERE r.refID = %s;
                   ''', refID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Should refs choosing their game to ref be here?

# # Get all referees for a specific sport
# @referees.route('/referees/<sportID>', methods=['GET'])
# def get_sport_referees(sportID):
#     cursor = db.get_db().cursor()
#     cursor.execute('''
#                    SELECT firstName AS First_Name, lastName as 'Last_Name', email
#                    FROM referees as r
#                    JOIN officiates o ON r.refID = o.refID
#                    JOIN games g ON o.gameID = g.gameID
#                    WHERE g.sportID = %s;
#                    ''', sportID)
#     row_headers = [x[0] for x in cursor.description]
#     json_data = []
#     theData = cursor.fetchall()
#     for row in theData:
#         json_data.append(dict(zip(row_headers, row)))
#     the_response = make_response(jsonify(json_data))
#     the_response.status_code = 200
#     the_response.mimetype = 'application/json'
#     return the_response

# Update referee information for a specific referee
@referees.route('/referees/<refID>', methods=['PUT'])
def update_referee(refID):
    data = request.get_json()
    current_app.logger.info(data)

    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']

    cursor = db.get_db().cursor()

    cursor.execute('''
                   UPDATE referees
                   SET firstName = %s, lastName = %s, email = %s
                   WHERE refID = %s;
                   ''', (firstName, lastName, email, refID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Referee updated'), 200)

# Add a new referee to the DB
@referees.route('/referees', methods=['POST'])
def add_referee():
    cursor = db.get_db().cursor()
    cursor.execute('''
                   INSERT INTO referees (firstName, lastName, email)
                   VALUES (%s, %s, %s);
                   ''', (request.json['firstName'], request.json['lastName'], request.json['email']))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Referee added'), 200)

# Delete a referee from the DB
@referees.route('/referees/<refID>', methods=['DELETE'])
def delete_referee(refID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE r
                   FROM referees as r
                   WHERE r.refID = %s;
                   ''', refID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Referee deleted'), 200)