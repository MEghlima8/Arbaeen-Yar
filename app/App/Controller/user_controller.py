from App.Controller import db_postgres_controller as db
from App.Controller.validation import Valid
import uuid


class Manager:

    def __init__(self,  username=None, fullname=None, password=None):
        self.username = username
        self.fullname = fullname
        self.password = password        
        
    # Do signup user
    def signup(self):        
        # Validate signup info
        valid = Valid(username = self.username , fullname = self.fullname , password = self.password)
        check_user_info = valid.signup()     

        if check_user_info == True:
            manager_uuid = uuid.uuid4().hex         
            db.db.signupManager(manager_uuid, self.username, self.fullname, self.password)
            res = {"status":"True"}
            return res
        
        res = {"status":"False", "result": check_user_info}
        return res
                                            

    # Do signin manager
    def signin(self):        
        valid = Valid(username=self.username, password=self.password)        
        valid_info = valid.signin()
        if valid_info == 'invalid':
            # is manager
            return 'invalid'
        return 'true'



class User:
    def __init__(self, fullname=None, username=None, password=None):
        self.fullname = fullname
        self.username = username
        self.password = password

    # Do signup user
    def signup(self,karavan_uuid):
        valid = Valid(self.username, self.fullname, self.password)
        check_user_info = valid.signup()
        
        if check_user_info == True:
            user_uuid = uuid.uuid4().hex  
            db.db.signupUser(user_uuid, self.username, self.fullname, self.password)
            db.db.addUserToKaravanUsers(uuid.uuid4().hex, user_uuid, karavan_uuid, 'user')

            res = {"status":"True"}
            return res
        
        res = {"status":"False", "result": check_user_info}
        return res
        
        
#     def whoIs(self):
#         try:
#             manager,user = db.db.checkWhoIs(self.chat_id)[0]
#             if manager == 'true':
#                 return 'manager'
#             elif user == 'true':
#                 return 'user'
#             return 'false'
#         except:
#             return 'false'
