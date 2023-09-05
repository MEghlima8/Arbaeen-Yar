from telegram import InlineKeyboardButton,InlineKeyboardMarkup


keyboard_cancel = [
    [InlineKeyboardButton("بازگشت به صفحه اصلی", callback_data="/cancel")]
]
reply_markup_cancel = InlineKeyboardMarkup(keyboard_cancel)


keyboard_start_user = [
    [InlineKeyboardButton("ارسال موقعیت مکانی", callback_data="/send-my-location")],
    [InlineKeyboardButton("ثبت عکس یادگاری", callback_data="/record-souvenir-photo")]
]
reply_markup_start_user = InlineKeyboardMarkup(keyboard_start_user)


keyboard_photo_event = [
    [
        InlineKeyboardButton("محرم", callback_data="moharram"),
        InlineKeyboardButton("اربعین", callback_data="arbaeen")
    ],
    [
        InlineKeyboardButton("عید غدیر", callback_data="ghadir"),
        InlineKeyboardButton("عید فطر", callback_data="fetr")
    ],
    [InlineKeyboardButton("سایر", callback_data="other")]

]
reply_markup_photo_event = InlineKeyboardMarkup(keyboard_photo_event)

