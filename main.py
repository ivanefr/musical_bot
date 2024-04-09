from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)
from shazam import shazam_handler
from top_tracks import get_top_tracks_in_country, get_top_world_tracks
import os
from database import get_tracks
import pymorphy2

reply_keyboard = [['/shazam', '/recognized'],
                  ['/top_tracks', '/top_tracks_ru'],
                  ['/help']]
COMMANDS_MARKUP = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)


async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Привет {user.full_name}, я музыкальный бот, чтобы получить список комманд напишите\n/help"
    await update.message.reply_text(text, reply_markup=COMMANDS_MARKUP)


async def help_command(update: Update, context: CallbackContext):
    list_of_commands = ["/start - команда для старта бота",
                        "/help - список всех команд бота",
                        "/shazam - распознавание музыки",
                        "/recognized - список распознанных треков",
                        "/top_tracks - самые часто распознаваемые треки в мире",
                        "/top_tracks_ru - самые часто распознаваемые треки в России"]

    await update.message.reply_text("\n".join(list_of_commands), reply_markup=COMMANDS_MARKUP)


async def top_tracks_command(update: Update, context: CallbackContext, track_list, message):
    """Команда для получения самых часто распознаваемых треков со всего мира"""

    arr = []

    for i, track in enumerate(track_list, start=1):
        # Если в полученном объекте есть ссылка на apple music
        # добавляем html вида <a href="http://www.url.com/">text</a>
        link = track.apple_music_url
        if link:
            arr.append(f"{i}. <a href=\"{link}\">{track.title} - {track.subtitle}</a>")
        else:
            arr.append(f"{i}. {track.title} - {track.subtitle}")

    # Отправка сообщений с топ-треками
    await update.message.reply_text(message)
    await update.message.reply_text("\n".join(arr), parse_mode="HTML", reply_markup=COMMANDS_MARKUP)


async def top_tracks_world_command(update: Update, context: CallbackContext):
    top_tracks_world = await get_top_world_tracks()
    await top_tracks_command(update, context, top_tracks_world, "Наиболее распознаваемые треки мира:")


async def top_tracks_ru_command(update: Update, context: CallbackContext):
    top_tracks_ru = await get_top_tracks_in_country("RU")
    await top_tracks_command(update, context, top_tracks_ru, "Наиболее распознаваемые треки России:")


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
                    f"Название: {track.title}", ]
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
                                    f"{morph.parse('трек')[0].make_agree_with_number(c).word}",
                                    reply_markup=COMMANDS_MARKUP)


async def unknown_message_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Неопознанная команда или сообщение.",
                                    reply_markup=COMMANDS_MARKUP)


def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()

    all_handlers = []

    command_handlers = {"start": start_command, "help": help_command}
    for command, function in command_handlers.items():
        all_handlers.append(CommandHandler(command, function))

    unknown_text_handler = MessageHandler(filters.ALL, unknown_message_command)
    top_tracks_command_handler = CommandHandler("top_tracks", top_tracks_world_command)
    top_tracks_ru_handler = CommandHandler("top_tracks_ru", top_tracks_ru_command)
    recognized_command_handler = CommandHandler("recognized", recognized_command)

    all_handlers.append(recognized_command_handler)
    all_handlers.append(shazam_handler)
    all_handlers.append(top_tracks_command_handler)
    all_handlers.append(top_tracks_ru_handler)
    all_handlers.append(unknown_text_handler)

    for handler in all_handlers:
        app.add_handler(handler)

    app.run_polling()


if __name__ == '__main__':
    main()
