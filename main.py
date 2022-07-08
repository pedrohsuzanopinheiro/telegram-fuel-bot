import os

from dotenv import load_dotenv
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update

from spreadsheet import update_spreadsheet

load_dotenv()

updater = Updater(os.environ.get("BOTFATHER_TOKEN"), use_context=True)

introduction = """
Get the hell out of here!
    """


def start(update: Update, context: CallbackContext):
    update.message.reply_text(introduction)


def help(update: Update, context: CallbackContext):
    update.message.reply_text(introduction)


def register(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"""
Parâmetros recebidos!
Valor (em R$): {context.args[0]}
Litros abastecidos: {context.args[1]}
KM atual: {context.args[2]}
    """
    )
    try:
        update_spreadsheet(context.args[0], context.args[1], context.args[2])
        update.message.reply_text("Planilha atualizada!")
    except Exception as e:
        update.message.reply_text(f"Algo de errado rolou. Erro: {e}")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text
    )


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text
    )


updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", help))
updater.dispatcher.add_handler(CommandHandler("register", register))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(
    MessageHandler(
        # Filters out unknown commands
        Filters.command,
        unknown,
    )
)

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()