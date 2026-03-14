import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

# কনফিগারেশন
URL = "https://krishakbandhu.wb.gov.in/agricultural-labour/farmer_search?query=7866852729&commit=Search"
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

def check_status():
    try:
        response = requests.get(URL, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ওয়েবসাইটের রেজাল্ট সেকশন খুঁজে বের করা (সাধারণত টেবিল বা নির্দিষ্ট ডিভ)
        # আপনি চাইলে পুরো টেক্সট পাঠাতে পারেন অথবা নির্দিষ্ট অংশ ফিল্টার করতে পারেন
        result_text = soup.get_text(strip=True)
        
        # এখানে আমরা রেজাল্টের একটি নির্দিষ্ট অংশ ইমেইলে পাঠাব
        send_email("Krishak Bandhu Status Update", result_text[:1000]) # প্রথম ১০০০ ক্যারেক্টার
        
    except Exception as e:
        print(f"Error: {e}")

def send_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS # নিজের ইমেইলেই রেজাল্ট যাবে
    msg.set_content(f"Current Status from Website:\n\n{body}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("Email sent successfully!")

if __name__ == "__main__":
    check_status()
  
