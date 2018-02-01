"""
    Create our database and fill it with items
"""
from api import db
from api import Teams

db.create_all()

print('Adding teams...')
for teamNum in range(1, 12):
    new_item = Teams(teamNum=teamNum, name='Team {}'.format(teamNum))
    print('Adding Team {}'.format(teamNum))
    db.session.add(new_item)

print('Done')
db.session.commit()