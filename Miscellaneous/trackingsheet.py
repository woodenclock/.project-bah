import os
import gspread
import random
from dotenv import load_dotenv

load_dotenv()

private_key = "-----BEGIN PRIVATE KEY-----{0}-----END PRIVATE KEY-----\n".format(os.environ["PRIVATE_KEY"]).replace("\\n", "\n")

{
    "type": "service_account",
    "project_id": "big-at-heart-bot",
    "private_key_id": "100e8a4a9d2dea6100c95be0f870068b593a2d2d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCVXrwPGqVIc8c/\nSmCLJS6cmdc5dGrgH5OwrX56G5q6mvmDniIvDm8iJt52iLiAS7Oapvdeqx6fvriQ\nl3W3hijBBEahyOPh1KjaAyivfwfx1HUeQlhwTuo196vEW4C4w79f9KxKiPpv5guQ\nvjONveEdLAdYQr2Y/upvt//OpBbKEJJQ7ppRlEubwPuojHuETYt29I/V+dh0sHF7\nCovt7hLwgP+wUGl2KGvHe9Qo7qnV7NTY7Yp5zchvqfRCK+fc5ZSnABqokCTuEB2L\nw3pwSkSan6bBNfb0YQKkaZh8/2hxXyRuBHKefnIyHX/s8XVf4b/ChDu5w67ay+PD\ny3hvCAMTAgMBAAECggEAA93BimE12VaTLV00ezA0MP4pEaX6GjZXBqIG/bbMiNCi\nwrhgyXewgrbKLVFD9/YoU57Hal44MF7/Efxe91LJUphUvQf2dg2gwpEwXWfcAcjD\nsKEmVDSGtWzlYki9X+BD34JKxLHKTFktACBxidVaB/zwF7sVLepIkSm3ElcxoSXw\niEx8EVgSNMkyCMRg/sd8fbwm24oi843o31zVrT5Xp/kqfv3qD3KkloTSa9N8UUDI\ndH0odl+qqo/tJYIM6mHhNOhh2rz/Z6zV86bhgJen7qf3KjtG5wapra16HvKFIq+O\nAxq/nlkPfPJxavXFjtCsBVwuOjbTQ0hc0BBy0owXgQKBgQDJYT10llsnu1uOPXFJ\nKGLJKgRj4zZyBRuESQCdZYa1Cyk7TckVpQffHQOYs1qL1d4QJQrX2+2jODT/MGBk\nnQXvUmLyi4tG1Vqv8jFR0jNh9TLMnxMC+IaH0sS5txkccPg0749hPbohuOxdTrhf\nN3HhDqlTQu50LTdna89xzdCzUwKBgQC94jUxIEOe/lEuixaBAvTHctIzimHV9Rxu\n1u5b4hgNNcGjQrl5I3hgOPiRe6ES+P/4+niP+io87QRra8KYXMeC52oVSABebC2P\nu8DEimV7hmcYFC+PLZHVkTsPTaAPJvtuD7kFVzUFd9gXY72PmvIiGxmZegtitEbZ\n8keM1885QQKBgHwXL4doH0OccA52ThiGiljrS0lB+YrJGuupEHfs19U3y3B/vilY\nSEFz34N5AZKpduz75nKdUxIA0KdvZ/aXy9BtNAvBcVF0py1EUJ/ap071iRgN7ekm\nu792YUMPUKn18vyroe6J2uhsyzm0CGikAchtAGoOFGICeuF/zZSS/seBAoGAZMLa\nCSSe3YsE11b1bSZ9cC0tAC6pthjoqqShPd7fdnsVMyZgN7kr0pvIw6LAGcpKQvve\n6EAPE9+OXdaEH8f0EzHr6DkaAQEUuFYgd+sc6QysPmnPxwGehp8XoQpHKmM8Pu5W\n90+MkkdDQz4pREArxw9saTYLPqh9hH/9me6XR0ECgYEAnzhgZU71JwSKTzXTrCzL\nMAPV/7v91a1OKfG3O+LcM1WJfTGZpPdkWJJFKNcaH6Psq49KVrLKd3u5/tAblMrp\nsdwte/rlLPKrRGg3sEX0V04DfKlKMLuLszlEMTm5Z7LunMtbDkM7eZ/AYmL0fJ1n\njTiQYqHZSaInvpjFFBQKvOM=\n-----END PRIVATE KEY-----\n",
    "client_email": "big-at-heart@big-at-heart-bot.iam.gserviceaccount.com",
    "client_id": "106729815751320042081",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/big-at-heart%40big-at-heart-bot.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }
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