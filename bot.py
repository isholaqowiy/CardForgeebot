import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import database
import handlers
from config import BOT_TOKEN

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database.init_db())

    if not BOT_TOKEN:
        print("Fatal error: Missing BOT_TOKEN environmental deployment property configuration data.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.start_convo, pattern="^menu_create$")],
        states={
            handlers.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_name)],
            handlers.TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_title)],
            handlers.COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_company)],
            handlers.PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_phone)],
            handlers.EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_email)],
            handlers.WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.get_website)]
        },
        fallbacks=[CommandHandler("start", handlers.start)]
    )

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("stats", handlers.admin_stats))
    app.add_handler(CallbackQueryHandler(handlers.menu_routing, pattern="^(menu_|tpl_|go_home)"))
    app.add_handler(conv_handler)

    print("CardForge Core Engine Workers Polling Live...")
    app.run_polling()

if __name__ == '__main__':
    main()

