import sys
import os

# Append the directory of the parent folder to sys.path
# so Python knows where to find the 'config' module.
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
parent_dir = os.path.dirname(script_dir)  # Parent directory
sys.path.append(parent_dir)

from config import config
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler


# Define the conversation states
NAME, AGE, GENDER, WORK_STATUS, IMMIGRATION_STATUS, INTERESTS, SKILLS, SUMMARY, CONFIRMATION= range(9)


# Define the callback data for button handling
GENDER_BUTTONS = ["Male", "Female", "Non-Binary", "Prefer Not to Say"]
WORK_STATUS_BUTTONS = ["Part-Time", "Full-Time", "Student"]
IMMIGRATION_STATUS_BUTTONS = ["Singapore Citizen", "Permanent Resident", "Long-Term Pass Holder"]
INTERESTS_BUTTONS = ["Environment", "Animal Welfare", "Education and Mentoring", "Health and Wellness", "Elderly Care",
                     "International Volunteering"]
SKILLS_BUTTONS = ["Leadership", "Technical and Digital Skills", "Teaching and Mentoring Skills"]


# Define the dictionary to store user information
user_data = {}


# Helper function to prompt for valid input
async def reject_invalid(update, context, prompt_message):
    await update.message.reply_text("Please enter a valid input!")
    await update.message.reply_text(prompt_message)


async def start_enroll(update, context):
    chat_id = update.message.chat_id
    if check_enrollment(chat_id):
        await update.message.reply_text("Our records show that you have already enrolled. "
                                        "If you need to update your details, please contact support.")
        return ConversationHandler.END
    else:
        user_data[chat_id] = {
            'telegram_user_id': chat_id,
            'telegram_username': update.message.from_user.username,
        }
        await update.message.reply_text("Let's get you enrolled into the Big At Hearts family! 🤩\n"
                                        "Please enter your full name:")
        return NAME


async def ask_name(update, context):
    name = update.message.text.strip()
    # Check if the name is valid (only alphabets and not starting with a "/")
    if all(x.isalpha() or x.isspace() for x in name) and not name.startswith('/'):
        # Store the valid name in the user_data dictionary
        user_data[update.message.chat_id]['name'] = name
        # Ask for age
        await update.message.reply_text(f"Hi {name} 🖐️\n"
                                        f"Nice to meet you!\n"
                                        f"Please enter your age:")
        return AGE
    else:
        # Reject invalid name input
        await reject_invalid(update, context, "Please enter your name:")
        return NAME


async def ask_age(update, context):
    age = update.message.text
    # Check if the age is valid (only numbers)
    if age.isdigit() and 1 <= int(age) <= 100 and not age.startswith('/'):
        # Store the valid age in the user_data dictionary
        user_data[update.effective_chat.id]['age'] = int(age)

        # Proceed to ask for gender
        return await ask_gender(update, context)
    else:
        # Reject invalid age input
        await reject_invalid(update, context, "Please enter your age:")
        return AGE


async def ask_gender(update, context):
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
    return WORK_STATUS


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
    await update.callback_query.message.edit_text("Please choose your work status:", reply_markup=reply_markup)

    # Store the work status in user_data
    user_data[update.callback_query.message.chat_id]['work_status'] = update.callback_query.data
    return IMMIGRATION_STATUS


async def ask_immigration_status(update, context):
    # Show immigration status options as buttons
    keyboard = [
        [InlineKeyboardButton("Singapore Citizen", callback_data='Singapore Citizen')],
        [InlineKeyboardButton("Permanent Resident", callback_data='Permanent Resident')],
        [InlineKeyboardButton("Long-Term Pass Holder", callback_data='Long-Term Pass Holder')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ask for immigration status
    await update.callback_query.message.edit_text("Please choose your immigration status:", reply_markup=reply_markup)
    return INTERESTS


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
    await update.callback_query.message.edit_text("Please choose your interests:", reply_markup=reply_markup)
    return SKILLS


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
    await update.callback_query.message.edit_text("Please choose your skills:", reply_markup=reply_markup)
    return SUMMARY


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
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data='confirm_yes')],
        [InlineKeyboardButton("No", callback_data='confirm_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text(
        f"Here is a summary of your information:\n\n{summary}\n\nConfirm your choices?",
        reply_markup=reply_markup
    )

    return CONFIRMATION


def check_enrollment(telegram_user_id):
    credentials = Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE, scopes=config.scope)
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet_id = config.SHEET_ID
    range_name = 'Volunteers!A2:E'  # Adjust the range based on where the telegram_user_id is stored

    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        for row in values:
            # Assuming the telegram_user_id is in the first column
            if str(telegram_user_id) == row[0]:
                return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


async def handle_confirmation(update, context):
    query = update.callback_query
    query.answer()  # Important to provide feedback to the user that their click was received

    if query.data == 'confirm_yes':
        # Save the data to Google Sheets
        save_to_google_sheets(user_data[query.message.chat_id])
        await query.edit_message_text("Thank you for enrolling.\n"
                                      "You are now a member of the Big At Hearts family! 👨‍👩‍👧‍👦")
        # Clear the user_data
        del user_data[query.message.chat_id]

    elif query.data == 'confirm_no':
        await query.edit_message_text("Okay, let's start over.")
        # Optionally, clear the user_data or restart the process
        del user_data[query.message.chat_id]

    return ConversationHandler.END


def save_to_google_sheets(data):
    credentials = Credentials.from_service_account_file(
        config.SERVICE_ACCOUNT_FILE, scopes=config.scope)

    service = build('sheets', 'v4', credentials=credentials)

    spreadsheet_id = config.SHEET_ID
    range_name = 'Volunteers!A2'  # Adjust based on your needs
    values = [[
        data['name'],
        data['telegram_user_id'],
        data['telegram_username'],
        data['age'],
        data['gender'],
        data['work_status'],
        data['immigration_status'],
        data['interests'],
        data['skills']
    ]]

    body = {'values': values}

    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    except Exception as e:
        print(f"An error occurred: {e}")


async def cancel(update, context):
    chat_id = update.message.chat_id
    # Check if the user_data exists before trying to delete it
    if chat_id in user_data:
        del user_data[chat_id]
        await update.message.reply_text("Your enrollment has been canceled.")
    else:
        await update.message.reply_text("You have not started enrollment.")

    # Depending on your state management, you may need to end the conversation
    return ConversationHandler.END

