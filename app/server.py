from App import config
from App.Controller.user_controller import Manager
from App.Controller import db_postgres_controller as db
from App.Controller import bot_process
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler,  filters, ContextTypes
from re import match
from App.Controller.keyboard import reply_markup_start, reply_markup_start_manager, reply_markup_cancel, reply_markup_start_user
import time
import threading
import web_server


TOKEN = config.configs['BOT_TOKEN']
BASE_URL = config.configs['BASE_URL']
BASE_FILE_URL = config.configs['BASE_FILE_URL']
     

async def cancel(_update, context, _text, _STEP, chat_id):
    whois = Manager(chat_id).whoIs()
    if whois == 'false':
        await context.bot.send_message(chat_id, text='صفحه اصلی \nبرای شروع یکی از گزینه های زیر را انتخاب کنید', reply_markup=reply_markup_start)
    elif whois == 'manager':
        await context.bot.send_message(chat_id, text='بازگشت به صفحه اصلی انجام شد', reply_markup=reply_markup_start_manager)
    else:
        await context.bot.send_message(chat_id, text='بازگشت به صفحه اصلی انجام شد', reply_markup=reply_markup_start_user)
    db.db.changeUserSTEP('home', chat_id)



# Start bot
async def start(_update, context, _text, _STEP, chat_id):
    db.db.changeUserSTEP('home', chat_id)
    whois = Manager(chat_id).whoIs()
    if whois == 'manager':
        await context.bot.send_message(chat_id, text='به ربات اربعین یار خوش برگشتید', reply_markup=reply_markup_start_manager)
        return
    elif whois == 'user':
        await context.bot.send_message(chat_id, text='به ربات اربعین یار خوش برگشتید', reply_markup=reply_markup_start_user)
        return
    user = Manager(chat_id=chat_id)
    user.signup()
    await context.bot.send_message(chat_id=chat_id, text='سلام به ربات {} خوش آمدید \nاگر عضو یک کاروان هستید بر روی گزینه ورود اعضا ضربه بزنید \nاگر مدیر یک کاروان هستید بر روی گزینه ورود مدیران ضربه بزنید'.format(config.configs['SYSTEM_NAME']), reply_markup=reply_markup_start)



commands = [
    # text - step - callback
    
    # COMMANDS
    [r"/start", r".+", start], # text - step - callback
    # [r"/help", r".+", help],
    [r"/cancel", r".+", cancel],
    
    [r"/signin-karavan-user", r".+", bot_process.signin_karavan_user],
    
    [r"/send-my-location", r".+", bot_process.send_my_location],
    
    
    
    # [r".+", r"get-karavan-user-fullname", bot_process.get_karavan_user_fullname],
    
    [r".+", r"get-user-username-to-signin", bot_process.get_user_username_to_signin],
    [r".+", r"get-user-password-to-signin", bot_process.get_user_password_to_signin],
    
    [r".+", r"get-user-location", bot_process.get_user_location],
    [r".+", r"get-user-caption-location", bot_process.get_user_caption_location],
    
]


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Get chat id and message text
    # import pdb; pdb.set_trace()
    try:
        chat_id = update.effective_chat.id
        text = update.callback_query.data
        STEP = db.db.getUserSTEP(chat_id)[0]
        
        # The user must complete the route or cancel. User can't go to another route while user is in a route
        if STEP != 'home' and (text != '/cancel' and text !='/help' ):
            await context.bot.send_message(chat_id=chat_id, text='لطفا درخواست خود را تکمیل یا بر روی بازگشت به صفحه اصلی ضربه بزنید.')
            return
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