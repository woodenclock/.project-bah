from typing import Final
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

TOKEN: Final = "6703996151:AAEBzfOp95w-uhNE8YDvPJ5NQCZTfc4jAso"
BOT_USERNAME: Final = "@bahh4g_bot"


# Dictionary to store user data temporarily
user_data = {}

# States for the conversation handler
ASK_AGE, ASK_GENDER, ASK_WORK_STATUS, ASK_IMMIGRATION_STATUS, ASK_INTERESTS, ASK_SKILLS, ASK_OTHER_SKILLS = range(7)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    context.user_data[user_id] = {}

    update.message.reply_text(
        f"Hello {update.message.from_user.first_name}! Welcome to the volunteer registration process.\n\n"
        "To enroll as a volunteer, use the /enroll command."
    )

    # Display available commands
    command_list(update, context)

    # Initiate the enrollment process
    return enroll(update, context)

# Function to handle the /enroll command
def enroll(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Check if the user has already started the enrollment process
    if user_id not in context.user_data or not context.user_data[user_id]:
        context.user_data[user_id] = {}

        update.message.reply_text("Welcome to the volunteer registration process!\n\nPlease enter your age:")
        return ASK_AGE
    else:
        update.message.reply_text("You are already enrolled. If you want to start over, use the /enroll command.")
        return ConversationHandler.END

# Function to handle age input
def ask_age(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    age = update.message.text
    user_data[user_id]["age"] = age

    update.message.reply_text(
        "Choose your gender:",
        reply_markup=ReplyKeyboardMarkup([["Male", "Female"], ["Non-Binary", "Prefer not to say"]], one_time_keyboard=True),
    )
    return ASK_GENDER

# Function to handle gender input
def ask_gender(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    gender = update.message.text
    user_data[user_id]["gender"] = gender

    update.message.reply_text(
        "Choose your work status:",
        reply_markup=ReplyKeyboardMarkup([["Part-Time", "Full-Time"], ["Student"]], one_time_keyboard=True),
    )
    return ASK_WORK_STATUS

# Function to handle work status input
def ask_work_status(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    work_status = update.message.text
    user_data[user_id]["work_status"] = work_status

    # Ask for immigration status
    keyboard = [
        ["Singapore Citizen", "Permanent Resident"],
        ["Long-Term Pass Holder", "Next"],
    ]
    update.message.reply_text(
        "Choose your immigration status:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return ASK_IMMIGRATION_STATUS

# Function to handle immigration status input
def ask_immigration_status(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    immigration_status = update.message.text
    user_data[user_id]["immigration_status"] = immigration_status

    # Ask for interests
    keyboard = [
        ["Environment", "Animal Welfare"],
        ["Education and Mentoring", "Health and Wellness"],
        ["Elderly Care", "International Volunteering"],
        ["Other", "Next"]
    ]
    update.message.reply_text(
        "Choose your interests (you can select multiple):",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return ASK_INTERESTS

# Function to handle interests input
def ask_interests(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    interests = update.message.text

    if interests == "Next":
        # Ask for skills
        keyboard = [
            ["Leadership", "Technical and Digital Skills"],
            ["Teaching and Mentoring Skills", "Other"],
        ]
        update.message.reply_text(
            "Choose your skills (you can select multiple):",
            reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
        )
        return ASK_SKILLS
    else:
        if "interests" not in user_data[user_id]:
            user_data[user_id]["interests"] = []
        user_data[user_id]["interests"].append(interests)
        return ASK_INTERESTS

# Function to handle skills input
def ask_skills(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    skills = update.message.text

    if skills == "Other":
        update.message.reply_text("Type in your other skills:")
        return ASK_OTHER_SKILLS
    else:
        if "skills" not in user_data[user_id]:
            user_data[user_id]["skills"] = []
        user_data[user_id]["skills"].append(skills)
        return ASK_SKILLS

# Function to handle other skills input
def ask_other_skills(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    other_skills = update.message.text

    if "skills" not in user_data[user_id]:
        user_data[user_id]["skills"] = []
    user_data[user_id]["skills"].append(other_skills)

    # Finish enrollment
    return finish_enrollment(update, context)

# Function to handle finishing enrollment
def finish_enrollment(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Print user data (replace this with your desired action)
    print(f"User ID: {user_id}")
    print("User Data:")
    print(user_data[user_id])

    update.message.reply_text("Thank you for enrolling! Your information has been recorded.")
    user_data.pop(user_id)  # Remove user data after enrollment is complete
    return ConversationHandler.END

# Function to display the list of commands
def command_list(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Available Commands:\n/enroll - Start the volunteer enrollment process\n/help - Show this command list")

# Define the main function
def main() -> None:
    # Set up the Telegram Bot
    updater = Updater("6703996151:AAEBzfOp95w-uhNE8YDvPJ5NQCZTfc4jAso")
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("enroll", enroll))
    dp.add_handler(CommandHandler("help", command_list))

    # Register conversation handler with entry points and states
    enrollment_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("enroll", enroll)],
        states={
            ASK_AGE: [MessageHandler(Filters.text & ~Filters.command, ask_age)],
            ASK_GENDER: [MessageHandler(Filters.text & ~Filters.command, ask_gender)],
            ASK_WORK_STATUS: [MessageHandler(Filters.text & ~Filters.command, ask_work_status)],
            ASK_IMMIGRATION_STATUS: [MessageHandler(Filters.text & ~Filters.command, ask_immigration_status)],
            ASK_INTERESTS: [MessageHandler(Filters.text & ~Filters.command, ask_interests)],
            ASK_SKILLS: [MessageHandler(Filters.text & ~Filters.command, ask_skills)],
            ASK_OTHER_SKILLS: [MessageHandler(Filters.text & ~Filters.command, ask_other_skills)],
        },
        fallbacks=[],
    )
    dp.add_handler(enrollment_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == "__main__":
    main()
