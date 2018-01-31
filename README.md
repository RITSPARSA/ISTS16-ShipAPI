# ISTS 16 - Ship API

API to manage space ship counts for each all teams. 

## Getting Started

Running the api.py python module will initialize a 'teams.db' sqlite3 database, built with the Teams() model. 


### Prerequisites

```
pip install -r requirements.txt
```

### Running

```
$ python api.py
```

# Queries

# Increment guardian 

Increments a team's guardian ship count.

```
/teams/<teamNum>/guardian [POST]
```
## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X POST -d '{"value" : [NUMBER OF SHIPS]}' http://127.0.0.1:5000/teams/<teamNum>/guardian
```
## Response
```
{
    'message': 'Team 2 has built X guardian ships'
}
```
# Increment bomber

Increments a team's bomber ship count.

```
/teams/<teamNum>/bomber [POST]
```
## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X POST -d '{"value" : [NUMBER OF SHIPS]}' http://127.0.0.1:5000/teams/<teamNum>/bomber
```
## Response
```
{
    'message': 'Team 2 has built X bomber ships'
}
```
# Increment striker

Increments a team's striker ship count. 

```
/teams/<teamNum>/striker [POST]
```
## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X POST -d '{"value" : [NUMBER OF SHIPS]}' http://127.0.0.1:5000/teams/<teamNum>/striker

```
## Response
```
{
    'message': 'Team 2 has built striker ships'
}
```

# Create a team 

Creates a new team in the database with zeroed ships. Whiteteam authenticated.

```
/createteam [POST]
```

## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X POST -d '{"teamNum" : [TEAM NUMBER], "name" : "[TEAM NAME]"}' http://127.0.0.1:5000/createteam
```
## Data
```
teamNum(integer)- the team number
name(string) - the team name


{
    'teamNum' : 2, 'name' : 'Blue Team 2'
}
```
## Response
```
{
    'message': 'Team 2 - Blue Team 2 created'
}
```

# Delete a team 

Deletes an existing team in the database. Whiteteam authenticated.

```
/deleteteam/<teamNum> [DELETE]
```
## URL
```
curl -b COOKIE -v -X DELETE http://127.0.0.1:5000/deleteteam/<teamNum>
```
## Data 
```
teamNum(integer)- the team number
```
## Response
```
{
    'message': 'Team 2 deleted'
}
```

# Get all teams 
 
Returns JSON of all the teams in the database. White team authenticated.

```
/teams [GET]
```

## URL 
```
curl -b COOKIE -v http://127.0.0.1:5000/teams
```
## Response
```
{
    "teams": [
        {
            "bomber": 0,
            "damage": 125,
            "guardian": 0,
            "health": 100,
            "name": "Blue Team 2",
            "speed": 100,
            "striker": 0,
            "teamNum": 2
        },
        {
            "bomber": 0,
            "damage": 100,
            "guardian": 0,
            "health": 100,
            "name": "Blue Team 3",
            "speed": 100,
            "striker": 0,
            "teamNum": 3
        }
    ]
}
```

# Get one team 

Returns JSON of the team requested. White team authenticated.

```
/teams/<teamNum> [GET]
```

## URL 
```
curl -b COOKIE -v http://127.0.0.1:5000/teams/<teamNum>
```
## Response
```
{
    "bomber": 7,
    "damage": 125,
    "guardian": 10,
    "health": 100,
    "name": "Blue Team 2",
    "speed": 100,
    "striker": 1,
    "teamNum": 2
}
```

# Override a team 

Overrides any ship's count. White team authenticated.

```
/teams/<teamNum> [POST]
```
## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X POST -d '{'guardian' : [COUNT], 'bomber' : [COUNT], 'striker' : [COUNT]}' http://127.0.0.1:5000/teams/<teamNum>
```
## Data
```
guardian - guardian ship count
bomber - bomber ship count
striker - heavy ship count
damage - percentage of damage
speed - percentage of speed
health - percentage of health

{
    'guardian' : 2, 'bomber' : 0, 'striker' : 3, 'damage' : 100, 'speed' : 125, 'health : 25
}
```
## Response
```
{
    'message': 'Team 2 is updated to guardian 2, bomber 0, striker 3, damage 100, speed 125, health 25'
}
```

# Reset a team 

Reset's a team to default values

```
/teams/<teamNum>/reset [PUT]
```
## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/reset
```
## Response
```
{
    'message': 'Team 2 has been reset'
}
```
# Boost a team

Boost a team's attribute by however much is passed.

```
/teams/<teamNum>/boost [POST]
```
## URL
```
curl -b COOKIE -v -H "Content-Type: application/json" -X POST -d '{"attribute" : damage, speed, or health, "type" : "increase or decrease", "value" : 25}' http://127.0.0.1:5000/teams/<teamNum>/boost
```
## Response
```
{
    'message' : 'Team X [type]'d their [damage, speed, health] by [value]'
}
```
## Built With

* [Flask](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [SQLAlchemy](https://maven.apache.org/) - Database management
* [sqlite3](https//.org/) - Database

## Authors

* **Brandon Dossantos**


