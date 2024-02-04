from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters

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


async def enroll_command(update, context):
    # Initialize user data in the conversation
    user_data[update.message.chat_id] = {}

    # Ask for the user's name
    await update.message.reply_text("Please enter your name:")
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
        f"Here is a summary of your information:\n\n{summary}\n\nPlease proceed to browsing our available "
        f"oppotunities by clicking /view_opportunities!")

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
        return enroll_command(update, context)

    return ConversationHandler.END


async def feedback(update, context):
    # Provide the Google Form link for feedback
    feedback_link = "https://www.youtube.com/watch?v=vZtm1wuA2yc&t=1138s&ab_channel=Indently"

    # Create an InlineKeyboardButton with the feedback link
    button = InlineKeyboardButton("Provide Feedback", url=feedback_link)

    # Create an InlineKeyboardMarkup with the button
    keyboard = InlineKeyboardMarkup([[button]])

    # Send a message with the feedback link and the button
    await update.message.reply_text(
        "Please provide your feedback using the following link:",
        reply_markup=keyboard
    )


async def cancel(update, context):
    # Clear the user_data and end the conversation
    del user_data[update.message.chat_id]
    await update.message.reply_text("Okay, let's start over.")
    return enroll_command(update, context)

'''
def main():

    # # Create the Telegram Updater and Dispatcher
    # updater = Updater("6703996151:AAEBzfOp95w-uhNE8YDvPJ5NQCZTfc4jAso", use_context=True)
    # dispatcher = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('enroll', enroll_command)],
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

    # Add the start command handler
    #dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('feedback', feedback))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
'''

'''
# Define states
NAME, AGE, GENDER, WORK_STATUS, IMMIGRATION_STATUS, INTERESTS, SKILLS, CONFIRMATION = range(8)

# For storing user data
user_data = {}

# Define the callback data for button handling
GENDER_BUTTONS = ["Male", "Female", "Non-Binary", "Prefer Not to Say"]
WORK_STATUS_BUTTONS = ["Part-Time", "Full-Time", "Student"]
IMMIGRATION_STATUS_BUTTONS = ["Singapore Citizen", "Permanent Resident", "Long-Term Pass Holder"]
INTERESTS_BUTTONS = ["Environment", "Animal Welfare", "Education and Mentoring", "Health and Wellness", "Elderly Care", "International Volunteering"]
SKILLS_BUTTONS = ["Leadership", "Technical and Digital Skills", "Teaching and Mentoring Skills"]


# Enroll Command
async def enroll_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Please enter your name:')
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data['name'] = update.message.text  # Collect the name
    await update.message.reply_text('Please enter your age:')
    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data['age'] = update.message.text  # Collect the age
    # Now that we have the age, proceed to gender selection as in your original flow
    keyboard = [[InlineKeyboardButton(gender, callback_data=gender) for gender in GENDER_BUTTONS]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose your gender:', reply_markup=reply_markup)
    return GENDER


async def gender_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # Save the selected gender in the context user data
    context.user_data['gender'] = query.data

    # Move to the next category (Work Status)
    keyboard = [[InlineKeyboardButton(status, callback_data=status) for status in WORK_STATUS_BUTTONS]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please choose your work status:", reply_markup=reply_markup)
    return WORK_STATUS


async def work_status_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data['work_status'] = query.data

    keyboard = [[InlineKeyboardButton(status, callback_data=status) for status in IMMIGRATION_STATUS_BUTTONS]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please choose your immigration status:", reply_markup=reply_markup)
    return IMMIGRATION_STATUS


async def immigration_status_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # Save the selected work status in the context user data
    context.user_data['work_status'] = query.data

    # Move to the next category (Immigration Status)
    keyboard = [[InlineKeyboardButton(status, callback_data=status) for status in IMMIGRATION_STATUS_BUTTONS]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please choose your immigration status:", reply_markup=reply_markup)
    return IMMIGRATION_STATUS


async def interests_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # Save the selected immigration status in the context user data
    context.user_data['immigration_status'] = query.data

    # Move to the next category (Interests)
    keyboard = [[InlineKeyboardButton(interest, callback_data=interest) for interest in INTERESTS_BUTTONS]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please choose your interest(s):", reply_markup=reply_markup)
    return INTERESTS


async def skills_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # Optionally, handle multiple interests if needed; for now, we assume one interest for simplicity
    context.user_data['interests'] = query.data

    # Move to the next category (Skills)
    keyboard = [[InlineKeyboardButton(skill, callback_data=skill) for skill in SKILLS_BUTTONS]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Please choose your skill(s):", reply_markup=reply_markup)
    return SKILLS


async def confirmation(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # Compile user data for confirmation
    user_data = context.user_data
    confirmation_message = "Please confirm your information:\n" + \
                           "\n".join([f"{key}: {value}" for key, value in user_data.items()])

    keyboard = [
        InlineKeyboardButton("Confirm", callback_data="confirm"),
        InlineKeyboardButton("Cancel", callback_data="cancel")
    ]
    reply_markup = InlineKeyboardMarkup([keyboard])
    await query.edit_message_text(text=confirmation_message, reply_markup=reply_markup)
    return CONFIRMATION


async def save_to_sheet(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == "confirm":
        # Save data to Google Sheets
        sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.volunteer_sheet_name)
        user_data = context.user_data
        # Assuming the sheet has headers: Gender, Work Status, Immigration Status, Interests, Skills
        row = [user_data.get('gender', ''),
               user_data.get('work_status', ''),
               user_data.get('immigration_status', ''),
               user_data.get('interests', ''),
               user_data.get('skills', '')]
        sheet.append_row(row)
        await query.edit_message_text(text="Thank you for enrolling! Your information has been saved.")
    else:
        await query.edit_message_text(text="Enrollment cancelled.")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Enrollment process has been cancelled.')
    return ConversationHandler.END
'''
