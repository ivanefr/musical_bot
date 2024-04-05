from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          CallbackContext, filters, ConversationHandler)
import os
from shazam import Song

WAIT_VOICE = 1


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
    await update.message.reply_text("С помощью этой команды вы можете распознать название и автора интересующегося"
                                    " вам произведения. Пришлите голосовое сообщение с данной музыкой.")
    await update.message.reply_text("Если желаете прекратить функцию shazam отправьте /stop_shazam")
    return WAIT_VOICE


async def audio_recognition(update: Update, context: CallbackContext):
    await update.message.reply_text("Сообщение получено, обработка...")
    audio = update.message.voice
    file = await audio.get_file()
    data = await file.download_as_bytearray()

    song = Song(data)
    await song.recognize_data()
    artist = song.artist
    title = song.title

    if artist and title:
        await update.message.reply_text(f"Трек распознан!!!\nИсполнитель: {artist}\nНазвание: {title}")
    else:
        await update.message.reply_text("Трек не распознался, попытайтесь ещё раз")
        return WAIT_VOICE
    return ConversationHandler.END


async def bad_audio(update: Update, context: CallbackContext):
    if update.message.text == "/stop_shazam":
        await stop_shazam_command(update, context)
        return ConversationHandler.END
    await update.message.reply_text("Это не голосовое сообщение!!!")
    await update.message.reply_text("Если желаете прекратить функцию shazam отправьте /stop_shazam")
    return WAIT_VOICE


async def stop_shazam_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Shazam прекратил свою работу")
    return ConversationHandler.END


async def unknown_message_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Неопознанная команда или сообщение.")


def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()

    all_handlers = []

    # handlers for commands
    command_handlers = {"start": start_command, "help": help_command}
    for command, function in command_handlers.items():
        all_handlers.append(CommandHandler(command, function))

    shazam_handler = ConversationHandler(
        entry_points=[CommandHandler("shazam", shazam_command)],

        fallbacks=[CommandHandler("stop_shazam", stop_shazam_command)],

        states={
            WAIT_VOICE: [MessageHandler(filters.VOICE, audio_recognition),
                         MessageHandler(~filters.VOICE, bad_audio), ]
        },

    )

    # conversation handler for shazam
    all_handlers.append(shazam_handler)

    unknown_text_handler = MessageHandler(filters.ALL, unknown_message_command)
    all_handlers.append(unknown_text_handler)

    for handler in all_handlers:
        app.add_handler(handler)

    app.run_polling()


if __name__ == '__main__':
    main()
