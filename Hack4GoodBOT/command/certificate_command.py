from datetime import datetime
from Hack4GoodBOT.config import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from PIL import Image, ImageDraw, ImageFont


async def certificate_command(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    registrations_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.register_sheet_name)
    registrations = registrations_sheet.get_all_records()

    # await update.message.reply_text(f"Raw data: {registrations}")

    # Filter out past events with attendance marked as "1"
    past_events = [reg for reg in registrations if str(reg['User ID']) == str(user_id)
                   and datetime.strptime(reg['Date'], "%d/%m/%Y") < datetime.now()
                   and reg.get('Attendance') == 1]  # Adjusted to check for integer 1

    if not past_events:
        await update.message.reply_text("You have no past events with attendance marked.")
        return

    # If only one past event is found, generate the certificate directly
    if len(past_events) == 1:
        event = past_events[0]
        create_certificate(event['Name'], event['Date'], event['Event'])
        await send_certificate(update, context, config.output_path)
        return

    # If multiple events are found, show buttons for each event
    buttons = [InlineKeyboardButton(text=event['Event'], callback_data=f"cert_{event['Event']}")
               for event in past_events]
    keyboard = [buttons[i:i + 1] for i in range(0, len(buttons), 1)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose an event to generate a certificate for:',
                                    reply_markup=reply_markup)
    return


async def certificate_button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    event_name = '_'.join(query.data.split('_')[1:])  # Adjusted for event names with underscores
    registrations_sheet = config.client.open_by_key(config.SHEET_ID).worksheet(config.register_sheet_name)
    registrations = registrations_sheet.get_all_records()
    event = next((reg for reg in registrations if reg['Event'] == event_name and str(reg['Attendance']) == '1'), None)

    if event:
        create_certificate(event['Name'], event['Date'], event['Event'])
        await send_certificate(query, context, config.output_path)  # Pass the query object
    else:
        # More specific error message for debugging
        await query.message.reply_text(
            f"Error: No event found for {event_name} or attendance issue. Please check your data and try again.")


def create_certificate(name, date, course):
    # Load the certificate template
    image = Image.open(config.template_path)
    draw = ImageDraw.Draw(image)

    # Load the font
    name_font = ImageFont.truetype(config.font_path, 150)
    # Add name text
    name_text_width = draw.textlength(name, font=name_font)

    # Calculate the position
    x = config.name_position[0] - name_text_width / 2
    y = config.name_position[1] - 80
    draw.text((x, y), name, font=name_font, align="center", fill="black")

    # Add date text
    date_font = ImageFont.truetype(config.font_path, 40)
    date_text_width = draw.textlength(date, font=date_font)
    draw.text((550 - date_text_width / 2, 1010), date, font=date_font, align="center", fill="black")

    # Add course name text
    course_font = ImageFont.truetype(config.font_path, 30)
    course_text_width = draw.textlength(course, font=course_font)
    draw.text((1000 - course_text_width / 2, 915), course, font=course_font, align="center", fill="black")

    # Save the modified image
    image.save(config.output_path)


# Example usage
# name = "Katelyn Choo Choo"
# date = "21 September 2023"
# course = "Digital Literacy Trainer 1"
#
# create_certificate(name, date, course)


async def send_certificate(update_or_query, context: CallbackContext, certificate_path: str) -> None:
    # Determine if this is a message update or a callback query and get the chat_id accordingly
    if hasattr(update_or_query, 'effective_chat'):
        chat_id = update_or_query.effective_chat.id  # For message updates
    elif hasattr(update_or_query, 'message'):
        chat_id = update_or_query.message.chat.id  # For callback queries
    else:
        # Log error or send a reply indicating the failure to determine chat context
        print("Cannot determine chat context.")
        return

    with open(certificate_path, 'rb') as certificate:
        await context.bot.send_photo(chat_id=chat_id, photo=certificate)
