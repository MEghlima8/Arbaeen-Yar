from App import config
import psycopg2

database = config.configs['DB_NAME']
host = config.configs['DB_HOST']
user = config.configs['DB_USER']
port = config.configs['DB_PORT']
password = config.configs['DB_PASSWORD']

class PostgreSQL:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, database, user, password, port):
        if not hasattr(self, 'connection'):
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.port = port
            self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
    def execute_query(self, query, args=()):        
        cur = self.connection.cursor()
        cur.execute(query,args)
        self.connection.commit()  
        return cur


    def signupManager(self, user_uuid, username, fullname, password):
        query = "INSERT INTO users (uuid, fullname, username, password, is_manager, active) VALUES (%s, %s, %s, %s, 'true', 'true')"
        args =(user_uuid, fullname, username, password)
        self.execute_query(query, args)
        return 'true'


    def signupUser(self, user_uuid, username, fullname, password):
        query = "INSERT INTO users (uuid, fullname, username, password, is_user, active) VALUES (%s, %s, %s, %s, 'true', 'false')"
        args =(user_uuid, fullname, username, password)
        self.execute_query(query, args)
        return 'true'


# Add user to karavan_users table
    def addUserToKaravanUsers(self, karavan_users_uuid, user_uuid, karavan_uuid):
        query = "INSERT INTO karavan_users (uuid,user_uuid,karavan_uuid) VALUES (%s, %s, %s)"
        args = (karavan_users_uuid, user_uuid, karavan_uuid)
        self.execute_query(query, args)
        return 'true'
        
    
        
    def checkMatchUsernamePassword(self,username,password):
        query = "select uuid,is_manager,is_user,active from users WHERE username=%s AND password=%s"
        args = (username, password)
        res = self.execute_query(query, args).fetchall()
        return res
    
    
    def getUserUUID(self, username):
        query = "SELECT uuid FROM users WHERE username=%s"
        args = (username,)
        res = self.execute_query(query,args).fetchone()[0]
        return res
    
    
    def getKaravansInfo(self,manager_uuid):
        query = "SELECT uuid,name FROM karavan WHERE manager_uuid=%s ORDER BY counter ASC"
        args = (manager_uuid,)
        res = self.execute_query(query,args).fetchall()
        return res
        

    def getKaravanUUID(self, manager_uuid):
        query = "SELECT uuid FROM karavan WHERE manager_uuid=%s"
        args = (manager_uuid,)
        res = self.execute_query(query,args).fetchone()[0]
        return res
    
    
    def createNewKaravan(self, uuid, karavan_name, manager_uuid):
        query = "INSERT INTO karavan (uuid,name,manager_uuid) VALUES (%s, %s, %s)"
        args = (uuid,karavan_name, manager_uuid)
        self.execute_query(query, args)
        return 'true'
        

    def addUserFromBotToDB(self, uuid, chat_id):
        query = "INSERT INTO users (uuid,chat_id,step) VALUES (%s, %s, 'home')"
        args = (uuid, chat_id)
        self.execute_query(query, args)
        return 'true'


    def getFirstTextMsg(self, chat_id):
        query = "SELECT first_msg FROM users WHERE chat_id=%s"
        args = (chat_id,)
        res = self.execute_query(query,args).fetchone()[0]
        return res


    def changeFirstTextMsg(self, value, chat_id):
        query = "UPDATE users set first_msg=%s WHERE chat_id=%s"
        args = (value, chat_id )
        text = self.execute_query(query, args)
        return text



    def getSecondTextMsg(self,user_id):
        query = "SELECT second_msg FROM users WHERE id=%s RETURNING second_msg, step"
        args = (user_id,)
        res = self.execute_query(query,args).fetchone()[0]
        return res


    def changeSecondTextMsg(self, value, user_id):
        query = "UPDATE users set second_msg=%s WHERE chat_id=%s RETURNING second_msg, step"
        args = (value, user_id )
        text = self.execute_query(query, args).fetchall()[0]
        return text

 
    def changeUserSTEP(self, new_step, chat_id):
        query = "UPDATE users set step=%s WHERE chat_id=%s"
        args = (new_step, chat_id )
        self.execute_query(query, args)
        return 'true'

 
    def getUserSTEP(self,user_id):
        query = "select step from users WHERE chat_id=%s"
        args = (user_id, )
        text = self.execute_query(query, args).fetchall()[0]
        return text       
        
 
    def updateUserToManager(self,chat_id, fullname, username, password):
        query = "UPDATE users set is_manager='true' , active='true' , fullname=%s, username=%s, password=%s WHERE chat_id=%s"
        args = (fullname, username, password, chat_id)
        self.execute_query(query, args)
        return 'true'

    
    def checkWhoIs(self,chat_id):
        query = "select is_manager,is_user from users WHERE chat_id=%s"
        args = (chat_id, )
        text = self.execute_query(query, args).fetchall()
        return text
 
    def addUserToDatabase(self,user_uuid,fullname, username, password):
        query = "INSERT INTO users (uuid, fullname, username, password, is_user, active, is_manager, step) VALUES (%s , %s , %s , %s , 'true', 'false', 'false', 'home')"
        args = (user_uuid, fullname, username, password)
        self.execute_query(query, args)
        return 'true'
        
    def activeUserAccount(self, uuid, chat_id):
        query = "DELETE FROM users where chat_id = %s"
        args = (chat_id,)
        res = self.execute_query(query, args)
        query = "UPDATE users set chat_id=%s , active='true', step='home' WHERE uuid=%s"
        args = (chat_id,uuid)
        res = self.execute_query(query, args)
        return res

    
    def addReqToDb(self, uuid, user_uuid, type, j_params, time, status):
        query = "INSERT INTO request (uuid, user_uuid, type, params, time, status) VALUES (%s , %s , %s , %s , %s , %s) RETURNING uuid"
        args =(uuid, user_uuid, type, j_params, time, status)
        req_uuid = self.execute_query(query, args).fetchall()[0][0]
        return req_uuid    
        


# web functions

    def getAllKaravanUsersInfo(self, karavan_uuid):
        query = """SELECT users.uuid, users.chat_id, users.fullname, users.username, users.password, users.active FROM users
                    INNER JOIN karavan_users ON users.uuid=karavan_users.user_uuid 
                    WHERE karavan_users.karavan_uuid=%s AND users.is_user='true'"""
        args =(karavan_uuid,)
        info = self.execute_query(query,args).fetchall()
        return info
    
    def getKaravanName(self, karavan_uuid):
        query = "SELECT name FROM karavan WHERE uuid = %s"
        args = (karavan_uuid,)
        karavan_name = self.execute_query(query,args).fetchone()[0]
        return karavan_name

    def getUserLocations(self, user_uuid):
        query = "SELECT * FROM request WHERE user_uuid = %s AND type='/send-my-location'"
        args = (user_uuid,)
        user_locations = self.execute_query(query, args).fetchall()
        return user_locations


    def checkDuplicateUsername(self, username):
        query = 'select username from users where username=%s'
        args = (username,)
        res = self.execute_query(query,args).fetchone()
        return res


db = PostgreSQL(host=host, database=database, user=user, password=password, port=port)
db.connect()