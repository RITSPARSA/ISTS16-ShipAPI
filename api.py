from functools import wraps
from pathlib import Path
import os
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address
#from flask.ext.limiter import Limiter, HEADERS

app = Flask(__name__)
dir_path = os.path.dirname(os.path.realpath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/teams.db'.format(dir_path)
db = SQLAlchemy(app)

# def check_auth(username, password):
#     """This function is called to check if a username /
#     password combination is valid.
#     """
#     return username == 'whiteteam' and password == 'BmuqO=[yUDQ%>)*`'

# def authenticate():
#     """Sends a 401 response that enables basic auth"""
#     return Response(
#     'YOU SHALL NOT PASS.\n', 401,
#     {'WWW-Authenticate': 'Basic realm="Login Required"'}),
    

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated

class Teams(db.Model):
    #id = db .Column(db.Integer, primary_key=True)
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

# RATELIMIT = 5

# limiter = Limiter(
#     app,
#     headers_enabled=True, 
#     key_func=get_remote_address,
#     default_limits=["10/{}minute".format(RATELIMIT)],
    
# )

# @app.route('/ratelimit', methods=['GET','POST'])
# @requires_auth
# def change_ratelimit():
#     if request.method == 'GET':
#         global RATELIMIT
#         return jsonify({'message' : '{}'.format(RATELIMIT)})
#     else:
#         data = request.get_json()
#         limiter._default_limits = data['ratelimit']
#         return jsonify({'message' : 'Ratelimit has been set to {}'.format(data['ratelimit'])})
# @app.route('/ratelimit', methods=['GET'])
# @requires_auth
# def change_ratelimit():
#     data = request.get_json()
#     global RATELIMIT
#     RATELIMIT = data['ratelimit']
#     return jsonify({'message' : 'Ratelimit has been set to {}'.format(RATELIMIT)})
"""
Creates a new team in the database with zeroed ships
"""
@app.route('/createteam', methods=['POST'])
# @requires_auth
def create_team():
    data = request.get_json(force=True)
    print("data is {}".format(data))
    new_team = Teams(teamNum=data['teamNum'], name=data['name'])
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message' : 'Team {} - {} created'.format(data['teamNum'], data['name'])})


"""
Deletes an existing team in the database 
"""
@app.route('/deleteteam/<teamNum>', methods=['DELETE'])
# @requires_auth
def delete_team(teamNum): 
    team = Teams.query.filter_by(teamNum=teamNum).first()

    if not team:
        return jsonify({'message' : 'Team {} NOT found!'.format(teamNum)})

    db.session.delete(team)
    db.session.commit()
    return jsonify({'message' : 'Team {} deleted'.format(teamNum)})

"""
Returns JSON of all the teams in the database
"""
@app.route('/teams', methods=['GET'])
# @requires_auth
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
@app.route('/teams/<teamNum>', methods=['GET'])
# @requires_auth
def get_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    if not team:
        return jsonify({'message' : 'Team {} - {} NOT found!'.format(data['teamNum'], data['name'])})

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
@app.route('/teams/<teamNum>', methods=['POST'])
# @requires_auth
def override_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json()
    team.guardian = data['guardian']
    team.bomber = data['bomber']
    team.striker = data['striker']
    team.damage = data['damage']
    team.speed = data['speed']
    team.health = data['health']
    db.session.commit()
    return jsonify({'message' : 'Team {} is updated to guardian {}, bomber {}, striker {}, damage {}, speed {}, health {}'.format(teamNum, data['guardian'], data['bomber'], data['striker'], data['damage'], data['speed'], data['health'])})

"""
Resets a team's ship counts to default
"""
@app.route('/teams/<teamNum>/reset', methods=['PUT'])
# @requires_auth
def reset_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
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
@app.route('/teams/<teamNum>/guardian', methods=['POST'])
def increment_guardian(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json(force=True)
    team.guardian += data['value']
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a guardian ship'.format(teamNum, data['value'])})

"""
Increments a team's bomber ship count
"""
@app.route('/teams/<teamNum>/bomber', methods=['POST'])
def increment_bomber(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json(force=True)
    team.bomber += data['value']
    db.session.commit()
    return jsonify({'message' : 'Team {} has built {} bomber ships'.format(teamNum, data['value'])})

"""
Increments a team's striker ship count
"""
@app.route('/teams/<teamNum>/striker', methods=['POST'])
def increment_striker(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json(force=True)
    team.striker += data['value']
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a striker ship'.format(teamNum, data['value'])})


"""
Boost damage, health, or speed by however much was passed. 
"""
@app.route('/teams/<teamNum>/boost', methods=['POST'])
# @requires_auth
def boost_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json(force=True)
    try:
        setattr(team, data['attribute'], getattr(team, data['attribute'])+data['value'])
    except Exception as e:
        return jsonify({'message' : 'Something is wrong'})

    db.session.commit()
    return jsonify({'message' : 'Team {} their {} by {} '.format(teamNum, data['boost'], data['value'])})

if __name__ == '__main__':

    if not os.path.exists('teams.db'): 
        open('teams.db', 'w').close() 
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

            