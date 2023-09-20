from App.Controller.keyboard import reply_markup_cancel, reply_markup_photo_event, reply_markup_cancel_help
from App.Controller import db_postgres_controller as db
import uuid
import json
from datetime import datetime
from jdatetime import datetime as jdatetime
from App import config
import os
import requests
import hashlib
import requests
import PIL.Image
import PIL.ExifTags


events = {'moharram':'محرم', 'arbaeen':'اربعین', 'ghadir':'غدیر', 'fetr':'فطر', 'other':'سایر'}


# Get image location coordinate
def get_image_location(img_path):
    
    img = PIL.Image.open(img_path)
    try:
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k , v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        north = exif['GPSInfo'][2]
        east = exif['GPSInfo'][4]
    
    except:
        # Location not recorded in image details
        return (None, None)
    
    
    lat = ((((north[0] * 60) + north[1]) * 60) + north[2]) / 60 / 60
    long = ((((east[0] * 60) + east[1]) * 60) + east[2]) / 60 / 60
    
    lat, long = float(lat), float(long) # Convert fraction to float
    
    return (lat, long)
        

# Get address from coordinates
def get_coordinates_address(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    response = requests.request("GET", url, headers={}, data="")
    return response.text

# Save media in local storage
def save_media(path, mime_type, user_id):
    config_path = '.' + config.configs["UPLOAD_USER_FILE"] + str(user_id) + '/'
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        
    response = requests.get(path)
    path = config_path + uuid.uuid4().hex + '.' + mime_type
    with open(path, 'wb') as file:
        file.write(response.content)
    return path


def get_datetime():
    jdate = jdatetime.fromgregorian(datetime=datetime.now())
    hour = jdate.hour + 3
    minute = jdate.minute + 30
    second = jdate.second
    if minute > 59 :
       minute -= 60
       hour +=1
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
    password = hashlib.md5(text.encode("utf-8")).hexdigest()
    
    user_info = db.db.checkMatchUsernamePassword(username, password)
    if user_info != [] and user_info[0][2] == 'true':
        user_uuid = user_info[0][0]
        
        # Remove the additional user record that created and update info of the user that created by manager.
        db.db.activeUserAccount(user_uuid,chat_id)
        karavan_name = db.db.getKaravanNameFromUserInfo(user_uuid)
        await context.bot.send_message(chat_id=chat_id, text='به {} خوش آمدید \n حالا میتوانید از امکانات ربات استفاده کنید'.format(karavan_name) , reply_markup=reply_markup_cancel)
    else:
        db.db.changeUserSTEP('get-user-username-to-signin', chat_id)
        # Wrong username and password
        await context.bot.send_message(chat_id=chat_id, text='نام کاربری یا رمز عبور اشتباه می باشد \nنام کاربری را مجدد وارد کنید :')
        
    
    
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
    
    # Get postal address from coordinates
    address = get_coordinates_address(latitude,longitude)
    
    db.db.changeUserSTEP('home', chat_id)
    j_date_time = get_datetime()
    user_uuid = db.db.getUserUUIDFromChatId(chat_id)
    karavan_uuid = db.db.getKaravanUUIDFromUser(user_uuid)
    db.db.addReqToDb(uuid.uuid4().hex, user_uuid, karavan_uuid, '/send-my-location', address, j_date_time, 'done')
    await context.bot.send_message(chat_id=chat_id, text='موقعیت مکانی شما با موفقیت ثبت شد', reply_markup=reply_markup_cancel)
    
    
    
# Record a souvenir photo - send message to get event
async def record_souvenir_photo(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('handle-photo-event', chat_id)
    await context.bot.send_message(chat_id=chat_id, text='رویداد مورد نظر خود را انتخاب کنید :',reply_markup=reply_markup_photo_event)

# Record a souvenir photo - send message to get image
async def handle_photo_event(_update, context, text, _STEP, chat_id):
    if text in events.keys():
        db.db.changeFirstTextMsg(text,chat_id) # Store event name in database
        db.db.changeUserSTEP('handle-record-souvenir-photo', chat_id)
        await context.bot.send_message(chat_id=chat_id, text=''' تصویر مورد نظر را به صورت فایل ارسال کنید :\nاگر به صورت فایل ارسال نکنید یا در زمان عکس گرفتن موقعیت مکانی دستگاه شما خاموش باشد موقعیت مکانی شما ثبت نخواهد شد''',
                                       reply_markup = reply_markup_cancel_help)
    else:
        await context.bot.send_message(chat_id=chat_id, text='لطفا یک رویداد را انتخاب کنید')
    

# Record a souvenir photo - save photo
async def handle_record_souvenir_photo(update, context, _text, _STEP, chat_id):
    event_name = db.db.getFirstTextMsg(chat_id)
    
    # Check the user sent image or not
    mime_type = update.message.document.mime_type.split('/')  # 'image/png'
    if mime_type[0] != 'image':
        await context.bot.send_message(chat_id=chat_id, text='لطفا فقط تصویر ارسال کنید',reply_markup=reply_markup_cancel)
        return
    
    file = await context.bot.get_file(update.message.document)
    j_date_time = get_datetime()
    
    # save image in local
    path = save_media(file.file_path, mime_type[1], chat_id)
    
    lat,lon = get_image_location(path)
    if lat is None :
        address = 'empty'
    else :
        address = json.loads(get_coordinates_address(lat , lon))
    
    params = json.dumps({"path":path, "event":event_name, "address":address})
    
    user_uuid = db.db.getUserUUIDFromChatId(chat_id)
    karavan_uuid = db.db.getKaravanUUIDFromUser(user_uuid)
    
    # Add request to database
    db.db.addReqToDb(uuid.uuid4().hex, user_uuid, karavan_uuid, '/souvenir-photo', params, j_date_time, 'done')
    await context.bot.send_message(chat_id=chat_id, text='تصویر با موفقیت ثبت شد',reply_markup=reply_markup_cancel)
    db.db.changeUserSTEP('home', chat_id)