from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputTextMessageContent, ReplyKeyboardRemove
from telegram.ext import (Application, CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, MessageHandler, filters)
import os
from shazam import Track

WAIT_VOICE = 1
EXTRA_INFO = 2


async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    text = f"Привет {user.full_name}, я музыкальный бот, чтобы получить список комманд напишите\n/help"
    await update.message.reply_text(text)


async def help_command(update: Update, context: CallbackContext):
    list_of_commands = ["/start - команда для старта бота",
                        "/help - список всех команд бота",
                        "/shazam - распознавание музыки"]

    await update.message.reply_text("\n".join(list_of_commands))


async def shazam_command(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Распознать музыку", callback_data="recognize_music")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Нажмите на кнопку, чтобы распознать музыку:", reply_markup=reply_markup)

    return WAIT_VOICE


async def recognize_music(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Пришлите голосовое сообщение с музыкой.")


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
        await update.message.reply_text("Трек не распознался, попытайтесь ещё раз")
        return WAIT_VOICE


async def ask_extra_question(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Подробнее", callback_data="info"),
            InlineKeyboardButton("Завершить", callback_data="stop_shazam")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Желаете узнать дополнительную информацию?", reply_markup=reply_markup)


async def info_command(update: Update, context: CallbackContext):
    track = context.user_data["track"]
    album = track.album
    released = track.released
    genre = track.genre
    text = f"Альбом: {album}\nДата релиза: {released}\nЖанр произведения: {genre}"
    await context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=track.coverart_url, caption=text)
    await update.callback_query.edit_message_text("Дополнительная информация:", reply_markup=InlineKeyboardMarkup([]))
    return EXTRA_INFO


async def stop_shazam_command(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.callback_query.edit_message_text("Shazam прекратил свою работу")
    return WAIT_VOICE


async def unknown_message_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Неопознанная команда или сообщение.")


async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == "recognize_music":
        await recognize_music(update, context)
    elif data == "info":
        await info_command(update, context)
    elif data == "stop_shazam":
        await stop_shazam_command(update, context)


def main():
    token = "6438049469:AAEASLen8m4g-qOHGW2L7LUUzkGyKyxpqr4"
    app = Application.builder().token(token).build()

    all_handlers = []

    # handlers for commands
    command_handlers = {"start": start_command, "help": help_command}
    for command, function in command_handlers.items():
        all_handlers.append(CommandHandler(command, function))

    unknown_text_handler = MessageHandler(filters.ALL, unknown_message_command)

    end_conversation_handler = CommandHandler("stop_shazam", stop_shazam_command)
    shazam_handler = ConversationHandler(
        entry_points=[CommandHandler("shazam", shazam_command)],

        fallbacks=[end_conversation_handler],

        states={
            WAIT_VOICE:
                [
                    MessageHandler(filters.VOICE, audio_recognition),
                    end_conversation_handler,
                    unknown_text_handler
                ],
            EXTRA_INFO:
                [
                    CallbackQueryHandler(button_handler, pattern="info"),
                    CallbackQueryHandler(button_handler, pattern="stop_shazam"),
                    end_conversation_handler,
                    unknown_text_handler,
                ]
        },

    )

    # conversation handler for shazam
    all_handlers.append(shazam_handler)

    all_handlers.append(unknown_text_handler)

    all_handlers.append(CallbackQueryHandler(button_handler))

    for handler in all_handlers:
        app.add_handler(handler)

    app.run_polling()


if __name__ == '__main__':
    main()
