from App import config
from App.Controller import db_postgres_controller as db
from App.Controller import bot_process
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, MessageHandler,  filters, ContextTypes
from re import match
from App.Controller.keyboard import reply_markup_start_user
import threading
import web_server
import uuid


TOKEN = config.configs['BOT_TOKEN']
BASE_URL = config.configs['BASE_URL']
BASE_FILE_URL = config.configs['BASE_FILE_URL']
     

async def cancel(_update, context, _text, _STEP, chat_id):
    account_status = db.db.checkIsUserActive(chat_id)
    
    if account_status == [] or account_status[0][0] is None:
        db.db.addUserFromBotToDB(uuid.uuid4().hex, chat_id)
        await context.bot.send_message(chat_id, text='بازگشت به صفحه اصلی انجام شد')
        db.db.changeUserSTEP('get-user-username-to-signin', chat_id)   
    elif account_status[0][0] and account_status[0][1]['status']=='true':
        await context.bot.send_message(chat_id, text='بازگشت به صفحه اصلی انجام شد \nیکی از گزینه های زیر را انتخاب کنید', reply_markup=reply_markup_start_user)
        db.db.changeUserSTEP('home', chat_id)
        

# Start bot
async def start(_update, context, _text, _STEP, chat_id):
    account_status = db.db.checkIsUserActive(chat_id)
    
    if account_status == [] or account_status[0][0] is None:
        db.db.addUserFromBotToDB(uuid.uuid4().hex, chat_id)
        await context.bot.send_message(chat_id=chat_id, text='سلام به ربات {} خوش آمدید \nلطفا نام کاربری خود را وارد کنید :'.format(config.configs['SYSTEM_NAME']))
        db.db.changeUserSTEP('get-user-username-to-signin', chat_id)
        return
    elif account_status[0][0] and account_status[0][1]['status']=='true':
        await context.bot.send_message(chat_id, text='خوش آمدید \nیکی از گزینه های زیر را انتخاب کنید', reply_markup=reply_markup_start_user)
        db.db.changeUserSTEP('home', chat_id)
        return


async def help(_update, context, _text, _STEP, chat_id):
    help_user_send_file = config.configs['HELP_USER_SEND_FILE']
    await context.bot.send_video(chat_id, help_user_send_file)
    await context.bot.send_message(chat_id, text=' برای ارسال تصویر به صورت فایل ابتدا از سمت چپ و پایین بر روی آیکون + ضربه بزنید سپس بر روی ارسال به صورت فایل ضربه بزنید')


commands = [
    # text - step - callback
    
    # COMMANDS
    [r"/start", r".+", start], # text - step - callback
    [r"/help", r".+", help],
    [r"/cancel", r".+", cancel],
    
    [r"/send-my-location", r".+", bot_process.send_my_location],
    
    [r"/record-souvenir-photo", r".+", bot_process.record_souvenir_photo],
    
    [r".", r"handle-photo-event", bot_process.handle_photo_event],
    
    [r".+", r"get-user-username-to-signin", bot_process.get_user_username_to_signin],
    [r".+", r"get-user-password-to-signin", bot_process.get_user_password_to_signin],
    
    [r".+", r"get-user-location", bot_process.get_user_location],
    
    [r".+", r"handle-record-souvenir-photo", bot_process.handle_record_souvenir_photo],
]


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get chat id and message text
    try:
        chat_id = update.effective_chat.id
        text = update.callback_query.data
        STEP = db.db.getUserSTEP(chat_id)[0]
        
    except:
        try:
            chat_id = update.effective_chat.id
            text = update.callback_query.data
        except:
            text = update.message.text
            chat_id = update.message.chat_id
        
    if text is None:
        # user sent media or location, not a text
        text = '/none'
    
    # Store text in database and get text,STEP of user
    try:
        text,STEP = db.db.changeSecondTextMsg(text, chat_id) 
    except: # Save user info in the database
        await start(update, context, None, None, chat_id)
        return
    
    for command in commands:
        valid_command = False
        pattern, step, callback = command
        if match(pattern, text) and match(step, STEP):
            valid_command = True
            await callback(update,context,text,STEP,chat_id)
            break
        
    account_status = db.db.checkIsUserActive(chat_id)
    if account_status[0][0] and account_status[0][1]['status']=='disable':
        await context.bot.send_message(chat_id, text='حسابتان توسط مدیر کاروان غیرفعال شده است. از او بخواهید دوباره حسابتان را فعال کند')
        return
        
    if not valid_command:
        await context.bot.send_message(chat_id=chat_id, text='لطفا یک دستور معتبر وارد کنید!')
           
           


def main():
    
    # Run web server
    t = threading.Thread(None, web_server.main, None, ())
    t.start()
    
    app = Application.builder().token(TOKEN).base_url(BASE_URL).base_file_url(BASE_FILE_URL).build()
    
    # Messages
    app.add_handler(MessageHandler(filters=filters.ALL, callback=message))
    # Inline Keyboard
    app.add_handler(CallbackQueryHandler(message))

    # Polls the bot
    print('Polling...')
    app.run_polling(allowed_updates=Update.ALL_TYPES)

main()