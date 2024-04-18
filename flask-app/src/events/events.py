from flask import Blueprint, current_app, request, jsonify, make_response
import json
from src import db

events = Blueprint('events', __name__)

# Get all events from the DB
@events.route('/events', methods=['GET'])
def get_events():
    cursor = db.get_db().cursor()
    cursor.execute('select * from events')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get event details for a specific event
@events.route('/events/<eventID>', methods=['GET'])
def get_specific_event(eventID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT e
                   FROM events as e
                   WHERE e.eventID = %s;
                   ''', eventID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all events from a specific sponsor
@events.route('/events/<sponsorID>', methods=['GET'])
def get_sponsor_events(sponsorID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   SELECT *
                   FROM events
                   WHERE sponsorID = %s;
                   ''', sponsorID)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update event information for a specific event
@events.route('/events/<eventID>', methods=['PUT'])
def update_specific_event(eventID):
    data = request.get_json()
    current_app.logger.info(data)

    description = data['description']
    dateTime = data['dateTime']
    location = data['location']
    sponsorID = data['sponsorID']

    cursor = db.get_db().cursor()

    cursor.execute('''
                   UPDATE events
                   SET description = %s, dateTime = %s, location = %s, sponsorID = %s
                   WHERE eventID = %s;
                   ''', (description, dateTime, location, sponsorID, eventID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Event updated'), 200)

# Add a new event to the DB
@events.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    current_app.logger.info(data)

    description = data['description']
    dateTime = data['dateTime']
    location = data['location']
    sponsorID = data['sponsorID']

    cursor = db.get_db().cursor()

    cursor.execute('''
                   INSERT INTO events (description, dateTime, location, sponsorID)
                   VALUES (%s, %s, %s, %s);
                   ''', (description, dateTime, location, sponsorID))
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Event added'), 201)

# Delete an event from the DB
@events.route('/events/<eventID>', methods=['DELETE'])
def delete_event(eventID):
    cursor = db.get_db().cursor()
    cursor.execute('''
                   DELETE e
                   FROM events as e
                   WHERE e.eventID = %s;
                   ''', eventID)
    
    cursor = db.get_db().commit()
    return make_response(jsonify('Event deleted'), 200)