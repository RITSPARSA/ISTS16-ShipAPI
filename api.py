from flask import Flask, request, jsonify, Response
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.ext.limiter import Limiter, HEADERS
from pathlib import Path
import datetime, os, sys

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/teams.db'.format(dir_path)
db = SQLAlchemy(app)

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'whiteteam' and password == 'secret'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'YOU SHALL NOT PASS.\n', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'}),
    

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

class Teams(db.Model):
    id = db .Column(db.Integer, primary_key=True)
    teamNum = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(50), unique=True)
    light = db.Column(db.Integer)
    medium = db.Column(db.Integer)
    heavy = db.Column(db.Integer)
    # ratelimit = db.Column(db.Integer, nullable=True)

# WHITETEAM = Teams.query.filter_by(teamNum=999).first()

limiter = Limiter(
    app,
    headers_enabled=True, 
    key_func=get_remote_address,
    default_limits=["1/{}minute".format(5)]
)

# @app.route('/ratelimit', methods=['POST'])
# @requires_auth
# def change_ratelimit():
#     data = request.get_json()
#     team = Teams.query.filter_by(teamNum=999).first()
#     team.ratelimit = data['ratelimit']
#     db.session.commit()
#     return jsonify({'message' : 'Team {} - {} created'.format(data['teamNum'], data['name'])})

"""
Creates a new team in the database with zeroed ships
Whiteteam authenticated

URL: 
    curl -v -H "Content-Type: application/json" -X POST -d '{"teamNum" : [TEAM NUMBER], "name" : "[TEAM NAME]"}' http://127.0.0.1:5000/createteam
Method: 
    POST
Data: 
    teamNum(integer)- the team number
    name(string) - the team name

    {"teamNum" : 2, "name" : "Blue Team 2"}
Return: 
    {
    'message': 'Team 2 - Blue Team 2 created'
    }
"""
@app.route('/createteam', methods=['POST'])
@requires_auth
def create_team():
    data = request.get_json()
    new_team = Teams(teamNum=data['teamNum'], name=data['name'], light=0, medium=0, heavy=0, ratelimit=null)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message' : 'Team {} - {} created'.format(data['teamNum'], data['name'])})


"""
Deletes an existing team in the database 
Whiteteam authenticated

URL: 
    curl -v -X DELETE http://127.0.0.1:5000/deleteteam/<teamNum>
Method: 
    DELETE
Data: 
    teamNum(integer)- the team number
Return:
    {
    'message': 'Team 2 deleted'
    }
"""
@app.route('/deleteteam/<teamNum>', methods=['DELETE'])
@requires_auth
def delete_team(teamNum): 
    team = Teams.query.filter_by(teamNum=teamNum).first()

    if not team:
        return jsonify({'message' : 'Team {} NOT found!'.format(teamNum)})

    db.session.delete(team)
    db.session.commit()
    return jsonify({'message' : 'Team {} deleted'.format(teamNum)})

"""
Returns JSON of all the teams in the database
White team authenticated

URL: 
    curl -v http://127.0.0.1:5000/teams
Method: 
    GET
Data: 
    N/A
Return:
{
    "teams": [
        {
            "heavy": 0,
            "id": 1,
            "light": 0,
            "medium": 0,
            "name": "Blue Team 2",
            "teamNum": 2
        },
        {
            "heavy": 0,
            "id": 3,
            "light": 0,
            "medium": 0,
            "name": "Blue Team 3",
            "teamNum": 3
        },
"""
@app.route('/teams', methods=['GET'])
@requires_auth
@limiter.exempt
def get_all_teams():
    teams = Teams.query.all()
    output = []
    for team in teams:
        team_data = {}
        team_data['teamNum'] = team.teamNum
        team_data['name'] = team.name
        team_data['id'] = team.id
        team_data['light'] = team.light
        team_data['medium'] = team.medium
        team_data['heavy'] = team.heavy
        output.append(team_data)
    return jsonify({'teams': output})

