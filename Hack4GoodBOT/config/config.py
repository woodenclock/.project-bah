import logging
import gspread
import os
from typing import Final
from oauth2client.service_account import ServiceAccountCredentials

# Initialization
TOKEN: Final = "6915448696:AAGa692f2FuuPsMzjhyw5b-Lllnc00g5f3M"
BOT_USERNAME: Final = "@Hack4GoodBOT"

# Google Sheets information
SHEET_ID: Final = "1dQOfj3kamyPNE5X0mO7YVlKtCP4awO_XX7B4Vhf9sZc"
opportunities_sheet_name = 'Opportunities'
register_sheet_name = 'Registrations'
volunteer_sheet_name = 'Volunteers'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get current working directory
current_working_directory = os.getcwd()

# Load credentials for Google Sheets
SERVICE_ACCOUNT_FILE = os.path.join(current_working_directory, 'Hack4GoodBOT', 'config', 'credentials.json')
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(creds)

# Certificate Generation
base_dir = os.path.join(current_working_directory, 'Hack4GoodBOT', 'certificate')
template_path = os.path.join(base_dir, 'certificate_template.png')
font_path = os.path.join(base_dir, 'times.ttf')
name_position = (1000, 707)
output_path = os.path.join(base_dir, 'personalized_certificate.png')
