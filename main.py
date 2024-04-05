from telegram import Update
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          CallbackContext, filters, ConversationHandler)
import os
from shazam import Recognizer

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
    await update.message.reply_text("С помощью этой команды вы можете распознать название и автора интересующегося"
                                    " вам произведения. Пришлите голосовое сообщение с данной музыкой.")
    await update.message.reply_text("Если желаете прекратить функцию shazam отправьте /stop_shazam")
    return WAIT_VOICE


async def audio_recognition(update: Update, context: CallbackContext):
    await update.message.reply_text("Сообщение получено, обработка...")
    audio = update.message.voice
    file = await audio.get_file()
    data = await file.download_as_bytearray()

    audio_recognizer = Recognizer(data)
    await audio_recognizer.recognize_data()
    track = await audio_recognizer.track
    artist = await audio_recognizer.artist

    if artist and track:
        context.user_data["artist"] = artist
        context.user_data["track"] = track
        await update.message.reply_text(f"Трек распознан!!!\nИсполнитель: {artist.name}\nНазвание: {track.title}")
        await ask_extra_question(update, context)
    else:
        await update.message.reply_text("Трек не распознался, попытайтесь ещё раз")
        return WAIT_VOICE


async def ask_extra_question(update: Update, context: CallbackContext):
    commands = ["/artist - Подробнее узнать об исполнителе",
                "/track - Подробнее узнать о произведении",
                ""]
    await update.message.reply_text("Желаете узнать допольнительную информацию?\n" + "\n".join(commands))
    return EXTRA_INFO


async def bad_audio(update: Update, context: CallbackContext):
    await unknown_message_command(update, context)
    return WAIT_VOICE


async def stop_shazam_command(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.message.reply_text("Shazam прекратил свою работу")
    return ConversationHandler.END


async def unknown_message_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Неопознанная команда или сообщение.")


async def artist_info_command(update: Update, context: CallbackContext):
    return context.user_data["artist"]


async def track_info_command(update: Update, context: CallbackContext):
    return context.user_data["track"]


def main():
    token = os.environ["BOT_TOKEN"]
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
                    CommandHandler("artist", artist_info_command),
                    CommandHandler("track", track_info_command),
                    end_conversation_handler,
                    unknown_text_handler,
                ]
        },

    )

    # conversation handler for shazam
    all_handlers.append(shazam_handler)

    all_handlers.append(unknown_text_handler)

    for handler in all_handlers:
        app.add_handler(handler)

    app.run_polling()


if __name__ == '__main__':
    main()
