import csv
import os
import smtplib
from datetime import date, timedelta
from email.message import EmailMessage
from config import Config


EMAIL_USER = Config.EMAIL_USER
EMAIL_PASS = Config.EMAIL_PASS
csv_path = Config.CSV_PATH
csv_file = f"{csv_path}/schedule.csv"
today = date.today()
recipient = Config.RECIPIENT
new_list = []

with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)

    for line in csv_reader:
        due_date = date.fromisoformat(line['DueDate'])
        remove_task_date = due_date + timedelta(days=14)
        if today == due_date:
            msg = EmailMessage()
            msg['Subject'] = line['Subject']
            msg['From'] = EMAIL_USER
            msg['To'] = recipient
            msg.set_content(line['Message'])

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                connection.login(user=EMAIL_USER, password=EMAIL_PASS)
                connection.send_message(msg=msg)
        elif today < remove_task_date:
            new_list.append(line)

with open(csv_file, 'w', newline='') as new_file:
    fieldnames = ['Subject', 'DueDate', 'Message']
    csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
    for list in new_list:
        csv_writer.writerow(list)
        