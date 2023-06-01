# Automatic Data Scraping and Email Sending

This Python code automatically scrapes data from a specific website and sends it to a desired email address.

## Usage Instructions

1. Install the Python requirements:

pip install selenium requests

2. Download ChromeDriver and choose the version that matches your Chrome browser. Then, update the `driver_path` variable and specify the file path of ChromeDriver.

3. Set up the login credentials:
- `username`: Variable containing your username for the website.
- `password`: Variable containing your password for the website.

4. Configure email settings:
- `sender_email`: Variable containing the email address of the sender.
- `recipients`: List containing the email addresses of the recipients who should receive the email.
- `sender_password`: Variable containing the password of the sender's email account.
- `mail_server`: Variable containing the address of the email server.
- `mail_port`: Variable containing the port number of the email server.

5. Specify the download folder:
Update the `download_folder` variable to the correct path where downloaded files should be saved.

6. Run the code:

python test.py

7. The automatic data scraping and email sending process will take place, and you will see the results in the console.

**Note:** Please make sure to modify the URLs in the code according to the website you want to scrape data from. Replace the example URLs with the correct URLs.