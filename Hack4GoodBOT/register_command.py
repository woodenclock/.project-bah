import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes,
                          CallbackContext, CallbackQueryHandler)


# Register Command
async def register_command(update: Update, context: CallbackContext) -> None:
    # Access the sheet with volunteering opportunities
    events_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.opportunities_sheet_name)
    events = events_sheet.get_all_records()

    # Create a list of InlineKeyboardButtons for each event
    buttons = [
        InlineKeyboardButton(text=event['Event'], callback_data=f"register_{event['Event']}")
        for event in events
    ]

    # Organize buttons into a keyboard layout
    keyboard = [buttons[i:i + 1] for i in range(0, len(buttons), 1)]  # one button per row
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with inline buttons
    await update.message.reply_text('Please choose an event to register:', reply_markup=reply_markup)


async def button_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Extract event name from the callback data
    event_name = query.data.split('_')[1]

    # Store the chosen event name in the user's context for later use
    context.user_data['chosen_event'] = event_name

    user_id = query.from_user.id

    # Access the 'Registrations' sheet
    registrations_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.register_sheet_name)
    registrations = registrations_sheet.get_all_records()

    # Check if the user has already registered for the event
    already_registered = any(
        reg['Event'] == event_name and str(reg['User ID']) == str(user_id) for reg in registrations)

    if already_registered:
        # Inform the user that they are already registered
        await query.edit_message_text(text=f"You have already registered: {event_name}. "
                                           f"We appreciate your enthusiasm! 🤩"
                                           f"Thank you!")
    else:
        # Ask for registration confirmation
        keyboard = [
            InlineKeyboardButton(text="Yes", callback_data="confirm_registration"),
            InlineKeyboardButton(text="No", callback_data="cancel_registration")
        ]
        reply_markup = InlineKeyboardMarkup([keyboard])
        await query.edit_message_text(text=f"Confirm registration for {event_name}?", reply_markup=reply_markup)


async def confirmation_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if 'confirm_registration' in query.data:
        # Retrieve the chosen event name from the user's context
        event_name = context.user_data.get('chosen_event')
        events_sheet = config.client.open_by_key(config.SHEET_ID).worksheet('Opportunities')
        events = events_sheet.get_all_records()

        # Find the event details by the event name
        event_details = next((event for event in events if event['Event'] == event_name), None)
        if event_details:
            registration_url = event_details['Register']
            date_of_event = event_details['Date']
            user_id = query.from_user.id
            username = query.from_user.username  # Get the user's Telegram username

            # Access the 'Registrations' sheet
            registrations_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.register_sheet_name)

            # Append the new registration
            # Include the username along with the other details
            registrations_sheet.append_row([event_name, date_of_event, user_id, username])

            # Provide the link to the Google Form for additional details
            await query.edit_message_text(text=f"You have been registered for {event_name}. "
                                               f"Please fill in the following form: {registration_url}")
        else:
            await query.edit_message_text(text="There was an error processing your registration. Please try again.")

    elif 'cancel_registration' in query.data:
        # User pressed "No", so we display the list of opportunities again
        await query.edit_message_reply_markup(reply_markup=await register_command(query, context))