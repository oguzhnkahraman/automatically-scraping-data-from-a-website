import time
import os
import requests
import smtplib
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Define login credentials
username = "username"
password = "password"

# Specify the file path and options for ChromeDriver
driver_path = "C:/Python311/chromedriver.exe"  # Enter the file path of ChromeDriver here
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Enables running in headless mode (optional)

# Configure the WebDriver
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# Log in to the panel
driver.get("https://ilanbis.bik.gov.tr")
driver.find_element(By.CSS_SELECTOR, "input#UserName.form-control").send_keys(username)
driver.find_element(By.CSS_SELECTOR, "input#Password.form-control").send_keys(password)
driver.find_element(By.CSS_SELECTOR, "button#giris.btn.btn-primary.btn-flat.btn-block").click()

# Wait and go to the announcement page
wait = WebDriverWait(driver, 5)
announcement_link = "https://ilanbis.bik.gov.tr/Ilan/IndexYayin"
driver.get(announcement_link)

# Wait and select the checkbox
checkbox = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "icheckbox_square-blue")))
checkbox.click()

# Wait and click on the "ilanlar" button
announcements_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-group.ilanlar-buttons")))
announcements_button.click()

# Wait and download the announcements
time.sleep(2)  # Wait for the announcements to load

# Specify the download folder
download_folder = "C:/Users/your_account/Downloads"  # Modify the download folder accordingly

# Wait and find the latest downloaded file
latest_file = None
start_time = time.time()

while time.time() - start_time < 10:  # Wait for the downloaded file for 10 seconds
    time.sleep(1)
    files = glob.glob(download_folder + "/*")
    if files:
        latest_file = max(files, key=os.path.getctime)
        break

if latest_file is not None:
    print("Latest downloaded file:", latest_file)
    file_name = os.path.basename(latest_file)
    downloaded_file_path = latest_file

    # Email settings
    sender_email = "send_mail"
    recipients = [
        "mail_1",
        "mail_2",
        "mail_3",
    ]
    sender_password = "mail_password*"
    mail_server = "smtp"
    mail_port = 465

    # Email sending process
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = "subject"

    # Add email body (optional)
    message_text = "text"
    msg.attach(MIMEText(message_text, "plain"))

    # Add the downloaded file as an attachment
    with open(downloaded_file_path, "rb") as file:
        attachment = MIMEApplication(file.read(), Name=file_name)
    attachment["Content-Disposition"] = f"attachment; filename={file_name}"
    msg.attach(attachment)

    # Connect to the email server and send the email
    try:
        server = smtplib.SMTP_SSL(mail_server, mail_port)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("Email sent.")
    except Exception as e:
        print("Email sending error:", str(e))
else:
    print("Downloaded file not found.")

# Close the WebDriver
driver.quit()
