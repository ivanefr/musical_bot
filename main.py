from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
import os


async def start_command(update: Update, context: CallbackContext):
    user = update.effective_user

    text = f"Привет {user.full_name}, я музыкальный бот, чтобы получить список комманд напишите\n/help"
    await update.message.reply_text(text)


async def help_command(update: Update, context: CallbackContext):
    list_of_commands = ["/start - команда для старта бота",
                        "/help - список всех команд бота", ]

    await update.message.reply_text("\n".join(list_of_commands))


def main():
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()

    command_handlers = {"start": start_command, "help": help_command}

    for command, function in command_handlers.items():
        app.add_handler(CommandHandler(command, function))

    app.run_polling()


if __name__ == '__main__':
    main()
