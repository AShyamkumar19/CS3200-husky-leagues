from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


games = Blueprint('games', __name__)

# Get all the games from the database
@games.route('/games', methods=['GET'])
def get_products():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get the games with the teams names and sport
    query = """SELECT g.gameID AS gameID, g.dateTime AS dateTime, g.location AS location, t1.name AS 'Team 1',
            g.team1_score AS 'Team 1 Score', t2.name AS 'Team 2', g.team2_score AS 'Team 2 Score', s.name AS Sport
            FROM games AS g 
            JOIN teams AS t1 ON g.team1_ID = t1.teamID AND g.team1_sportID = t1.sportID
            JOIN teams AS t2 ON g.team2_ID = t2.teamID AND g.team2_sportID = t2.sportID
            JOIN sports AS s ON s.sportID = t1.sportID;"""
    
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

# Add a new team member to the team_members table
@games.route('/games', methods=['POST'])
def add_team_member():
    data = request.get_json()
    current_app.logger.info(data)
    
    dateTime = data['dateTime']
    location = data['location']
    team1_id = data['team1_id']
    team1_sportID = data['team1_sportID']
    team2_id = data['team2_id']
    team2_sportID = data['team2_sportID']

    cursor = db.get_db().cursor()

    # create the query
    query = f"INSERT INTO games (dateTime, location, team1_ID, team2_ID, team1_sportID, team2_sportID)
              VALUES ({dateTime}, {location}, {team1_id}, {team2_id}, {team1_sportID}, {team2_sportID})"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Game created'), 200)

# Update a specific game
@games.route('/games/<gameID>', methods=['PUT'])
def update_game(gameID):
    data = request.get_json()
    current_app.logger.info(data)
    
    dateTime = data['dateTime']
    location = data['location']
    team1_ID = data['team1_ID']
    team1_sportID = data['team1_sportID']
    team1_score = data['team1_score']
    team2_ID = data['team2_ID']
    team2_sportID = data['team2_sportID']
    team2_score = data['team2_score']

    cursor = db.get_db().cursor()

    query = f"UPDATE games
              SET dateTime = {dateTime}, location = {location}, team1_ID = {team1_ID}, team1_sportID = {team1_sportID}, team1_score = {team1_score},
              team2_ID = {team2_ID}, team2_sportID = {team2_sportID}, team2_score = {team2_score}
              WHERE gameID = {gameID}"

    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Game updated'), 200)

# Delete a game
@games.route('/team_members/<gameID>', methods=['DELETE'])
def delete_team_member(gameID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE FROM games
                   WHERE gameID = %s;
                   ''', (gameID))
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Game deleted'), 200)

# Get all the games for a specific sport
@games.route('/games/<sportID>', methods=['GET'])
def get_products(sportID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get the games with the teams names and sport
    query = f"SELECT g.gameID AS gameID, g.dateTime AS dateTime, g.location AS location, t1.name AS 'Team 1',
            g.team1_score AS 'Team 1 Score', t2.name AS 'Team 2', g.team2_score AS 'Team 2 Score', s.name AS Sport
            FROM games AS g 
            JOIN teams AS t1 ON g.team1_ID = t1.teamID AND g.team1_sportID = t1.sportID
            JOIN teams AS t2 ON g.team2_ID = t2.teamID AND g.team2_sportID = t2.sportID
            JOIN sports AS s ON s.sportID = t1.sportID
            WHERE g.team1_sportID = {sportID} AND g.team2_sportID = {sportID};"
    
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

# Get info for a specific game
@games.route('/games/<gameID>', methods=['GET'])
def get_products(gameID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get the games with the teams names and sport
    query = f"SELECT g.gameID AS gameID, g.dateTime AS dateTime, g.location AS location, t1.name AS 'Team 1',
            g.team1_score AS 'Team 1 Score', t2.name AS 'Team 2', g.team2_score AS 'Team 2 Score', s.name AS Sport
            FROM games AS g 
            JOIN teams AS t1 ON g.team1_ID = t1.teamID AND g.team1_sportID = t1.sportID
            JOIN teams AS t2 ON g.team2_ID = t2.teamID AND g.team2_sportID = t2.sportID
            JOIN sports AS s ON s.sportID = t1.sportID
            WHERE g.gameID = {gameID};"
    
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

# Get all the games for a team
@games.route('/games/<teamID>/<sportID>', methods=['GET'])
def get_products(teamID, sportID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get the games with the teams names and sport
    query = f"SELECT g.gameID AS gameID, g.dateTime AS dateTime, g.location AS location, t1.name AS 'Team 1',
            g.team1_score AS 'Team 1 Score', t2.name AS 'Team 2', g.team2_score AS 'Team 2 Score', s.name AS Sport
            FROM games AS g 
            JOIN teams AS t1 ON g.team1_ID = t1.teamID AND g.team1_sportID = t1.sportID
            JOIN teams AS t2 ON g.team2_ID = t2.teamID AND g.team2_sportID = t2.sportID
            JOIN sports AS s ON s.sportID = t1.sportID
            WHERE g.team1_sportID = {sportID} AND g.team2_sportID = {sportID} AND (g.team1_ID = {teamID} OR g.team2_ID = {teamID});"
    
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