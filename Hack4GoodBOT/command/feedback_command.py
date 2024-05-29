from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


async def feedback_command(update, context):
    # Provide the Google Form link for feedback
    feedback_link = "https://forms.gle/547D2dEf32PaJBSE7"

    # Create an InlineKeyboardButton with the feedback link
    button = InlineKeyboardButton("Provide Feedback", url=feedback_link)

    # Create an InlineKeyboardMarkup with the button
    keyboard = InlineKeyboardMarkup([[button]])

    # Send a message with the feedback link and the button
    await update.message.reply_text(
        "Please provide your feedback using the following link:",
        reply_markup=keyboard
    )
