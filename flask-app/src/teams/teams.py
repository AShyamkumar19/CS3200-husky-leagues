from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


teams = Blueprint('teams', __name__)

# create a team

# get info from a team

# update team info

# delete a team

# add a pre existing team member to a team

# delete a member from a team
@teams.route('/team_members/<memberID>', methods=['DELETE'])
def delete_team_member(teamID, sportID, memberID):
    cursor = db.get_db().cursor()

    query = f"DELETE FROM part_of
              WHERE teamID = {teamID} AND sportID={sportID} AND memberID={memberID};"
    
    cursor.execute(query)
    
    cursor = db.get_db().commit()

    return make_response(jsonify('Team member deleted'), 200)