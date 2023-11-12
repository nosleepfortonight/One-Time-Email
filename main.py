import requests, tkinter.messagebox, colorama

colorama.init()

print(f"""{colorama.Fore.RED}
 ▒█████   ███▄    █ ▓█████    ▄▄▄█████▓ ██▓ ███▄ ▄███▓▓█████    ▓█████  ███▄ ▄███▓ ▄▄▄       ██▓ ██▓    
▒██▒  ██▒ ██ ▀█   █ ▓█   ▀    ▓  ██▒ ▓▒▓██▒▓██▒▀█▀ ██▒▓█   ▀    ▓█   ▀ ▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    
▒██░  ██▒▓██  ▀█ ██▒▒███      ▒ ▓██░ ▒░▒██▒▓██    ▓██░▒███      ▒███   ▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    
▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄    ░ ▓██▓ ░ ░██░▒██    ▒██ ▒▓█  ▄    ▒▓█  ▄ ▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    
░ ████▓▒░▒██░   ▓██░░▒████▒     ▒██▒ ░ ░██░▒██▒   ░██▒░▒████▒   ░▒████▒▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒
░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░     ▒ ░░   ░▓  ░ ▒░   ░  ░░░ ▒░ ░   ░░ ▒░ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░
  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░       ░     ▒ ░░  ░      ░ ░ ░  ░    ░ ░  ░░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░
░ ░ ░ ▒     ░   ░ ░    ░        ░       ▒ ░░      ░      ░         ░   ░      ░     ░   ▒    ▒ ░  ░ ░   
    ░ ░           ░    ░  ░             ░         ░      ░  ░      ░  ░       ░         ░  ░ ░      ░  ░
                                                                                                        {colorama.Fore.RESET}""")

temp_emails = []

emails = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1').json()
for email in emails:
    temp_emails.append({'address': email.split('@')[0], 'domain': email.split('@')[1]})

previous_id = 0
print('Here is your one time email: '+temp_emails[0]['address']+'@'+temp_emails[0]['domain']+'\nIt will exist while program is running.')
print('Also, i coded this program in 45 lines.')
while True:
    inbox = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={temp_emails[0]["address"]}&domain={temp_emails[0]["domain"]}').json()
    if inbox != []:
        for inbox_el in inbox:
            if inbox_el['id'] > previous_id:
                previous_id = inbox_el['id']
                message = requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={temp_emails[0]["address"]}&domain={temp_emails[0]["domain"]}&id={inbox_el["id"]}').json()
                message_content = f"""
From: {message['from']} | {message['date']}
Subject: {message['subject'] if not message['subject'] == '' else 'No subject'}
{message['textBody'] if not message['textBody'] == '' else 'No content'}
"""

                print(message_content)

                if message['attachments'] != []:
                    if tkinter.messagebox.askyesno('Wowwie', 'You got some attachments in message, wanna download?'):
                        for attachment in message['attachments']:
                            open(attachment['filename'], 'wb').write(requests.get(f'https://www.1secmail.com/api/v1/?action=download&login={temp_emails[0]["address"]}&domain={temp_emails[0]["domain"]}&id={message["id"]}&file={attachment["filename"]}').content)
