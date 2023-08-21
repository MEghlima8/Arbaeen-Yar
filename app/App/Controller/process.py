from App.Controller.keyboard import reply_markup_start, reply_markup_start_manager, reply_markup_cancel
from App.Controller import db_postgres_controller as db
from App.Controller import validation
import random
import string
import uuid


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
    await context.bot.send_message(chat_id=chat_id, text='ایجاد حساب کاربری برای زائر {} با موفقیت انجام شد \n جهت ورود زائر به ربات اطلاعات زیر را برای زائر ارسال کنید : \n نام کاربری : {} \nرمز عبور : {}'.format(user_fullname, username, password),reply_markup=reply_markup_cancel)
