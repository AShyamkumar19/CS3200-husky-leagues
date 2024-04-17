from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


teams = Blueprint('teams', __name__)

# create a team
@teams.route('/teams', methods=['POST'])
def add_team():
    data = request.get_json()
    current_app.logger.info(data)
    
    name = data['name']
    sportID = data['sportID']
    
    cursor = db.get_db().cursor()

    # create the query
    query = f"INSERT INTO teams (sportID, name) \
              VALUES ({sportID}, {name})"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team created'), 200)

# get all teams
@teams.route('/teams', methods=['GET'])
def get_teamss():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get team names and sport
    query = """SELECT t.sportID, t.teamID, t.name AS 'Team_Name', s.name AS Sport
               FROM teams AS t
               JOIN sports AS s
               ON s.sportID = t.sportID;"""
    
    # use cursor to query the database for a list of games
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))
        
    return make_response(jsonify(json_data), 200)

# get info from a team
@teams.route('/teams/<sportID>/<teamID>', methods=['GET'])
def get_team(teamID, sportID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get the games with the teams names and sport
    query = f"SELECT t.name AS 'Team Name', s.name AS Sport \
               FROM teams AS t \
               JOIN sports AS s \
               ON s.sportID = t.sportID \
               WHERE s.sportID = {sportID} AND t.teamID={teamID};"
    
    # use cursor to query the database for a list of games
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

# update team info
@teams.route('/teams/<teamID>/<sportID>', methods=['PUT'])
def update_team(teamID, sportID):
    data = request.get_json()
    current_app.logger.info(data)
    
    name = data['name']

    cursor = db.get_db().cursor()

    query = f"UPDATE teams \
              SET name={name} \
              WHERE teamID={teamID} AND sportID={sportID}"

    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team updated'), 200)

# delete a team
@teams.route('/teams/<teamID>/<sportID>>', methods=['DELETE'])
def delete_team(teamID, sportID):
    cursor = db.get_db().cursor()

    query = f"DELETE FROM teams \
              WHERE teamID = {teamID} AND sportID={sportID};"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team deleted'), 200)

# add a pre existing team member to a team
@teams.route('/teams', methods=['POST'])
def add_team_member_toteam():
    data = request.get_json()
    current_app.logger.info(data)
    
    teamID = data['teamID']
    sportID = data['sportID']
    memberID = data['memberID']
    jerseyNum = data['jerseyNum']
    roleID = data['roleID']
    
    cursor = db.get_db().cursor()

    # create the query
    query = f"INSERT INTO part_of (sportID, teamID, memberID, jerseyNum, roleID) \
              VALUES ({sportID}, {teamID}, {memberID}, {jerseyNum}, {roleID})"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team created'), 200)

# delete a member from a team
@teams.route('/teams/<teamID>/<sportID>/<memberID>', methods=['DELETE'])
def delete_team_member_onteam(teamID, sportID, memberID):
    cursor = db.get_db().cursor()

    query = f"DELETE FROM part_of \
              WHERE teamID = {teamID} AND sportID={sportID} AND memberID={memberID};"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team member deleted'), 200)

# get all teams for a specific sport
@teams.route('/teams/<sportID>', methods=['GET'])
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