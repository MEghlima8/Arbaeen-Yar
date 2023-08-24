import json
from App.Controller import db_postgres_controller as db
import uuid
import random
import string

def getKaravanUsersInfo(karavan_uuid):
    info = db.db.getUsersInfoFromKaravanUUID(karavan_uuid)
    karavan_name = db.db.getKaravanName(karavan_uuid)
    result = json.dumps({"status-code":200, "result": info, "karavan_name": karavan_name})
    return result


def createNewKaravan(karavan_name, manager_username):
    if karavan_name is None:
        return 'invalid'
    manager_uuid = db.db.getUserUUID(manager_username)
    db.db.createNewKaravan(uuid.uuid4().hex, karavan_name, manager_uuid)
    return 'true'


def addNewUserToKaravan(user_fullname, user_username, manager_username):
    manager_uuid = db.db.getUserUUID(manager_username)
    karavan_uuid = db.db.getKaravanUUID(manager_uuid)
    user_uuid = uuid.uuid4().hex
    password = ''.join(random.choice(string.ascii_letters) for _ in range(12))
    db.db.addUserToDatabase(user_uuid, user_fullname, user_username, password)
    db.db.addUserToKaravanUsers(uuid.uuid4().hex, user_uuid, karavan_uuid, 'user')



# def getUserLocations(user_uuid):
#     user_locations = db.db.getUserLocations(user_uuid)
#     if user_locations == []: 
#         result = json.dumps(
#             {"status-code": 204, "result":"no location"}
#             )  
#     else:
#         result = json.dumps(
#             {"status-code":200, "result":user_locations}
#             )
#     return result
