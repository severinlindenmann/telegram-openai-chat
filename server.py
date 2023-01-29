import logging
import os
from dotenv import load_dotenv
import openai


################VENV#######################
load_dotenv()

STATUS = os.getenv('STATUS')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
TELEGRAM_USERS = os.getenv('TELEGRAM_USERS')
TELEGRAM_USERS = TELEGRAM_USERS.split(",")


################OPENAI#######################
openai.api_key = OPENAI_TOKEN

def openai_api_call(msg,prefix=""):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prefix + msg,
    temperature=0.9,
     max_tokens=1048,
     top_p=1,
     frequency_penalty=0.0,
     presence_penalty=0.6,
    )
    return response["choices"][0]["text"]
    
print("Running: %s" % STATUS)

################TELEGRAM BOT#######################
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""
Verwenden einen der folgenden Commands:
/uebersetzen_ungarisch "Meine Nachricht"
/uebersetzen_deutsch "Meine Nachricht"
/korrigieren_deutsch "Meine Nachricht"
/umschreiben_deutsch "Meine Nachricht"
/chatgpt "bitte schreibe mir Ideen zu diesem Thema: Umweltverschmutzung"
""")


async def uebersetzen_ungarisch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends Translate Request to OPENAI"""
    if str(update.message.chat.id) in TELEGRAM_USERS:
        await update.message.reply_text(openai_api_call(update.message.text,"bitte übersetze den Text auf ungarisch:"))
    else:
        await update.message.reply_text('Sorry you are unauthorized')

async def uebersetzen_deutsch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends Translate Request to OPENAI"""
    if str(update.message.chat.id) in TELEGRAM_USERS:
        await update.message.reply_text(openai_api_call(update.message.text,"bitte übersetze den Text auf ungarisch:"))
    else:
        await update.message.reply_text('Sorry you are unauthorized')
        
async def korrigieren_deutsch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends Translate Request to OPENAI"""
    if str(update.message.chat.id) in TELEGRAM_USERS:
        await update.message.reply_text(openai_api_call(update.message.text,"bitte korrigiere mein Deutsch:"))
    else:
        await update.message.reply_text('Sorry you are unauthorized')

async def umschreiben_deutsch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends Translate Request to OPENAI"""
    if str(update.message.chat.id) in TELEGRAM_USERS:
        await update.message.reply_text(openai_api_call(update.message.text,"schreibe meinen Text um:"))
    else:
        await update.message.reply_text('Sorry you are unauthorized')
        
async def chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends Translate Request to OPENAI"""
    if str(update.message.chat.id) in TELEGRAM_USERS:
        await update.message.reply_text(openai_api_call(update.message.text))
    else:
        await update.message.reply_text('Sorry you are unauthorized')
            
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    if str(update.message.chat.id) in TELEGRAM_USERS:
        await update.message.reply_text(update.message.text)
    else:
        print(update.message.chat.id)
        await update.message.reply_text('Sorry you are unauthorized: ' + str(update.message.chat.id))

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("uebersetzen_ungarisch", uebersetzen_ungarisch))
    application.add_handler(CommandHandler("uebersetzen_deutsch", uebersetzen_deutsch))
    application.add_handler(CommandHandler("korrigieren_deutsch", korrigieren_deutsch))
    application.add_handler(CommandHandler("umschreiben_deutsch", umschreiben_deutsch))
    application.add_handler(CommandHandler("chatgpt", umschreiben_deutsch))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()