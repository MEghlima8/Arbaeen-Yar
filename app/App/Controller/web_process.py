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
    db.db.createNewKaravan(karavan_uuid, karavan_name, manager_uuid, uuid.uuid4().hex)
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
            if i[4]['event'] == event:
                result.append(i)
        except:
            pass
    return result


def convert_add_user_error_to_persian(error):
    match error:
        case 'no_valid_fullname':
            return 'نام و نام خانوادگی باید به فارسی باشد'
        case 'empty_fullname':
            return 'نام و نام خانوادگی ثبت نشده است'
            
        case 'empty_password':
            return 'رمز عبور ثبت نشده است'
        case 'char_password':
            return 'طول رمز عبور باید بیشتر از 8 کاراکتر و فقط شامل حرف انگلیسی و کاراکتر خاص و عدد باشد'
        case 'used_info_in_password':
            return 'رمز عبور مطابقت زیادی با نام کاربری دارد. رمز عبور دیگری را انتخاب کنید'
            
        case 'empty_username':
            return 'نام کاربری ثبت نشده است'
        case 'duplicate_username':
            return 'نام کاربری تکراری می باشد'
        case 'length_username':
            return 'نام کاربری بین 3 تا 20 کاراکتر باید باشد'
        case 'char_username':
            return 'نام کاربری فقط می تواند شامل حروف کوچک و بزرگ انگلیسی و اعداد و نقطه و زیرخط(آندرلاین) باشد'


def get_karavan_general_info(karavan_uuid):
    count_karavan_users_account_status = db.db.countKaravanUsersAccountStatus(karavan_uuid)
    count_karavan_reqs_type = db.db.countKaravanReqsType(karavan_uuid)
    
    if len(count_karavan_users_account_status) == 0 :
        noactive = ('noactive',0)
        active = ('active',0)
    elif len(count_karavan_users_account_status) == 1 :
        
        if count_karavan_users_account_status[0][0] == 'false':
            noactive = count_karavan_users_account_status[0]
            active = ('active',0)
        else:
            active = count_karavan_users_account_status[0]
            noactive = ('noactive',0)
    else:
        
        if count_karavan_users_account_status[0][0] == 'false':
            noactive = count_karavan_users_account_status[0]
            active = count_karavan_users_account_status[1]
        else:
            active = count_karavan_users_account_status[0]
            noactive = count_karavan_users_account_status[1]

    if len(count_karavan_reqs_type) == 0 :
        souvenir_photo = ('/souvenir-photo', 0)
        location = ('/send-my-location', 0)        
    elif len(count_karavan_reqs_type) == 1 :
        
        if count_karavan_reqs_type[0][0] == '/souvenir-photo':
            souvenir_photo = count_karavan_reqs_type[0]
            location = ('/send-my-location', 0)
        else:
            souvenir_photo = ('/souvenir-photo', 0)
            location = count_karavan_reqs_type[0]
    else:
        
        if count_karavan_reqs_type[0][0] == '/souvenir-photo':
            souvenir_photo = count_karavan_reqs_type[0]
            location = count_karavan_reqs_type[1]
        else:
            location = count_karavan_reqs_type[0]
            souvenir_photo = count_karavan_reqs_type[1]
                
    res = {'account': {
                        'active': active[1],
                        'noactive': noactive[1]
                        },
           'type': {
               '/send-my-location': location[1],
               '/souvenir-photo': souvenir_photo[1]
            },
        "status-code":200
        }
    
    return res


def add_event_to_karavan(karavan_uuid, event_name):
    check_event_name = db.db.checkDuplicateEventName(karavan_uuid, event_name)
    
    if check_event_name[0] == None or check_event_name == []:
        # valid name
        db.db.addEventToKaravan(karavan_uuid, event_name, uuid.uuid4().hex)
        res = {"result":"Event added successfully" , "status-code":200}
    else:
        # duplicate
        res = {"result":"duplicate name error" , "status-code":400}
    
    return res