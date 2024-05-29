from telegram import Update
from telegram.ext import (ContextTypes)


# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/enroll - Enroll as a new volunteer\n"
        "/browse - Browse volunteering events\n"
        "/register - Check events  I have signed up\n"
        "/attended - Check attended events\n"
        "/upcoming - Check upcoming events\n"
        "/feedback - Submit feedback/blog/reflection\n"
        "/certificate - Request a certificate for attended events"
    )
