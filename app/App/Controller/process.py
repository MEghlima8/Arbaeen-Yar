from App.Controller.keyboard import reply_markup_start, reply_markup_start_manager, reply_markup_cancel
from App.Controller import db_postgres_controller as db
from App.Controller import validation
import random
import string
import uuid
import json
from datetime import datetime
from jdatetime import datetime as jdatetime


def get_datetime():
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
    now_datetime = json.dumps({'date':date , 'time':time})
    return now_datetime



# Create karavan
async def create_new_karavan(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('get-karavan-manager-fullname', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا نام و نام خانوادگی خودتان را ارسال کنید:',reply_markup=reply_markup_cancel)
    return

# Create karavan - get karavan manager fullname
async def get_karavan_manager_fullname(_update, context, text, _STEP, chat_id):
    if validation.check_fullname_persian(text):
        db.db.changeFirstTextMsg(text,chat_id) # store fullname of karavan manager in database
        db.db.changeUserSTEP('get-karavan-name', chat_id)
        await context.bot.send_message(chat_id=chat_id, text='لطفا نام کاروان را ارسال کنید. \nاین نام هر نامی که می خواهید می تواند باشد. \n توجه: دیگر اعضای کاروان این نام را مشاهده خواهند کرد',reply_markup=reply_markup_cancel)
    else:
        await context.bot.send_message(chat_id=chat_id, text='نام و نام خانوادگی باید فقط شامل حروف فارسی باشد')
    return
            
            
# Create karavan - get karavan name from manager
async def get_karavan_name(_update, context, text, _STEP, chat_id):
    karavan_manger_name = db.db.getFirstTextMsg(chat_id)
    # text is karavan name
    karavan_uuid = uuid.uuid4().hex
    user_uuid = db.db.getUserUUID(chat_id=chat_id)
    db.db.createKaravan(karavan_uuid, text, user_uuid)
    db.db.addUserToKaravanUsers(karavan_users_id=uuid.uuid4().hex, user_uuid=user_uuid, karavan_uuid=karavan_uuid, whois='manager')
    db.db.updateUserToManager(chat_id,karavan_manger_name)
    await context.bot.send_message(chat_id=chat_id, text='اطلاعات شما با موفقیت ثبت شد',reply_markup=reply_markup_cancel)
    return



# Add new user to karavan - get user fullname from manager
async def add_new_user_to_karavan(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('get-karavan-user-fullname', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا نام و نام خانوادگی زائر را وارد کنید',reply_markup=reply_markup_cancel)

# Add new user to karavan - create new user
async def get_karavan_user_fullname(_update, context, text, _STEP, chat_id):
    manager_uuid = db.db.getUserUUID(chat_id)
    karavan_uuid = db.db.getKaravanUUID(manager_uuid)
    user_fullname = text
    user_uuid = uuid.uuid4().hex
    username = ''.join(random.choice(string.ascii_letters) for _ in range(12))
    password = ''.join(random.choice(string.ascii_letters) for _ in range(12))
    db.db.addUsernamePassToKaravan(user_uuid, user_fullname, username, password)
    db.db.addUserToKaravanUsers(uuid.uuid4().hex, user_uuid, karavan_uuid, 'user')
    await context.bot.send_message(chat_id=chat_id, text='ایجاد حساب کاربری برای {} با موفقیت انجام شد \n جهت ورود زائر به ربات اطلاعات زیر را برای زائر ارسال کنید : \n نام کاربری : {} \nرمز عبور : {}'.format(user_fullname, username, password),reply_markup=reply_markup_cancel)


# Signin user to account - for the first time
async def signin_karavan_user(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('get-user-username-to-signin', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا نام کاربری خود را وارد کنید : \nاگر حساب ندارید از مدیر کاروان بخواهید برایتان یک حساب ایجاد کند',reply_markup=reply_markup_cancel)
    return

# Signin user to account - Get user username
async def get_user_username_to_signin(_update, context, text, _STEP, chat_id):
    db.db.changeFirstTextMsg(text,chat_id) # Store user username in database
    db.db.changeUserSTEP('get-user-password-to-signin', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا رمز عبور خود را وارد کنید :',reply_markup=reply_markup_cancel)
    return 

# Signin user to account - Get user password and check info
async def get_user_password_to_signin(_update, context, text, _STEP, chat_id):
    username = db.db.getFirstTextMsg(chat_id)
    password = text
    user_uuid = db.db.checkMatchUsernamePassword(username, password)
    if user_uuid != []: # Wrong username and password
        user_uuid = user_uuid[0][0]
        # Remove the additional user record that created and update info of the user that created by manager.
        db.db.activeUserAccount(user_uuid,chat_id)
        await context.bot.send_message(chat_id=chat_id, text='اطلاعات شما با موفقیت تایید شد \nاز حالا میتوانید از امکانات ربات استفاده کنید',reply_markup=reply_markup_cancel)
    else:
        await context.bot.send_message(chat_id=chat_id, text='نام کاربری یا رمز عبور اشتباه می باشد',reply_markup=reply_markup_cancel)
        
    
# Send my location - send message to user to send location
async def send_my_location(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('get-user-location', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا موقعیت مکانی خود را ارسال کنید',reply_markup=reply_markup_cancel)
    return


# Send my location - get user location
async def get_user_location(update, context, _text, _STEP, chat_id):
    try :
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
    except:
        await context.bot.send_message(chat_id=chat_id, text='لطفا موقعیت مکانی خودتان را ارسال کنید', reply_markup=reply_markup_cancel)
        return
    location = json.dumps({
                        "latitude": latitude ,
                        "longitude": longitude,
                        })
    db.db.changeFirstTextMsg(location,chat_id)
    db.db.changeUserSTEP('get-user-caption-location', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا توضیحاتی را در مورد موقعیت مکانی خود شرح دهید برای مثال : \n- تا یک ساعت دیگر در این مکان استراحت خواهم کرد \n- در حال حرکت به سمت حرم هستم',reply_markup=reply_markup_cancel)
    
    
# Send my location - get user caption location and store in database   
async def get_user_caption_location(_update, context, location_caption, _STEP, chat_id):
    db.db.changeUserSTEP('home', chat_id)
    location = db.db.getFirstTextMsg(chat_id)
    params = json.loads(location)
    params["caption"] = location_caption
    params = json.dumps(params)
    j_date_time = get_datetime()
    user_uuid = db.db.getUserUUID(chat_id)
    db.db.addReqToDb(uuid.uuid4().hex, user_uuid, '/send-my-location', params, j_date_time, 'done')
    await context.bot.send_message(chat_id=chat_id, text='موقعیت مکانی شما با موفقیت ثبت شد', reply_markup=reply_markup_cancel)