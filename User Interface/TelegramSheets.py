# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 17:56:17 2021

@author: tehre
"""

import os
import gspread
import random
from dotenv import load_dotenv

load_dotenv()

private_key = "-----BEGIN PRIVATE KEY-----{0}-----END PRIVATE KEY-----\n".format(os.environ["PRIVATE_KEY"]).replace("\\n", "\n")

credentials = {
  "type": "service_account",
  "project_id": os.environ["PROJECT_ID"],
  "private_key_id": os.environ["PRIVATE_KEY_ID"],
  "private_key": private_key,
  "client_email": os.environ["CLIENT_EMAIL"],
  "client_id": os.environ["CLIENT_ID"],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ["CERT_URL"]
}

gc = gspread.service_account_from_dict(credentials)

sh = gc.open_by_url(os.environ["SPREADSHEET_URL"])

"""
START OF GETTING SHEET VALUES
"""
worksheet = sh.sheet1
all_values = worksheet.get_all_values() #returns a list of lists 

event_details = sh.worksheet("Event Details")
event_details_links = event_details.get_all_values()
"""
END OF GETTING SHEET VALUES
"""

def get_list():
    return all_values

def get_sheet():
    return worksheet()

def get_event_details_links():
    return event_details_links[1:]

def get_ccas_by_category(category):
    working_list = all_values
    
    return_list = []
    
    for items in working_list:
        if items[0] == category:
            return_list.append(items)
    
    return return_list

def get_ccas_by_zone(zone):
    working_list = all_values
    
    return_list = []
    
    for items in working_list:
        if items[7] == zone:
            return_list.append(items)
    
    return return_list

def get_random_cca():
    working_list = all_values
    
    k = random.randint(1,len(working_list)-1)
    
    return working_list[k]