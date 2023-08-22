from App.Controller import db_postgres_controller as db
import uuid

# 
class User:
    def __init__(self, chat_id=None):
        self.chat_id = chat_id

    # Do signup user
    def signup(self):        
        check_result = db.db.check_duplicate_id(self.chat_id)
        if check_result is None:
            db.db.signupUser(uuid.uuid4().hex, self.chat_id)
        return
        
        
    def whoIs(self):
        try:
            manager,user = db.db.checkWhoIs(self.chat_id)[0]
            if manager == 'true':
                return 'manager'
            elif user == 'true':
                return 'user'
            return 'false'
        except:
            return 'false'
