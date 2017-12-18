# Ship API

Whiteteam 

## Getting Started

Running the api.py python module will initialize a 'teams.db' sqlite3 database with the Teams() model. 


### Prerequisites

```
pip install -r requirements.txt
```

### Installing

```
$ python api.py
```

### Queries

## [WHITE] Create a team - create_team()

Creates a new team in the database with zeroed ships
Whiteteam authenticated.

# URL
```
curl -v -H "Content-Type: application/json" -X POST -d '{"teamNum" : [TEAM NUMBER], "name" : "[TEAM NAME]"}' http://127.0.0.1:5000/createteam
```
# Data: 
```
teamNum(integer)- the team number
name(string) - the team name


{"teamNum" : 2, "name" : "Blue Team 2"}
```
# Return: 
```
{
'message': 'Team 2 - Blue Team 2 created'
}
```

## [WHITE] Delete a team - delete_team()

Deletes an existing team in the database 
Whiteteam authenticated.

# URL
```
curl -v -X DELETE http://127.0.0.1:5000/deleteteam/<teamNum>
```
# Data 
```
teamNum(integer)- the team number
```
# Return 
```
{
'message': 'Team 2 deleted'
}
```

## [WHITE] Get all teams - get_all_teams()

Returns JSON of all the teams in the database
White team authenticated.

# URL 
```
curl -v http://127.0.0.1:5000/teams
```
# Response
```
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
        ...
```

## [WHITE] Get one team - get_one_team()

Returns JSON of the team requested
White team authenticated.

# URL 
```
curl -v http://127.0.0.1:5000/teams/<teamNum>
```
# Return 
```
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
```

## [WHITE] Override a team - override_one_team()

Overrides any ship's count
White team authenticated.

# URL
```
curl -v -H "Content-Type: application/json" -X POST -d '{'light' : [COUNT], 'medium' : [COUNT], 'heavy' : [COUNT]}' http://127.0.0.1:5000/teams/<teamNum>
```
# Data
```
light - light ship count
medium - medium ship count
heavy - heavy ship count

{'light' : 2, 'medium' : 0, 'heavy' : 3}
```
# Return 
```
{
'message': 'Team 2 is updated to light 2, medium 0, heavy 3'
}
```

## [WHITE] Wipe a team - wipe_one_team()

Wipes a team's ship counts to zero
White team authenticated

# URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/wipe
```
# Response
```
{
'message': 'Team 2 has been wiped'
}
```

# [ALL] Increment light - increment_light()

Increments a team's light ship count
No authenticated needed.

# URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/light
```
# Response
```
{
'message': 'Team 2 has built a light ship'
}
```
# [ALL] Increment medium - increment_medium()

Increments a team's medium ship count
No authenticated needed.

# URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/medium
```
# Response
```
{
'message': 'Team 2 has built a medium ship'
}
```
# [ALL] Increment light - increment_heavy()

Increments a team's heavy ship count
No authenticated needed.

# URL
```
curl -v -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/teams/<teamNum>/heavy
```
# Response
```
{
'message': 'Team 2 has built a heavy ship'
}
```
## Built With

* [Flask](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [SQLAlchemy](https://maven.apache.org/) - Database management
* [sqlite3](https//.org/) - Database

## Authors

* **Brandon Dossantos**


