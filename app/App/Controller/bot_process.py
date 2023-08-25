from App.Controller.keyboard import reply_markup_start, reply_markup_start_manager, reply_markup_cancel
from App.Controller import db_postgres_controller as db
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


# Signin user to account - Get user username
async def get_user_username_to_signin(_update, context, text, _STEP, chat_id):
    db.db.changeFirstTextMsg(text,chat_id) # Store user username in database
    db.db.changeUserSTEP('get-user-password-to-signin', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='لطفا رمز عبور خود را وارد کنید :')
    return 


# Signin user to account - Get user password and check info
async def get_user_password_to_signin(_update, context, text, _STEP, chat_id):
    username = db.db.getFirstTextMsg(chat_id)
    password = text
    user_info = db.db.checkMatchUsernamePassword(username, password)
    if user_info != [] and user_info[0][2] == 'true':
        user_uuid = user_info[0][0]
        # Remove the additional user record that created and update info of the user that created by manager.
        db.db.activeUserAccount(user_uuid,chat_id)
        await context.bot.send_message(chat_id=chat_id, text='اطلاعات شما با موفقیت تایید شد \nاز حالا میتوانید از امکانات ربات استفاده کنید',reply_markup=reply_markup_cancel)
    else:
        # Wrong username and password
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