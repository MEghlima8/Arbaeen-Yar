from App.Controller import db_postgres_controller as db
from App.Controller.validation import Valid
import uuid
import hashlib


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
            
            # To save password in database as hash.
            password = hashlib.md5(self.password.encode("utf-8")).hexdigest()
            
            db.db.signupManager(manager_uuid, self.username, self.fullname, password)
            res = {"status":"True"}
            return res
        
        res = {"status":"False", "result": check_user_info}
        return res
                                            
    # Do signin manager
    def signin(self):
        password = hashlib.md5(self.password.encode("utf-8")).hexdigest() 
        valid = Valid(username=self.username, password=password)   
        valid_info = valid.signin()
        
        if valid_info == 'invalid':
            return 'invalid'
        return 'true'


class User:
    
    def __init__(self, fullname=None, username=None, password=None):
        self.fullname = fullname
        self.username = username
        self.password = password

    # Do signup user
    def signup(self,karavan_uuid):
        user_uuid = uuid.uuid4().hex  
        
        # To save password in database as hash.
        password = hashlib.md5(self.password.encode("utf-8")).hexdigest()
        db.db.signupUser(user_uuid, self.username, self.fullname, password)
        db.db.addUserToKaravanUsers(uuid.uuid4().hex, user_uuid, karavan_uuid, 'user')

        res = {"status":"True"}
        return res
    
    def edit_info(self, uuid):
        
        # To save password in database as hash.
        password = hashlib.md5(self.password.encode("utf-8")).hexdigest()
        db.db.changeUserInfo(uuid, self.fullname, self.username, password)
        return True
        