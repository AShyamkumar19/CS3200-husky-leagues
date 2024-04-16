from flask import Blueprint, current_app, request, jsonify, make_response
import json
from src import db

team_members = Blueprint('team_members', __name__)

# Get all team members from the DB
@team_members.route('/team_members', methods=['GET'])
def get_team_members():
    cursor = db.get_db().cursor()
    cursor.execute('select * from team_members')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get team member detail for a specific team 
@team_members.route('/team_members/<teamID>, <sportID>', methods=['GET'])
def get_specific_team_members(teamID, sportID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT firstName AS First_Name, lastName as 'Last_Name', email
                   FROM team_members as tm
                   JOIN part_of pf ON tm.memberID = pf.memberID
                   JOIN teams t ON pf.teamID = t.teamID
                   WHERE t.teamID =%s and t.sportID = %s;
                   ''', (teamID, sportID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get details of a team member with a specific memberID
@team_members.route('/team_members/<memberID>', methods=['GET'])
def get_team_member(memberID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT firstName AS First_Name, lastName as 'Last_Name', email
                   FROM team_members as tm
                   WHERE tm.memberID = %s;
                   ''', memberID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update information of any of the attributes in team_members
@team_members.route('/team_members/<memberID>', methods=['PUT'])
def update_team_member(memberID):
    data = request.get_json()
    current_app.logger.info(data)
    
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    cursor = db.get_db().cursor()

    cursor.execute('''
                   UPDATE team_members
                   SET firstName = %s, lastName = %s, email = %s
                   WHERE memberID = %s;
                   ''', (first_name, last_name, email, memberID))
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team member updated'), 200)

# Delete a team member from team
@team_members.route('/team_members/<memberID>', methods=['DELETE'])
def delete_team_member(teamID, sportID, memberID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE tm
                   FROM team_members as tm
                   JOIN part_of po ON tm.memberID = po.memberID
                   JOIN teams t ON po.teamID = t.teamID
                   WHERE t.teamID = %s AND t.sportID = %s AND tm.memberID = %s;
                   ''', (teamID, sportID, memberID))
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team member deleted'), 200)

# Add a new team member to the team_members table
@team_members.route('/team_members', methods=['POST'])
def add_team_member():
    data = request.get_json()
    current_app.logger.info(data)
    
    team_id = data['team_id']
    sport_id = data['sport_id']
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']

    cursor = db.get_db().cursor()

    cursor.execute('''
                   INSERT INTO team_members (team_id, sport_id, first_name, last_name, email)
                   VALUES (%s, %s, %s, %s, %s);
                   ''', (team_id, sport_id, first_name, last_name, email))
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team member added'), 200)