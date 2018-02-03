from functools import wraps
from pathlib import Path
import os, requests
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address

AUTH_SERVER = 'http://lilbite.org:9000'

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/teams.db'.format(dir_path)
db = SQLAlchemy(app)

def no_token():
    return jsonify({'error' : 'no token in cookies'})

def no_match():
    return jsonify({'error' : 'team number does not match token'})

"""
Query the auth server with passed cookie token
and returns the token's team number.
"""
def authentication(token):
    data = {'token': token}
    url = '{}/validate-session'.format(AUTH_SERVER)
    resp = requests.post(url, data=data)
    resp_data = resp.json()
    if resp_data['success']:
        return int(resp_data['success'])
    else:
        return jsonify({'error' : 'success key'})

"""
Compares the number returned from the auth server 
with the teamnumber passed in the route.
"""
def blue_white(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in request.cookies:
            return no_token()
        try:
            token_num = authentication(request.cookies['token'])
        except Exception:
            return jsonify({'error' : 'success key not found'})
        if token_num == 1337 or token_num == kwargs['teamNum']:
            return f(*args, **kwargs)
        else:
            return no_match()
    return decorated

"""
Compares the number returned from the auth server 
with the teamnumber passed in the route.
"""
def white_team(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' not in request.cookies:
            return no_token()
        try:
            token_num = authentication(request.cookies['token'])
        except Exception:
            return jsonify({'error' : 'success key not found'})
        if token_num == 1337:
            return f(*args, **kwargs)
        else:
            return no_match()
    return decorated
class Teams(db.Model):
    teamNum = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    guardian = db.Column(db.Integer, default=0)
    bomber = db.Column(db.Integer, default=0)
    striker = db.Column(db.Integer, default=0)
    health = db.Column(db.Integer, default=100)
    damage = db.Column(db.Integer, default=100)
    speed = db.Column(db.Integer, default=100)

class Config(db.Model):
    ratelimit = db.Column(db.Integer, primary_key=True)

    def __init__(self, ratelimit=5):
        self.ratelimit = ratelimit
        db.session.commit()

"""
Creates a new team in the database with zeroed ships
"""
@app.route('/createteam', methods=['POST'])
@white_team
def create_team():
    data = request.get_json(force=True)
    new_team = Teams(teamNum=data['teamNum'], name=data['name'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message' : 'Team {} - {} created'.format(data['teamNum'], data['name'])})



"""
Deletes an existing team in the database 
"""
@app.route('/deleteteam/<int:teamNum>', methods=['DELETE'])
@white_team
def delete_team(teamNum): 
    team = Teams.query.filter_by(teamNum=teamNum).first()

    if not team:
        return jsonify({'message' : 'Team {} not found'.format(teamNum)})

    db.session.delete(team)
    db.session.commit()
    return jsonify({'message' : 'Team {} deleted'.format(teamNum)})

"""
Returns JSON of all the teams in the database
"""
@app.route('/teams', methods=['GET'])
@white_team
def get_all_teams():
    teams = Teams.query.all()
    output = []
    for team in teams:
        team_data = {}
        team_data['teamNum'] = team.teamNum
        team_data['name'] = team.name
        team_data['guardian'] = team.guardian
        team_data['bomber'] = team.bomber
        team_data['striker'] = team.striker
        team_data['damage'] = team.damage
        team_data['speed'] = team.speed
        team_data['health'] = team.health
        output.append(team_data)
    return jsonify({'teams': output})

"""
Returns JSON of the team requested
"""
@app.route('/teams/<int:teamNum>', methods=['GET'])
@blue_white
def get_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} - {} not found'.format(data['teamNum'], data['name'])})
    team_data = {}
    team_data['teamNum'] = team.teamNum
    team_data['name'] = team.name
    team_data['guardian'] = team.guardian
    team_data['bomber'] = team.bomber
    team_data['striker'] = team.striker
    team_data['damage'] = team.damage
    team_data['speed'] = team.speed
    team_data['health'] = team.health
    return jsonify(team_data)

"""
Override
"""
@app.route('/teams/<int:teamNum>', methods=['POST'])
@white_team
def override_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} not found'.format(teamNum)})

    data = request.get_json()
    team.guardian = data['guardian']
    team.bomber = data['bomber']
    team.striker = data['striker']
    team.damage = data['damage']
    team.speed = data['speed']
    team.health = data['health']
    db.session.commit()
    return jsonify({'message' : 'Team {} updated to guardian {}, bomber {}, striker {}, damage {}, speed {}, health {}'.format(teamNum, data['guardian'], data['bomber'], data['striker'], data['damage'], data['speed'], data['health'])})

"""
Resets a team's ship counts to default
"""
@app.route('/teams/<int:teamNum>/reset', methods=['POST'])
@white_team
def reset_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} not found'.format(teamNum)})
    team.guardian = 0
    team.bomber = 0
    team.striker = 0
    team.damage = 100
    team.speed = 100
    team.health = 100
    db.session.commit()
    return jsonify({'message' : 'Team {} has been reset'.format(teamNum)})

"""
Increments a team's guardian ship count
"""
@app.route('/teams/<int:teamNum>/guardian', methods=['POST'])
@white_team
def increment_guardian(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} not found'.format(teamNum)})
    data = request.get_json(force=True)
    team.guardian += data['value']
    if team.guardian < 0:
        team.guardian = 0

    db.session.commit()
    return jsonify({'message' : 'Team {} has built {} guardian ships'.format(teamNum, data['value'])})

"""
Increments a team's bomber ship count
"""
@app.route('/teams/<int:teamNum>/bomber', methods=['POST'])
@white_team
def increment_bomber(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} not found'.format(teamNum)})
    data = request.get_json(force=True)
    team.bomber += data['value']
    if team.bomber < 0:
        team.bomber = 0

    db.session.commit()
    return jsonify({'message' : 'Team {} has built {} bomber ships'.format(teamNum, data['value'])})

"""
Increments a team's striker ship count
"""
@app.route('/teams/<int:teamNum>/striker', methods=['POST'])
@blue_white
def increment_striker(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} not found'.format(teamNum)})
    data = request.get_json(force=True)
    team.striker += data['value']
    if team.striker < 0:
        team.striker = 0

    db.session.commit()
    return jsonify({'message' : 'Team {} has built {} striker ships'.format(teamNum, data['value'])})


"""
Boost damage, health, or speed by however much was passed. 
"""
@app.route('/teams/<int:teamNum>/boost', methods=['POST'])
@blue_white
def boost_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'error' : 'Team {} not found'.format(teamNum)})
    data = request.get_json(force=True)
    try:
        setattr(team, data['type'], getattr(team, data['type'])+data['value'])
    except Exception as e:
        return jsonify({'error' : '{}'.format(e)})

    db.session.commit()
    return jsonify({'message' : 'Team {} {}\'d their {} by {} '.format(teamNum, data['change'], data['type'], data['value'])})

if __name__ == '__main__':

    if not os.path.exists('teams.db'): 
        open('teams.db', 'w').close() 
    app.run(debug=True, host='0.0.0.0', port=6000)

            
