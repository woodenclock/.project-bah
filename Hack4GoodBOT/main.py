import Miscellaneous.response
from Hack4GoodBOT.config import config
from Hack4GoodBOT.command import (help_command, browse_command, attended_command, register_command,
                                  upcoming_command, feedback_command)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackQueryHandler)

# Define the conversation states
NAME, AGE, GENDER, WORK_STATUS, IMMIGRATION_STATUS, INTERESTS, SKILLS, SUMMARY = range(8)

# Define the callback data for button handling
GENDER_BUTTONS = ["Male", "Female", "Non-Binary", "Prefer Not to Say"]
WORK_STATUS_BUTTONS = ["Part-Time", "Full-Time", "Student"]
IMMIGRATION_STATUS_BUTTONS = ["Singapore Citizen", "Permanent Resident", "Long-Term Pass Holder"]
INTERESTS_BUTTONS = ["Environment", "Animal Welfare", "Education and Mentoring", "Health and Wellness", "Elderly Care",
                     "International Volunteering"]
SKILLS_BUTTONS = ["Leadership", "Technical and Digital Skills", "Teaching and Mentoring Skills"]

# Define the dictionary to store user information
user_data = {}


async def start_enroll(update, context):
    # Initialize user data in the conversation
    user_data[update.message.chat_id] = {}

    # Ask for the user's name
    await update.message.reply_text("Input \"/cancel\" to cancel your enrollment.\nPlease enter your name:")
    return NAME


async def ask_name(update, context):
    # Store the user's name in the user_data dictionary
    user_data[update.message.chat_id]['name'] = update.message.text

    # Ask for age
    await update.message.reply_text("Please enter your age:")
    return AGE


