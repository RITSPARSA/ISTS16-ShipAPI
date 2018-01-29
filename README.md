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

# Credentials 

```
username: whiteteam
password: BmuqO=[yUDQ%>)*`
```

# Queries

# [ALL] Increment guardian 

Increments a team's guardian ship count. No authenticated needed.

```
/teams/<teamNum>/guardian [PUT]
```
## URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/guardian
```
## Response
```
{
'message': 'Team 2 has built a guardian ship'
}
```
# [ALL] Increment bomber

Increments a team's bomber ship count. No authenticated needed.

```
/teams/<teamNum>/bomber [PUT]
```
## URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/bomber
```
## Response
```
{
'message': 'Team 2 has built a bomber ship'
}
```
# [ALL] Increment striker

Increments a team's striker ship count. No authenticated needed.

```
/teams/<teamNum>/striker [PUT]
```
## URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/striker
```
## Response
```
{
'message': 'Team 2 has built a striker ship'
}
```

# [WHITE] Create a team 

Creates a new team in the database with zeroed ships. Whiteteam authenticated.

```
/createteam [POST]
```

## URL
```
curl -u [WHITETEAM USER]:[WHITETEAM PASS] -v -H "Content-Type: application/json" -X POST -d '{"teamNum" : [TEAM NUMBER], "name" : "[TEAM NAME]"}' http://127.0.0.1:5000/createteam
```
## Data
```
teamNum(integer)- the team number
name(string) - the team name


{"teamNum" : 2, "name" : "Blue Team 2"}
```
## Response
```
{
'message': 'Team 2 - Blue Team 2 created'
}
```

# [WHITE] Delete a team 

Deletes an existing team in the database. Whiteteam authenticated.

```
/deleteteam/<teamNum> [DELETE]
```
## URL
```
curl -u [WHITETEAM USER]:[WHITETEAM PASS] -v -X DELETE http://127.0.0.1:5000/deleteteam/<teamNum>
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

# [WHITE] Get all teams 

Returns JSON of all the teams in the database. White team authenticated.

```
/teams [GET]
```

## URL 
```
curl -u [WHITETEAM USER]:[WHITETEAM PASS] -v http://127.0.0.1:5000/teams
```
## Response
```
{
"teams": [
    {
        "striker": 0,
        "id": 1,
        "guardian": 0,
        "bomber": 0,
        "name": "Blue Team 2",
        "teamNum": 2
    },
    {
        "striker": 0,
        "id": 3,
        "guardian": 0,
        "bomber": 0,
        "name": "Blue Team 3",
        "teamNum": 3
    },
        ...
```

# [WHITE] Get one team 

Returns JSON of the team requested. White team authenticated.

```
/teams/<teamNum> [GET]
```

## URL 
```
curl -u [WHITETEAM USER]:[WHITETEAM PASS] -v http://127.0.0.1:5000/teams/<teamNum>
```
## Response
```
{
    "teams": [
        {
            "striker": 0,
            "id": 1,
            "guardian": 0,
            "bomber": 0,
            "name": "Blue Team 2",
            "teamNum": 2
        }]
}
```

# [WHITE] Override a team 

Overrides any ship's count. White team authenticated.

```
/teams/<teamNum> [POST]
```
## URL
```
curl -u [WHITETEAM USER]:[WHITETEAM PASS] -v -H "Content-Type: application/json" -X POST -d '{'guardian' : [COUNT], 'bomber' : [COUNT], 'striker' : [COUNT]}' http://127.0.0.1:5000/teams/<teamNum>
```
## Data
```
guardian - guardian ship count
bomber - bomber ship count
striker - heavy ship count

{'guardian' : 2, 'bomber' : 0, 'striker' : 3}
```
## Response
```
{
'message': 'Team 2 is updated to guardian 2, bomber 0, striker 3'
}
```

# [WHITE] Wipe a team 

Wipes a team's ship counts to zero. White team authenticated

```
/teams/<teamNum>/wipe [PUT]
```
## URL
```
curl -u [WHITETEAM USER]:[WHITETEAM PASS] -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/wipe
```
## Response
```
{
'message': 'Team 2 has been wiped'
}
```
## Built With

* [Flask](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [SQLAlchemy](https://maven.apache.org/) - Database management
* [sqlite3](https//.org/) - Database

## Authors

* **Brandon Dossantos**


