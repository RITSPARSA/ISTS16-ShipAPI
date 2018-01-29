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

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'whiteteam' and password == 'BmuqO=[yUDQ%>)*`'

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
    guardian = db.Column(db.Integer)
    bomber = db.Column(db.Integer)
    striker = db.Column(db.Integer)
    # ratelimit = db.Column(db.Integer, nullable=True)

class Config(db.Model):
    ratelimit = db.Column(db.Integer, primary_key=True)

    def __init__(self, ratelimit=5):
        self.ratelimit = ratelimit
        db.session.commit()

RATELIMIT = 5

limiter = Limiter(
    app,
    headers_enabled=True, 
    key_func=get_remote_address,
    default_limits=["10/{}minute".format(RATELIMIT)],
    
)

@app.route('/ratelimit', methods=['GET','POST'])
@requires_auth
def change_ratelimit():
    if request.method == 'GET':
        global RATELIMIT
        return jsonify({'message' : '{}'.format(RATELIMIT)})
    else:
        data = request.get_json()
        limiter._default_limits = data['ratelimit']
        return jsonify({'message' : 'Ratelimit has been set to {}'.format(data['ratelimit'])})
# @app.route('/ratelimit', methods=['GET'])
# @requires_auth
# def change_ratelimit():
#     data = request.get_json()
#     global RATELIMIT
#     RATELIMIT = data['ratelimit']
#     return jsonify({'message' : 'Ratelimit has been set to {}'.format(RATELIMIT)})
"""
Creates a new team in the database with zeroed ships
Whiteteam authenticated
"""
@app.route('/createteam', methods=['POST'])
@requires_auth
def create_team():
    data = request.get_json()
    new_team = Teams(teamNum=data['teamNum'], name=data['name'], guardian=0, bomber=0, striker=0)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'message' : 'Team {} - {} created'.format(data['teamNum'], data['name'])})


"""
Deletes an existing team in the database 
Whiteteam authenticated
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
        team_data['guardian'] = team.guardian
        team_data['bomber'] = team.bomber
        team_data['striker'] = team.striker
        output.append(team_data)
    return jsonify({'teams': output})

"""
Returns JSON of the team requested
White team authenticated
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
    team_data['guardian'] = team.guardian
    team_data['bomber'] = team.bomber
    team_data['striker'] = team.striker
    return jsonify({'team' : team_data})

"""
Overrides any ship's count
White team authenticated
"""
@app.route('/teams/<teamNum>', methods=['POST'])
@requires_auth
@limiter.exempt
def override_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    data = request.get_json()
    team.guardian = data['guardian']
    team.bomber = data['bomber']
    team.striker = data['striker']
    db.session.commit()
    return jsonify({'message' : 'Team {} is updated to guardian {}, bomber {}, striker {}'.format(teamNum, data['guardian'], data['bomber'], data['striker'])})

"""
Wipes a team's ship counts to zero
White team authenticated
"""
@app.route('/teams/<teamNum>/wipe', methods=['PUT'])
@requires_auth
@limiter.exempt
def wipe_one_team(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.guardian = 0
    team.bomber = 0
    team.striker = 0
    db.session.commit()
    return jsonify({'message' : 'Team {} has been wiped'.format(teamNum)})

"""
Increments a team's guardian ship count
No authenticated needed.
"""
@app.route('/teams/<teamNum>/guardian', methods=['PUT'])
def increment_guardian(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.guardian += 1
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a guardian ship'.format(teamNum)})

"""
Increments a team's bomber ship count
No authenticated needed.
"""
@app.route('/teams/<teamNum>/bomber', methods=['PUT'])
def increment_bomber(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.bomber += 1
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a bomber ship'.format(teamNum)})

"""
Increments a team's striker ship count
No authenticated needed.
"""
@app.route('/teams/<teamNum>/striker', methods=['PUT'])
def increment_striker(teamNum):
    team = Teams.query.filter_by(teamNum=teamNum).first()
    team.striker += 1
    db.session.commit()
    return jsonify({'message' : 'Team {} has built a striker ship'.format(teamNum)})

if __name__ == '__main__':

    if not os.path.exists('teams.db'): 
        open('teams.db', 'w').close() 
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

            