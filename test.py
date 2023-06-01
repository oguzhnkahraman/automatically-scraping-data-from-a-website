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

# Giriş bilgilerini tanımlayın
kullanici_adi = "username"
sifre = "password"

# ChromeDriver'ın dosya yolunu ve seçeneklerini belirtin
driver_path = (
    "C:/Python311/chromedriver.exe"  # ChromeDriver'ın dosya yolunu buraya girin
)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Arka planda çalışmasını sağlar (isteğe bağlı)

# WebDriver'ı yapılandırın
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# Panele giriş yapın
driver.get("https://ilanbis.bik.gov.tr")
driver.find_element(By.CSS_SELECTOR, "input#UserName.form-control").send_keys(
    kullanici_adi
)
driver.find_element(By.CSS_SELECTOR, "input#Password.form-control").send_keys(sifre)
driver.find_element(
    By.CSS_SELECTOR, "button#giris.btn.btn-primary.btn-flat.btn-block"
).click()

# Bekleyin ve ilan sayfasına gidin
wait = WebDriverWait(driver, 5)
ilan_linki = "https://ilanbis.bik.gov.tr/Ilan/IndexYayin"
driver.get(ilan_linki)

# Bekleyin ve checkbox'ı seçin
checkbox = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "icheckbox_square-blue"))
)
checkbox.click()

# Bekleyin ve ilanlar butonuna basın
ilanlar_butonu = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "btn-group.ilanlar-buttons"))
)
ilanlar_butonu.click()

# Bekleyin ve ilanları indirin
time.sleep(2)  # İlanların yüklenmesi için bir süre bekleyin

# İndirme klasörünü belirleyin
download_folder = (
    "C:/Users/your_account/Downloads"  # İndirme klasörünü uygun şekilde değiştirin
)

# Bekleyin ve en son indirilen dosyayı bulun
latest_file = None
start_time = time.time()

while time.time() - start_time < 10:  # İndirilen dosyayı 10 saniye boyunca bekleyin
    time.sleep(1)
    files = glob.glob(download_folder + "/*")
    if files:
        latest_file = max(files, key=os.path.getctime)
        break

if latest_file is not None:
    print("En son indirilen dosya:", latest_file)
    dosya_adi = os.path.basename(latest_file)
    indirilen_dosya_yolu = latest_file

    # E-posta ayarları
    gonderen_email = "send_mail"
    alicilar = [
        "mail_1",
        "mail_2",
        "mail_3",
    ]
    gonderen_sifre = "mail_password*"
    mail_sunucusu = "smtp"
    mail_portu = 465

    # E-posta gönderme işlemi
    msg = MIMEMultipart()
    msg["From"] = gonderen_email
    msg["To"] = ", ".join(alicilar)
    msg["Subject"] = "subject"

    # E-posta metnini ekleyin (isteğe bağlı)
    mesaj_metni = "text"
    msg.attach(MIMEText(mesaj_metni, "plain"))

    # İndirilen dosyayı ekleyin
    with open(indirilen_dosya_yolu, "rb") as dosya:
        icerik_ek = MIMEApplication(dosya.read(), Name=dosya_adi)
    icerik_ek["Content-Disposition"] = f"attachment; filename={dosya_adi}"
    msg.attach(icerik_ek)

    # E-posta sunucusuna bağlanın ve e-postayı gönderin
    try:
        server = smtplib.SMTP_SSL(mail_sunucusu, mail_portu)
        server.login(gonderen_email, gonderen_sifre)
        server.send_message(msg)
        server.quit()
        print("E-posta gönderildi.")
    except Exception as e:
        print("E-posta gönderme hatası:", str(e))
else:
    print("İndirilen dosya bulunamadı.")


# WebDriver'ı kapatın
driver.quit()
