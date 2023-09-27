from telegram import InlineKeyboardButton,InlineKeyboardMarkup


keyboard_cancel = [
    [InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel")]
]
reply_markup_cancel = InlineKeyboardMarkup(keyboard_cancel)

keyboard_cancel_help = [
    [InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel")],
    [InlineKeyboardButton("راهنمای ارسال تصویر به صورت فایل", callback_data="/help")]
]
reply_markup_cancel_help = InlineKeyboardMarkup(keyboard_cancel_help)


keyboard_start_user = [
    [InlineKeyboardButton("ارسال موقعیت مکانی", callback_data="/send-my-location")],
    [InlineKeyboardButton("ثبت عکس یادگاری", callback_data="/record-souvenir-photo")]
]
reply_markup_start_user = InlineKeyboardMarkup(keyboard_start_user)


def keyboard_photo_events(events):
    inline_events = []
    for event in events:
        inline_events.append([ InlineKeyboardButton(event, callback_data=events[event]) ])

    reply_markup_photo_event = InlineKeyboardMarkup(inline_events)
    return reply_markup_photo_event

