from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


sponsors = Blueprint('sponsors', __name__)

# Get all sponsors
@sponsors.route('/sponsors', methods=['GET'])
def get_sponsors():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get sponsors
    query = """SELECT * FROM sponsors"""
    
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

# Delete a sponsor
@sponsors.route('/sponsors/<sponsorID>', methods=['DELETE'])
def delete_sponsor(sponsorID):
    cursor = db.get_db().cursor()

    query = f"DELETE FROM sponsors \
              WHERE teamID = {sponsorID};"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Sponsor deleted'), 200)

# add a sponsor
@sponsors.route('/sponsors', methods=['POST'])
def add_sponsor():
    data = request.get_json()
    current_app.logger.info(data)
    
    name = data['name']
    email = data['email']
    
    cursor = db.get_db().cursor()

    # create the query
    query = f"INSERT INTO sponsors (name, email) \
              VALUES ({name}, {email})"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Sponsor created'), 200)

# edit info for a specific sponsor
@sponsors.route('/teams/<sponsorID>', methods=['PUT'])
def update_sponsor(sponsorID):
    data = request.get_json()
    current_app.logger.info(data)
    
    name = data['name']
    email = data['email']

    cursor = db.get_db().cursor()

    query = f"UPDATE sponsors \
              SET name={name}, email={email} \
              WHERE sponsorID={sponsorID}"

    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team updated'), 200)


# get info for a specific sponsor
@sponsors.route('/sponsors/<sponsorID>', methods=['GET'])
def get_sponsor(sponsorID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get sponsors
    query = f"SELECT * FROM sponsors \
               WHERE sponsorID={sponsorID}"
    
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

# Return sponsorship info for a specific sponsor
@sponsors.route('/sponsors/<sponsorID>', methods=['GET'])
def get_sponsorship_sponsor(sponsorID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get sponsors
    query = f"SELECT s1.name, t.name, s2.name, s3.money \
              FROM sponsors AS s1 \
              JOIN sponsorships AS s3 ON s1.sponsorID = s3.sponsorID \
              JOIN teams AS t ON t.teamID = s3.teamID AND t.sportID = s3.sportID \
              JOIN sports AS s2 ON t.sportID = s2.sportID \
              WHERE s1.sponsorID={sponsorID}"
    
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

# Return info for a specific sponsorship
@sponsors.route('/sponsorship/<sponsorID>/<teamID>/<sportID>', methods=['GET'])
def get_sponsorship(sponsorID, teamID, sportID):
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get sponsors
    query = f"SELECT s1.name, t.name, s2.name, s3.money \
              FROM sponsors AS s1 \
              JOIN sponsorships AS s3 ON s1.sponsorID = s3.sponsorID \
              JOIN teams AS t ON t.teamID = s3.teamID AND t.sportID = s3.sportID \
              JOIN sports AS s2 ON t.sportID = s2.sportID \
              WHERE s3.sponsorID={sponsorID} AND s3.teamID={teamID} AND s3.sportID={sportID}"
    
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

# Update info for a specific sponsorship
@sponsors.route('/sponsorships/<sponsorID>/<teamID>/<sportID>', methods=['PUT'])
def update_sponsorship(sponsorID, teamID, sportID):
    data = request.get_json()
    current_app.logger.info(data)
    
    money = data['money']

    cursor = db.get_db().cursor()

    query = f"UPDATE sponsorships \
              SET money={money} \
              WHERE sponsorID={sponsorID} AND sportID={sportID} AND teamID={teamID}"

    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Sponsorship updated'), 200)

# add a sponsorship
@sponsors.route('/sponsorships', methods=['POST'])
def add_sponsorship():
    data = request.get_json()
    current_app.logger.info(data)
    
    sponsorID = data['sponsorID']
    teamID = data['teamID']
    sportID = data['sportID']
    money = data['money']
    
    cursor = db.get_db().cursor()

    # create the query
    query = f"INSERT INTO sponsorship (sponsorID, teamID, sportID, money) \
              VALUES ({sponsorID}, {teamID}, {sportID}, {money})"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Sponsor created'), 200)