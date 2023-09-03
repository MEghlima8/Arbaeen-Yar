import json
from App.Controller import db_postgres_controller as db
import uuid

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
