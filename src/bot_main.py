import os
import logging
import warnings
from dotenv import load_dotenv

from telegram import Update
from telegram.warnings import PTBUserWarning
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

# Set path context for relative imports inside src module
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from handlers.bot_handlers import (
    start,
    button_handler,
    cancel,
    unknown,
    PICKING_LANG,
    PICKING_CLASS,
)

warnings.filterwarnings("ignore", category=PTBUserWarning)
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

def main():
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env")

    app = Application.builder().token(BOT_TOKEN).concurrent_updates(True).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_handler, pattern="^change_class$"),
            CallbackQueryHandler(button_handler, pattern="^change_lang$"),
            CallbackQueryHandler(button_handler, pattern="^hw_mine$"),
        ],
        states={
            PICKING_LANG: [
                CallbackQueryHandler(button_handler, pattern="^lang:"),
<<<<<<< HEAD
                CallbackQueryHandler(button_handler, pattern="^menu_back$"),
            ],
            PICKING_CLASS: [
                CallbackQueryHandler(button_handler, pattern="^pick:"),
                CallbackQueryHandler(button_handler, pattern="^menu_back$"),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
        ],
=======
            ],
            PICKING_CLASS: [
                CallbackQueryHandler(button_handler, pattern="^pick:"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
>>>>>>> 0107596f5457f0bb1b3a42df5df7b8180e7999da
        per_chat=True,
        per_message=False,
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()
