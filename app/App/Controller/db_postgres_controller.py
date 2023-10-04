from App import config
import psycopg2
import re
from datetime import datetime
from jdatetime import datetime as jdatetime
import json

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

    def getCurrentTime(self, active_account_time):
        jdate = jdatetime.fromgregorian(datetime=datetime.now())
        hour = jdate.hour + 3
        minute = jdate.minute + 30
        second = jdate.second
        if minute > 59 :
            minute -= 60
        if hour > 23 : 
            hour -= 24
            
        time = f'{hour}:{minute}:{second}'
        date = f'{jdate.year}-{jdate.month}-{jdate.day}'
        if active_account_time :
            res = json.dumps({'status':'true' , 'date':date , 'time':time})
        else :
            res = json.dumps({'date':date , 'time':time})
        return res


    def signupManager(self, user_uuid, username, fullname, password):
        query = "INSERT INTO users (uuid, fullname, username, password, is_manager, active, last_activity) VALUES (%s, %s, %s, %s, 'true', %s, %s)"
        args =(user_uuid, fullname, username, password, self.getCurrentTime(True), self.getCurrentTime(False))
        self.execute_query(query, args)
        return 'true'


    def signupUser(self, user_uuid, username, fullname, password):
        current_time = json.loads(self.getCurrentTime(False))
        query = "INSERT INTO users (uuid, fullname, username, password, is_user, active) VALUES (%s, %s, %s, %s, 'true', %s)"
        args =(user_uuid, fullname, username, password,json.dumps({'status':'false', 'created':current_time}))
        self.execute_query(query, args)
        return 'true'


    def changeUserInfo(self, uuid, fullname, username, password):
        query = """
            UPDATE users
            SET
            fullname = CASE WHEN %s!='' THEN %s ELSE fullname END,
            username = CASE WHEN %s!='' THEN %s ELSE username END,
            password = CASE WHEN %s!='' THEN %s ELSE password END
            WHERE uuid = %s;
        """
        args = (fullname, fullname, username, username, password, password, uuid)
        text = self.execute_query(query, args)
        return text


    def countAdminUsersAccountStatus(self):
        query = """SELECT users.active->>'status', COUNT(*) AS count FROM users
                    GROUP BY users.active->>'status';"""    
        args = ()
        res = self.execute_query(query,args).fetchall()
        return res

    def countAdminReqsType(self):
        query = """SELECT type, COUNT(*) AS count FROM request
                    WHERE status = 'done' GROUP BY type"""
        args = ()
        res = self.execute_query(query,args).fetchall()
        return res

    def getKaravansList(self):
        query = "SELECT name,manager_uuid FROM karavan"
        args = ()
        res = self.execute_query(query,args).fetchall()
        return res


    def getAdminManagersList(self):
        query = "SELECT fullname,username FROM users WHERE is_manager='true'"
        args = ()
        res = self.execute_query(query,args).fetchall()
        return res

    def getUserFullname(self,uuid):
        query = "SELECT fullname,username FROM users WHERE uuid=%s"
        args = (uuid,)
        res = self.execute_query(query,args).fetchone()
        return res

    def countKaravanUsersAccountStatus(self, karavan_uuid):
        query = """SELECT users.active->>'status', COUNT(*) AS count FROM users
                    INNER JOIN karavan_users ON users.uuid = karavan_users.user_uuid
                    WHERE is_user = 'true' AND karavan_users.karavan_uuid = %s GROUP BY users.active->>'status';"""    
        args = (karavan_uuid,)
        res = self.execute_query(query,args).fetchall()
        return res
    
    def countKaravanReqsType(self, karavan_uuid):
        query = """SELECT type, COUNT(*) AS count FROM request
                    WHERE status = 'done' AND karavan_uuid=%s GROUP BY type"""
        args = (karavan_uuid,)
        res = self.execute_query(query,args).fetchall()
        return res

