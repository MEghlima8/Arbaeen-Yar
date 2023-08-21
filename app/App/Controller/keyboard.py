from telegram import InlineKeyboardButton,InlineKeyboardMarkup

keyboard_start = [
    [InlineKeyboardButton("ورود مدیران", callback_data="/create-new-karavan-manager")],
    [InlineKeyboardButton("ورود اعضا", callback_data="/signin-karavan-user")]
]
reply_markup_start = InlineKeyboardMarkup(keyboard_start)


keyboard_start_manager = [
    [InlineKeyboardButton("اضافه کردن زائر به کاروان", callback_data="/add-new-user-to-karavan")]
]
reply_markup_start_manager = InlineKeyboardMarkup(keyboard_start_manager)


keyboard_cancel = [
    [InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel")]
]
reply_markup_cancel = InlineKeyboardMarkup(keyboard_cancel)

