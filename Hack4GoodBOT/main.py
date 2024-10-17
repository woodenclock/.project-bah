from Hack4GoodBOT import response
from Hack4GoodBOT.config import config
from command import (start_command, help_command, browse_command, enroll_command, attended_command,
                     register_command, upcoming_command, feedback_command, certificate_command)
from telegram import Update
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackQueryHandler)


# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Main
def main() -> None:
    # Set up the bot
    print('Starting Hack4GoodBOT...')
    app = Application.builder().token(config.TOKEN).build()

    # Define the conversation handler
    enroll_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('enroll', enroll_command.start_enroll)],
        states={
            enroll_command.NAME: [MessageHandler(filters.TEXT, enroll_command.ask_name)],
            enroll_command.AGE: [MessageHandler(filters.TEXT, enroll_command.ask_age)],
            enroll_command.GENDER: [CallbackQueryHandler(enroll_command.ask_gender)],
            enroll_command.WORK_STATUS: [CallbackQueryHandler(enroll_command.ask_work_status)],
            enroll_command.IMMIGRATION_STATUS: [CallbackQueryHandler(enroll_command.ask_immigration_status)],
            enroll_command.INTERESTS: [CallbackQueryHandler(enroll_command.ask_interests)],
            enroll_command.SKILLS: [CallbackQueryHandler(enroll_command.ask_skills)],
            enroll_command.SUMMARY: [CallbackQueryHandler(enroll_command.ask_summary)],
            enroll_command.CONFIRMATION: [CallbackQueryHandler(enroll_command.handle_confirmation,
                                                               pattern='^confirm_(yes|no)$')]
        },
        fallbacks=[CommandHandler('cancel', enroll_command.cancel)]
    )

    # Add the conversation handler to the dispatcher
    app.add_handler(enroll_conv_handler)

    reg_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register_command.register_command)],
        states={
            register_command.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_command.validate_name)],
            register_command.REGISTER: [MessageHandler(filters.TEXT & ~filters.COMMAND,
                                                       register_command.register_command)],
            # Example placeholder
        },
        fallbacks=[CommandHandler('cancel', register_command.cancel)],
    )
    app.add_handler(reg_conv_handler)

    # Callback query handler for buttons
    app.add_handler(CallbackQueryHandler(register_command.button_callback_handler, pattern='^register_'))
    app.add_handler(
        CallbackQueryHandler(register_command.confirmation_callback_handler, pattern='^(confirm_registration'
                                                                                     '|cancel_registration)$'))

    # Commands
    app.add_handler(CommandHandler("start", start_command.start_command))
    app.add_handler(CommandHandler("help", help_command.help_command))
    app.add_handler(CommandHandler("browse", browse_command.browse_command))
    app.add_handler(CommandHandler("register", register_command.register_command))
    app.add_handler(CommandHandler("attended", attended_command.attended_command))
    app.add_handler(CommandHandler("upcoming", upcoming_command.upcoming_command))
    app.add_handler(CommandHandler("feedback", feedback_command.feedback_command))
    app.add_handler(CommandHandler('certificate', certificate_command.certificate_command))
    app.add_handler(CallbackQueryHandler(certificate_command.certificate_button_handler, pattern='^cert_'))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, response.handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    # print('Polling...')
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()