# Add user to karavan_users table
    def addUserToKaravanUsers(self, karavan_users_uuid, user_uuid, karavan_uuid, whois):
        query = "INSERT INTO karavan_users (uuid,user_uuid,karavan_uuid,whois) VALUES (%s, %s, %s, %s)"
        args = (karavan_users_uuid, user_uuid, karavan_uuid, whois)
        self.execute_query(query, args)
        return 'true'
        
        
    def checkMatchUsernamePassword(self,username,password):
        query = "SELECT uuid,is_manager,is_user,active FROM users WHERE username=%s AND password=%s"
        args = (username, password)
        res = self.execute_query(query, args).fetchall()
        return res
    
    
    def getUserUUID(self, username):
        query = "SELECT uuid FROM users WHERE username=%s"
        args = (username,)
        res = self.execute_query(query,args).fetchone()[0]
        return res
    
    def getManagerUUID(self, username):
        query = "SELECT uuid FROM users WHERE username=%s AND is_manager = 'true'"
        args = (username,)
        res = self.execute_query(query,args).fetchone()
        return res
    
    def getUserUUIDFromChatId(self, chat_id):
        query = "SELECT uuid FROM users WHERE chat_id=%s"
        args = (chat_id,)
        res = self.execute_query(query,args).fetchone()[0]
        return res        
    
    
    def getKaravansInfo(self,manager_uuid):
        query = "SELECT uuid,name FROM karavan WHERE managers ? %s ORDER BY counter ASC"
        args = (manager_uuid,)
        res = self.execute_query(query,args).fetchall()
        return res
        
        
    def getAllKaravanManagersUuid(self, karavan_uuid):
        query = "SELECT managers FROM karavan WHERE uuid=%s"
        args = (karavan_uuid,)
        res = self.execute_query(query,args).fetchone()
        return res
      
       
    def getManagerInfo(self, manager_uuid):
        query = "SELECT fullname, username FROM users WHERE uuid=%s"
        args = (manager_uuid,)
        res = self.execute_query(query,args).fetchall()
        return res   
    

    def getKaravanUUID(self, manager_uuid):
        query = "SELECT uuid FROM karavan WHERE manager_uuid=%s"
        args = (manager_uuid,)
        res = self.execute_query(query,args).fetchone()[0]
        return res
    
    
    def getKaravanUUIDFromUser(self, user_uuid):
        query = "SELECT karavan_uuid FROM karavan_users WHERE user_uuid=%s"
        args = (user_uuid,)
        res = self.execute_query(query,args).fetchone()[0]
        return res


    def getKaravanEvents(self, karavan_uuid):
        query = "SELECT events FROM karavan WHERE uuid=%s"
        args = (karavan_uuid,)
        res = self.execute_query(query,args).fetchall()
        return res
      
    
    def createNewKaravan(self, uuid, karavan_name, manager_uuid, manager_username, no_event_random_uuid):
        managers = json.dumps({manager_uuid : manager_username})
        event = json.dumps({'بدون رویداد' : no_event_random_uuid})
        query = "INSERT INTO karavan (uuid, name, manager_uuid, managers, events) VALUES (%s, %s, %s, %s, %s)"
        args = (uuid,karavan_name, manager_uuid, managers, event)
        self.execute_query(query, args)
        return 'true'
        

    def AddManagerToKaravan(self, karavan_uuid, manager_uuid, manager_username):
        x = f'{{"{manager_uuid}": "{manager_username}"}}'
        query = f"""UPDATE karavan SET managers = managers || %s 
                    WHERE uuid = %s;"""
        args = (x, karavan_uuid)
        self.execute_query(query,args)
        return 'done'


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
        query = "SELECT step FROM users WHERE chat_id=%s"
        args = (user_id, )
        text = self.execute_query(query, args).fetchall()[0]
        return text       
        
     
    def activeUserAccount(self, uuid, chat_id):
        query = "DELETE FROM users WHERE chat_id = %s"
        args = (chat_id,)
        self.execute_query(query, args)
        current_time = json.loads(self.getCurrentTime(True))        
        val2 = f'"{current_time["date"]}"'
        val3 = f'"{current_time["time"]}"'
        status_key = '{status}'
        date_key = '{date}'
        time_key = '{time}'

        query = f"""UPDATE users SET chat_id=%s, step='home',
                        active = jsonb_set( jsonb_set( jsonb_set(active,'{status_key}', '"true"'),
                                            '{date_key}', '{val2}'),
                                        '{time_key}', '{val3}') WHERE uuid=%s"""
        args = (chat_id, uuid)
        self.execute_query(query, args)
        return 'true'


    def getManagerFullname(self, username):
        query = "SELECT fullname FROM users WHERE username=%s AND is_manager='true'"
        args = (username, )
        fullname = self.execute_query(query, args).fetchone()
        return fullname       
    
    
    def addReqToDb(self, uuid, user_uuid, karavan_uuid, type, j_params, time, status):
        
        # Change user last activity to current time
        query = "UPDATE users SET last_activity=%s WHERE uuid=%s"
        args =(self.getCurrentTime(False), user_uuid)
        self.execute_query(query, args)
        
        # Add request to database
        client_service = config.configs['CLIENT_SERVICE_NAME']
        query = "INSERT INTO request (uuid, user_uuid, karavan_uuid, type, params, time, status, client_service) VALUES (%s , %s , %s , %s , %s , %s, %s, %s) RETURNING uuid"
        args =(uuid, user_uuid, karavan_uuid, type, j_params, time, status, client_service)
        req_uuid = self.execute_query(query, args).fetchall()[0][0]
        return req_uuid    
        

    def checkIsUserActive(self,chat_id):
        query = "SELECT is_user, active FROM users WHERE chat_id=%s"
        args = (chat_id, )
        account_status = self.execute_query(query, args).fetchall()
        return account_status
    
    
    def getKaravanNameFromUserInfo(self, user_uuid):
        # Get karavan uuid
        query = "SELECT karavan_uuid FROM karavan_users WHERE user_uuid=%s "
        args = (user_uuid, )
        karavan_uuid = self.execute_query(query, args).fetchone()[0]
        
        # Get karavan name
        query = "SELECT name FROM karavan WHERE uuid=%s "
        args = (karavan_uuid, )
        karavan_name = self.execute_query(query, args).fetchone()[0]
        return karavan_name
        
        
    def getKaravanName(self, karavan_uuid):
        query = "SELECT name FROM karavan WHERE uuid = %s"
        args = (karavan_uuid,)
        karavan_name = self.execute_query(query,args).fetchone()[0]
        return karavan_name


    def getUserLocations(self, user_uuid):
        query = """SELECT request.counter, request.uuid, request.params, request.time, users.fullname, users.username, users.uuid, request.client_service FROM request 
                    INNER JOIN users ON request.user_uuid = users.uuid
                    WHERE request.user_uuid = %s AND request.type='/send-my-location' ORDER BY request.counter DESC"""
        args = (user_uuid,)
        user_locations = self.execute_query(query, args).fetchall()
        return user_locations


    def checkDuplicateUsername(self, username):
        query = "SELECT username FROM users WHERE username=%s"
        args = (username,)
        res = self.execute_query(query,args).fetchone()
        return res


    def checkDuplicateEventName(self, karavan_uuid, event_name):
        query = "SELECT events->>%s FROM karavan WHERE uuid=%s"
        args = (event_name, karavan_uuid)
        res = self.execute_query(query,args).fetchone()
        return res
    
    
    def getAdminUsersList(self):
        query = """SELECT users.fullname, users.username, users.active,
                users.last_activity FROM users 
                WHERE users.is_user='true' ORDER BY users.counter ASC"""
        args =()
        info = self.execute_query(query,args).fetchall()
        return info

    
    def addEventToKaravan(self, karavan_uuid, event_name, random_uuid):
        x = f'{{"{event_name}": "{random_uuid}"}}'
        query = f"""UPDATE karavan SET events = events || %s 
                    WHERE uuid = %s;"""
        args = (x, karavan_uuid)
        self.execute_query(query,args)
        return 'done'

    def getAllKaravanUsersInfo(self, karavan_uuid, search_value):
        if search_value == '' or search_value == None :
            query = """SELECT users.uuid, users.chat_id, users.fullname, users.username, users.password, users.active,
                    users.last_activity FROM users INNER JOIN karavan_users ON users.uuid=karavan_users.user_uuid 
                    WHERE karavan_users.karavan_uuid=%s AND users.is_user='true' ORDER BY users.counter ASC"""
            args =(karavan_uuid,)
            
        # Search in fullname column
        elif re.match(r'^[\u0600-\u06FF\s]+$', search_value):
            query = """SELECT users.uuid, users.chat_id, users.fullname, users.username, users.password, users.active,
                    users.last_activity FROM users INNER JOIN karavan_users ON users.uuid=karavan_users.user_uuid 
                    WHERE karavan_users.karavan_uuid=%s AND users.is_user='true' AND 
                    users.fullname LIKE %s ORDER BY users.counter ASC"""
            args =(karavan_uuid, '%'+search_value+'%')

        # Search in username column
        else:
            query = """SELECT users.uuid, users.chat_id, users.fullname, users.username, users.password, users.active,
                    users.last_activity FROM users INNER JOIN karavan_users ON users.uuid=karavan_users.user_uuid 
                    WHERE karavan_users.karavan_uuid=%s AND users.is_user='true' AND 
                    users.username LIKE %s ORDER BY users.counter ASC"""
            args =(karavan_uuid, '%'+search_value+'%')

        info = self.execute_query(query,args).fetchall()
        return info
    

    def getKaravanRequestInfo(self, karavan_uuid, type, search_value):
        if search_value == '' or search_value is None :
            query = """SELECT users.fullname, users.username, request.uuid, request.time, request.params, request.client_service FROM users
                    INNER JOIN request ON users.uuid=request.user_uuid 
                    WHERE request.karavan_uuid=%s AND users.is_user='true' AND
                    request.type=%s ORDER BY request.counter DESC"""
            args = (karavan_uuid, type)
            
        # Search in fullname column
        elif re.match(r'^[\u0600-\u06FF\s]+$', search_value):
            query = """SELECT users.fullname, users.username, request.uuid, request.time, request.params, request.client_service FROM users
                    INNER JOIN request ON users.uuid=request.user_uuid 
                    WHERE request.karavan_uuid=%s AND users.is_user='true' AND
                    request.type=%s AND users.fullname LIKE %s ORDER BY request.counter DESC"""
            args = (karavan_uuid, type, '%'+search_value+'%')
        
        # Search in username column
        else:
            query = """SELECT users.fullname, users.username, request.uuid, request.time, request.params, request.client_service FROM users
                    INNER JOIN request ON users.uuid=request.user_uuid 
                    WHERE request.karavan_uuid=%s AND users.is_user='true' AND
                    request.type=%s AND users.username LIKE %s ORDER BY request.counter DESC"""
            args = (karavan_uuid, type, '%'+search_value+'%')
            
        res = self.execute_query(query,args).fetchall()
        return res


    def ChangeMsgStatus(self, msg_uuid, change_to):
        key = '{status}'
        value = f'"{change_to}"'
        query = f"UPDATE request SET params = JSONB_SET(params, '{key}', '{value}') WHERE uuid = %s"
        args = (msg_uuid,)
        self.execute_query(query, args)
        return 'done'



    def changeAccountStatus(self, user_uuid, new_status):
        key = '{status}'
        value = f'"{new_status}"'
        query = f"UPDATE users SET active = JSONB_SET(active, '{key}', '{value}') WHERE uuid = %s"
        args = (user_uuid,)        
        self.execute_query(query, args)
        return 'done'



db = PostgreSQL(host=host, database=database, user=user, password=password, port=port)
db.connect()