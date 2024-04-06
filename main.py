from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)
from shazam import shazam_handler
import os
from database import get_tracks
import pymorphy2


async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Привет {user.full_name}, я музыкальный бот, чтобы получить список комманд напишите\n/help"
    await update.message.reply_text(text)


async def help_command(update: Update, context: CallbackContext):
    list_of_commands = ["/start - команда для старта бота",
                        "/help - список всех команд бота",
                        "/shazam - распознавание музыки",
                        "/recognized - список распознанных треков"]

    await update.message.reply_text("\n".join(list_of_commands))


async def recognized_command(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    recognized_tracks = get_tracks(user_id)

    if not recognized_tracks:
        text = "Вы ещё не распознали ни одного трека."
        await update.message.reply_text(text)
        return
    else:
        for track in recognized_tracks:
            text = [f"Исполнитель: {track.artist}",
                    f"Название: {track.title}",]
            if track.album is not None:
                text.append(f"Альбом: {track.album}")
            if track.genre is not None:
                text.append(f"Жанр Произведения: {track.genre}")
            if track.released is not None:
                text.append(f"Дата релиза: {track.released}")
            if track.coverart_url is not None:
                await update.message.reply_photo(track.coverart_url, caption='\n'.join(text))
            else:
                await update.message.reply_text('\n'.join(text))
    c = len(recognized_tracks)

    morph = pymorphy2.MorphAnalyzer()
    if c == 1:
        r = "был распознан"
    else:
        r = "было распознано"
    await update.message.reply_text(f"Всего {r} {c} "
                                    f"{morph.parse('трек')[0].make_agree_with_number(c).word}")


async def unknown_message_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Неопознанная команда или сообщение.")


def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()

    all_handlers = []

    command_handlers = {"start": start_command, "help": help_command}
    for command, function in command_handlers.items():
        all_handlers.append(CommandHandler(command, function))

    unknown_text_handler = MessageHandler(filters.ALL, unknown_message_command)
    recognized_command_handler = CommandHandler("recognized", recognized_command)

    all_handlers.append(recognized_command_handler)
    all_handlers.append(shazam_handler)
    all_handlers.append(unknown_text_handler)

    for handler in all_handlers:
        app.add_handler(handler)

    app.run_polling()


if __name__ == '__main__':
    main()
