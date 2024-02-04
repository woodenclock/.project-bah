from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackContext, CallbackQueryHandler)

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