"""
Returns JSON of the team requested
White team authenticated

URL: 
    curl -v http://127.0.0.1:5000/teams/<teamNum>
Method: 
    GET
Data: 
    N/A
Return:
{
    "teams": [
        {
            "heavy": 0,
            "id": 1,
            "light": 0,
            "medium": 0,
            "name": "Blue Team 2",
            "teamNum": 2
        }]
}
"""
@app.route('/teams/<teamNum>', methods=['GET'])
@requires_auth
@limiter.exempt
def get_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'message' : 'Team {} - {} NOT found!'.format(data['teamNum'], data['name'])})

    team_data = {}
    team_data['teamNum'] = team.teamNum
    team_data['name'] = team.name
    team_data['id'] = team.id
    team_data['light'] = team.light
    team_data['medium'] = team.medium
    team_data['heavy'] = team.heavy
    return jsonify({'team' : team_data})

"""
Overrides any ship's count
White team authenticated

URL: 
    curl -v -H "Content-Type: application/json" -X POST -d '{'light' : [COUNT], 'medium' : [COUNT], 'heavy' : [COUNT]}' http://127.0.0.1:5000/teams/<teamNum>
Method: 
    POST
Data: 
    light - light ship count
    medium - medium ship count
    heavy - heavy ship count

    {'light' : 2, 'medium' : 0, 'heavy' : 3}
Return:
    {
    'message': 'Team 2 is updated to light 2, medium 0, heavy 3'
    }
"""
@app.route('/teams/<teamNum>', methods=['POST'])
@requires_auth
@limiter.exempt
def override_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json()
    team.light = data['light']
    team.medium = data['medium']
    team.heavy = data['heavy']
    db.session.commit()
    return jsonify({'message' : 'Team {} is updated to light {}, medium {}, heavy {}'.format(teamNum, data['light'], data['medium'], data['heavy'])})

"""
Wipes a team's ship counts to zero
White team authenticated

URL: 
    curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/wipe
Method: 
    PUT
Data: 
    N/A
Return:
    {
    'message': 'Team 2 has been wiped'
    }
"""
@app.route('/teams/<teamNum>/wipe', methods=['PUT'])
@requires_auth
@limiter.exempt
def wipe_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.light = 0
    team.medium = 0
    team.heavy = 0
    db.session.commit()
    return jsonify({'message' : 'Team {} has been wiped'.format(teamNum)})

"""
Increments a team's light ship count
No authenticated needed.

URL: 
    curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/light
Method: 
    PUT
Data: 
    N/A
Return:
    {
    'message': 'Team 2 has built a light ship'
    }
"""
@app.route('/teams/<teamNum>/light', methods=['PUT'])
def increment_light(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.light += 1
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a light ship'.format(teamNum)})

"""
Increments a team's medium ship count
No authenticated needed.

URL: 
    curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/medium
Method: 
    PUT
Data: 
    N/A
Return:
    {
    'message': 'Team 2 has built a medium ship'
    }
"""
@app.route('/teams/<teamNum>/medium', methods=['PUT'])
def increment_medium(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.medium += 1
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a medium ship'.format(teamNum)})

"""
Increments a team's heavy ship count
No authenticated needed.

URL: 
    curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/heavy
Method: 
    PUT
Data: 
    N/A
Return:
    {
    'message': 'Team 2 has built a heavy ship'
    }
"""
@app.route('/teams/<teamNum>/heavy', methods=['PUT'])
def increment_heavy(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.heavy += 1
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a heavy ship'.format(teamNum)})

if __name__ == '__main__':

    if not os.path.exists('teams.db'): 
        open('teams.db', 'w').close() 
        db.create_all()
        #white_team = Teams(teamNum=999, name="White Team", light=0, medium=0, heavy=0, ratelimit=5)
        #db.session.add(white_team)
        #db.commit()
    app.run(debug=True)

            