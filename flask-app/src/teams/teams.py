# create a team

# get info from a team

# update team info

# delete a team

# add a pre existing team member to a team

# delete a member from a team


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