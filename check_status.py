import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuration
URL = "https://krishakbandhu.wb.gov.in/agricultural-labour/farmer_search?query=7866852729&commit=Search"
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def scrape_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This looks for the table or result container on the page
        # Adjusting to capture common result areas in government sites
        content = soup.find('table') or soup.find('div', class_='container')
        
        if content:
            return content.get_text(strip=True, separator='\n')
        else:
            return "No specific data table found. The page might be empty or layout changed."
            
    except Exception as e:
        return f"Error scraping website: {str(e)}"

def send_email(result_text):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "Daily Krishak Bandhu Status Update"

    body = f"Here is the search result for mobile 7866852729:\n\n{result_text}\n\nLink: {URL}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    result = scrape_data()
    send_email(result)
