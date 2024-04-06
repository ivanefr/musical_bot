from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)
from recognizer import Track

RECOGNIZE_OR_EXIT = 0
WAIT_VOICE = 1
EXTRA_INFO = 2


async def shazam_command(update: Update, context: CallbackContext):
    context.user_data["shazam"] = True

    keyboard = [
        [
            InlineKeyboardButton("Распознать", callback_data="recognize_music"),
            InlineKeyboardButton("Выйти", callback_data="stop_shazam")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Нажмите на кнопку, чтобы распознать музыку:", reply_markup=reply_markup)

    return RECOGNIZE_OR_EXIT


async def recognize_music_callback(update: Update, context: CallbackContext):
    await update.callback_query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Выйти", callback_data="stop_shazam")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text("Пришлите голосовое сообщение с музыкой.",
                                                  reply_markup=reply_markup)

    return WAIT_VOICE


async def audio_recognition(update: Update, context: CallbackContext):
    await update.message.reply_text("Сообщение получено, обработка...")
    audio = update.message.voice
    file = await audio.get_file()
    data = await file.download_as_bytearray()

    track = Track(data)
    await track.recognize_data()

    if track.title:
        context.user_data["track"] = track
        await update.message.reply_text(
            f"Трек распознан!!!\nИсполнитель: {track.artist}\nНазвание:       {track.title}")
        await ask_extra_question(update, context)
        return EXTRA_INFO
    else:
        keyboard = [
            [
                InlineKeyboardButton("Выйти", callback_data="stop_shazam")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Трек не распознался, попытайтесь ещё раз или нажмите кнопку Выйти",
                                        reply_markup=reply_markup)
        return WAIT_VOICE


async def ask_extra_question(update: Update, context: CallbackContext):
    context.user_data["extra_info"] = True
    keyboard = [
        [
            InlineKeyboardButton("Подробнее", callback_data="info"),
            InlineKeyboardButton("Выйти", callback_data="stop_shazam")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Желаете узнать дополнительную информацию?", reply_markup=reply_markup)


async def info_command(update: Update, context: CallbackContext):
    context.user_data["extra_info"] = False

    track = context.user_data["track"]
    album = track.album
    released = track.released
    genre = track.genre
    text = f"Альбом: {album}\nДата релиза: {released}\nЖанр произведения: {genre}"
    if track.coverart_url is not None:
        await context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                                     photo=track.coverart_url,
                                     caption=text)
    else:
        await update.effective_user.send_message(text)
    await update.callback_query.edit_message_text("Дополнительная информация:",
                                                  reply_markup=InlineKeyboardMarkup([]))

    return await stop_shazam_command(update, context)


async def stop_shazam_command(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.effective_user.send_message("Shazam прекратил свою работу")
    return ConversationHandler.END


async def stop_shazam_callback(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.callback_query.edit_message_text("Shazam прекратил свою работу")
    return ConversationHandler.END


async def unknown_message_command(update: Update, context: CallbackContext):
    if context.user_data.get("shazam"):
        if context.user_data.get("extra_info"):
            return await ask_extra_question(update, context)
        keyboard = [
            [
                InlineKeyboardButton("Распознать", callback_data="recognize_music"),
                InlineKeyboardButton("Выйти", callback_data="stop_shazam")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Неопознанная команда или сообщение. Нажмите кнопку для продолжения",
                                        reply_markup=reply_markup)

        return RECOGNIZE_OR_EXIT
    await update.message.reply_text("Неопознанная команда или сообщение.")


unknown_text_handler = MessageHandler(filters.ALL, unknown_message_command)

end_conversation_handler = CommandHandler("stop_shazam", stop_shazam_command)
shazam_handler = ConversationHandler(
    entry_points=[CommandHandler("shazam", shazam_command)],

    fallbacks=[end_conversation_handler],

    states={
        RECOGNIZE_OR_EXIT:
            [
                CallbackQueryHandler(recognize_music_callback, pattern="recognize_music"),
                CallbackQueryHandler(stop_shazam_callback, pattern="stop_shazam"),
                end_conversation_handler,
                unknown_text_handler,
            ],
        WAIT_VOICE:
            [
                MessageHandler(filters.VOICE, audio_recognition),
                CallbackQueryHandler(stop_shazam_callback, pattern="stop_shazam"),
                end_conversation_handler,
                unknown_text_handler
            ],
        EXTRA_INFO:
            [
                CallbackQueryHandler(info_command, pattern="info"),
                CallbackQueryHandler(stop_shazam_callback, pattern="stop_shazam"),
                end_conversation_handler,
                unknown_text_handler,
            ]
    },

)
