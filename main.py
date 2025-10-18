import requests
from datetime import date
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

#Load environment data from env file
load_dotenv()

#Get variables from env files
newsletter_api_key = os.getenv("NEWSLETTER_API_KEY")
sender_mail_id = os.getenv("SENDER_MAIL_ID")
sender_password = os.getenv("SENDER_MAIL_PASSWORD")

#initialize email variables
receiver_mail_id = os.getenv("RECEIVER_MAIL")
today = date.today()
iso_tuple = today.isocalendar()
week_number = iso_tuple[1]
subject = f"Sci-Tech Headlines Today - Newsletter - CW{week_number}"

#Get and Compose Newsletter from Newsdata API. Just first 10 news
url = "https://newsdata.io/api/1/sources?apikey="+newsletter_api_key+"&category=technology,science&language=en"
request = requests.get(url)
content = request.json()
first_ten_news = content['results'][0:10]

email_message = ""

for index,news in enumerate(first_ten_news):
    formatted_news = (f"{index+1}. {news['name']} \n {news['description']} \n"
                      f"{news['url']} \n \n")
    email_message = email_message + formatted_news

#Compose Mail
msg = MIMEText(email_message, 'plain', 'utf-8')
msg['Subject'] = subject
msg['From'] = sender_mail_id
msg['To'] = receiver_mail_id

#setup SMTP and Send mail
try:
    # Connect to the SMTP server, 587 since TLS is used
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_mail_id, sender_password)

    # send email
    server.send_message(msg)

except Exception as e:
    print(f"Error sending email: {e}")

finally:
    server.quit()

#Not using below since it kept didn't support UTF-8

# def send_email(sender_mail,sender_pass,message):
#     host = "smtp.gmail.com"
#     port = 465
#
#     receiver = ""
#     context = ssl.create_default_context()
#
#     with smtplib.SMTP_SSL(host, port, context=context) as server:
#         server.login(sender_mail, sender_pass)
#         server.sendmail(sender_mail, receiver, message)
#
# send_email(sender_mail_id, sender_password,email_message)