async def ask_gender(update, context):
    # Store the age in user_data
    user_data[update.effective_chat.id]['age'] = update.message.text

    # Show gender options as buttons
    keyboard = [
        [InlineKeyboardButton("Male", callback_data='Male')],
        [InlineKeyboardButton("Female", callback_data='Female')],
        [InlineKeyboardButton("Non-Binary", callback_data='Non-Binary')],
        [InlineKeyboardButton("Prefer Not to Say", callback_data='Prefer Not to Say')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for gender
    await update.message.reply_text("Please choose your gender:", reply_markup=reply_markup)
    return GENDER


async def ask_work_status(update, context):
    # Store the gender in user_data
    user_data[update.callback_query.message.chat_id]['gender'] = update.callback_query.data

    # Show work status options as buttons
    keyboard = [
        [InlineKeyboardButton("Part-Time", callback_data='Part-Time')],
        [InlineKeyboardButton("Full-Time", callback_data='Full-Time')],
        [InlineKeyboardButton("Student", callback_data='Student')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for work status
    await update.callback_query.message.reply_text("Please choose your work status:", reply_markup=reply_markup)
    return WORK_STATUS


async def ask_immigration_status(update, context):
    # Store the work status in user_data
    user_data[update.callback_query.message.chat_id]['work_status'] = update.callback_query.data

    # Show immigration status options as buttons
    keyboard = [
        [InlineKeyboardButton("Singapore Citizen", callback_data='Singapore Citizen')],
        [InlineKeyboardButton("Permanent Resident", callback_data='Permanent Resident')],
        [InlineKeyboardButton("Long-Term Pass Holder", callback_data='Long-Term Pass Holder')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for immigration status
    await update.callback_query.message.reply_text("Please choose your immigration status:", reply_markup=reply_markup)
    return IMMIGRATION_STATUS


async def ask_interests(update, context):
    # Store the immigration status in user_data
    user_data[update.callback_query.message.chat_id]['immigration_status'] = update.callback_query.data

    # Show interests options as buttons
    keyboard = [
        [InlineKeyboardButton("Environment", callback_data='Environment')],
        [InlineKeyboardButton("Animal Welfare", callback_data='Animal Welfare')],
        [InlineKeyboardButton("Education and Mentoring", callback_data='Education and Mentoring')],
        [InlineKeyboardButton("Health and Wellness", callback_data='Health and Wellness')],
        [InlineKeyboardButton("Elderly Care", callback_data='Elderly Care')],
        [InlineKeyboardButton("International Volunteering", callback_data='International Volunteering')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for interests
    await update.callback_query.message.reply_text("Please choose your interests:", reply_markup=reply_markup)
    return INTERESTS


async def ask_skills(update, context):
    # Store the interests in user_data
    user_data[update.callback_query.message.chat_id]['interests'] = update.callback_query.data

    # Show skills options as buttons
    keyboard = [
        [InlineKeyboardButton("Leadership", callback_data='Leadership')],
        [InlineKeyboardButton("Technical and Digital Skills", callback_data='Technical and Digital Skills')],
        [InlineKeyboardButton("Teaching and Mentoring Skills", callback_data='Teaching and Mentoring Skills')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for skills
    await update.callback_query.message.reply_text("Please choose your skills:", reply_markup=reply_markup)
    return SKILLS


async def ask_summary(update, context):
    # Store the skills in user_data
    user_data[update.callback_query.message.chat_id]['skills'] = update.callback_query.data

    # Generate the summary
    summary = f"Name: {user_data[update.callback_query.message.chat_id]['name']}\n" \
              f"Age: {user_data[update.callback_query.message.chat_id]['age']}\n" \
              f"Gender: {user_data[update.callback_query.message.chat_id]['gender']}\n" \
              f"Work Status: {user_data[update.callback_query.message.chat_id]['work_status']}\n" \
              f"Immigration Status: {user_data[update.callback_query.message.chat_id]['immigration_status']}\n" \
              f"Interests: {user_data[update.callback_query.message.chat_id]['interests']}\n" \
              f"Skills: {user_data[update.callback_query.message.chat_id]['skills']}"

    # Store the summary in user_data
    user_data[update.callback_query.message.chat_id]['summary'] = summary

    # Display the summary to the user
    await update.callback_query.message.reply_text(
        f"Here is a summary of your information:\n\n{summary}\n\nPlease proceed to browsing our available oppotunities by clicking /browse!")

    return SUMMARY


async def confirm_summary(update, context):
    # Get the user's response
    response = update.callback_query.data

    if response == "Yes":
        # Information is correct, enrollment is complete
        await update.callback_query.message.reply_text("Thank you for enrolling. Your enrollment is complete!")

        # Clear the user_data
        del user_data[update.callback_query.message.chat_id]

    else:
        # Information is incorrect, restart the enrollment process
        await update.callback_query.message.reply_text("Okay, let's start over.")
        return start_enroll(update, context)

    return ConversationHandler.END


async def cancel(update, context):
    # Clear the user_data and end the conversation
    del user_data[update.message.chat_id]
    await update.message.reply_text("Okay, let's start over.")
    return start_enroll(update, context)


# Start Command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi there, I am Hack4GoodBOT!\nType /help to see available commands.")


# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Main
def main() -> None:
    # Set up the bot
    print('Starting Hack4GoodBOT...')
    app = Application.builder().token(config.TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command.help_command))
    app.add_handler(CommandHandler("browse", browse_command.browse_command))
    app.add_handler(CommandHandler("register", register_command.register_command))
    app.add_handler(CommandHandler("attended", attended_command.attended_command))
    app.add_handler(CommandHandler("upcoming", upcoming_command.upcoming_command))
    app.add_handler(CommandHandler("feedback", feedback_command.feedback_command))

    # Callback query handler for buttons
    app.add_handler(CallbackQueryHandler(register_command.button_callback_handler, pattern='^register_'))
    app.add_handler(
        CallbackQueryHandler(register_command.confirmation_callback_handler, pattern='^(confirm_registration'
                                                                                     '|cancel_registration)$'))

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('enroll', start_enroll)],
        states={
            NAME: [MessageHandler(filters.TEXT, ask_name)],
            AGE: [MessageHandler(filters.TEXT, ask_gender)],
            GENDER: [CallbackQueryHandler(ask_work_status)],
            WORK_STATUS: [CallbackQueryHandler(ask_immigration_status)],
            IMMIGRATION_STATUS: [CallbackQueryHandler(ask_interests)],
            INTERESTS: [CallbackQueryHandler(ask_skills)],
            SKILLS: [CallbackQueryHandler(ask_summary)],
            SUMMARY: [CallbackQueryHandler(confirm_summary)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add the conversation handler to the dispatcher
    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Miscellaneous.response.handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()
