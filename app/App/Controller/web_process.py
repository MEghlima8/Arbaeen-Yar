import json
from App.Controller import db_postgres_controller as db
import uuid
from datetime import datetime
from jdatetime import datetime as jdatetime

events = {'moharram':'محرم', 'arbaeen':'اربعین', 'ghadir':'غدیر', 'fetr':'فطر', 'other':'سایر'}

def get_date():
    jdate = jdatetime.fromgregorian(datetime=datetime.now())
    date = f'{jdate.year}-{jdate.month}-{jdate.day}'
    return date


def getKaravanUsersInfo(karavan_uuid):
    info = db.db.getUsersInfoFromKaravanUUID(karavan_uuid)
    karavan_name = db.db.getKaravanName(karavan_uuid)
    result = json.dumps({"status-code":200, "result": info, "karavan_name": karavan_name})
    return result


def createNewKaravan(karavan_name, manager_username):
    if karavan_name is None:
        return 'invalid'
    manager_uuid = db.db.getUserUUID(manager_username)
    karavan_uuid = uuid.uuid4().hex
    db.db.createNewKaravan(karavan_uuid, karavan_name, manager_uuid)
    db.db.addUserToKaravanUsers(uuid.uuid4().hex, manager_uuid, karavan_uuid, 'manager')
    return 'true'


def handleResultByTime(requests,time):
    result = []
    current_date = get_date()
    weekday = jdatetime.fromgregorian(datetime=datetime.now()).weekday()
    current_date = current_date.split('-')
    
    if time == 'all':
        return requests
    elif time == 'today':
        pass
    elif time == 'week':
        current_date[-1] = str(int(current_date[-1]) - weekday)
    elif time == 'month':
        current_date[-1] = '1'
    elif time == 'year':
        current_date[-1] = '1'
        current_date[-2] = '1'
        
    current_date = '-'.join(current_date)
    for i in requests:
        if i[3]['date'] >= current_date:
            result.append(i)
    return result


def handleResultByEvent(requests, event):
    result = []
    if event == 'all':
        return requests
    
    for i in requests:
        try:
            # [result.append(i) if i[4]['event'] == event ]
            if i[4]['event'] == event:
                result.append(i)
        except:
            pass
    return result
