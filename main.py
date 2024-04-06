from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)
from shazam import shazam_handler
import os


async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Привет {user.full_name}, я музыкальный бот, чтобы получить список комманд напишите\n/help"
    await update.message.reply_text(text)


async def help_command(update: Update, context: CallbackContext):
    list_of_commands = ["/start - команда для старта бота",
                        "/help - список всех команд бота",
                        "/shazam - распознавание музыки"]

    await update.message.reply_text("\n".join(list_of_commands))


async def unknown_message_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Неопознанная команда или сообщение.")


def main():
    token = os.environ.get("BOT_TOKEN")
    app = Application.builder().token(token).build()

    all_handlers = []

    # handlers for commands
    command_handlers = {"start": start_command, "help": help_command}
    for command, function in command_handlers.items():
        all_handlers.append(CommandHandler(command, function))

    unknown_text_handler = MessageHandler(filters.ALL, unknown_message_command)

    all_handlers.append(shazam_handler)

    all_handlers.append(unknown_text_handler)

    for handler in all_handlers:
        app.add_handler(handler)

    app.run_polling()


if __name__ == '__main__':
    main()
