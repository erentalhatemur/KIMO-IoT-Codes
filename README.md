![image](https://github.com/erentalhatemur/KIMO-IoT-Codes/assets/165311868/7e44f502-b6ea-4168-b437-b29a5892528f)

# Kim O! - Raspberry Pi Akıllı Kapı Güvenlik Sistemi / Who's There! - Smart Door Security System

Bu proje, bir Raspberry Pi, Pi Camera ve ultrasonik mesafe sensörü (HC-SR04) kullanarak basit ama etkili bir kapı güvenlik sistemi oluşturur. Sistem, kapıya 50 cm'den fazla yaklaşan birini algıladığında otomatik olarak fotoğraf ve video kaydı başlatır, bu kayıtları Dropbox'a yükler ve kullanıcıya e-posta ile bildirim gönderir.

This project is a simple but effective smart door security system using a Raspberry Pi, Pi Camera, and an HC-SR04 ultrasonic distance sensor. When the system detects a person closer than 50 cm, it automatically captures a photo and a 10-second video, uploads these files to Dropbox, and notifies the user via email.

---

## ⚙️ Çalışma Mantığı / How It Works

Script, sonsuz bir döngü içinde çalışır ve sürekli olarak mesafeyi ölçer:
The script runs in an infinite loop, continuously measuring the distance:

1.  **Gürültü Filtreleme / Noise Filtering:**
    Sistem, hatalı ölçümleri engellemek için 5 adet mesafe ölçümü alır, bunları sıralar ve ortadaki değeri (medyan) geçerli mesafe olarak kabul eder.
    The system takes 5 distance measurements to prevent false readings, sorts them, and uses the middle value (median) as the valid distance.

2.  **Algılama / Detection:**
    Eğer ölçülen mesafe `50 cm` sınırının altındaysa, bir `sayac` (sayaç) artırılır. Bu, anlık bir gölgenin veya hatanın sistemi tetiklemesini engeller.
    If the measured distance is below the `50 cm` threshold, a `sayac` (counter) is incremented. This prevents the system from being triggered by a passing shadow or error.

3.  **Tetiklenme / Triggering:**
    `sayac` 3'e ulaştığında (yani bir nesne kısa bir süre kapının önünde durduğunda) sistem harekete geçer:
    When the `sayac` reaches 3 (meaning an object has been stationary in front of the door for a short period), the system activates:
    * **Fotoğraf / Photo:** Hemen bir fotoğraf çeker (`fotograf_cek()`). / Immediately captures a photo (`fotograf_cek()`).
    * **Bildirim 1 / Notification 1:** Fotoğrafın çekildiğini belirten bir e-posta gönderir (`mail_gonder()`). / Sends an email notification that a photo has been taken (`mail_gonder()`).
    * **Upload 1:** Çekilen `.jpg` dosyasını Dropbox'a yükler (`dropboxa_gonder()`). / Uploads the captured `.jpg` file to Dropbox (`dropboxa_gonder()`).
    * **Video Kaydı / Video Recording:** 10 saniyelik (`video_suresi`) bir video kaydı başlatır (`video_cek()`). / Starts a 10-second (`video_suresi`) video recording (`video_cek()`).
    * **Bildirim 2 / Notification 2:** Video kaydının yapıldığını belirten ikinci bir e-posta gönderir. / Sends a second email notification that a video has been recorded.
    * **Video Dönüştürme / Video Conversion:** Çekilen `.h264` formatındaki videoyu `.mp4` formatına dönüştürür. / Converts the raw `.h264` video file to `.mp4` format.
    * **Upload 2:** Dönüştürülen `.mp4` videosunu Dropbox'a yükler. / Uploads the converted `.mp4` video to Dropbox.

4.  **Sıfırlama / Reset:**
    Eğer mesafe tekrar `50 cm` üzerine çıkarsa, `sayac` sıfırlanır ve sistem normal izleme moduna döner.
    If the distance exceeds `50 cm` again, the `sayac` is reset, and the system returns to normal monitoring mode.

---

## 🛠️ Donanım Gereksinimleri / Hardware Requirements

* **TR:** Raspberry Pi (Herhangi bir modeli) / **EN:** Raspberry Pi (Any model)
* [Raspberry Pi Camera Module](https://www.raspberrypi.com/products/camera-module-v2/)
* **TR:** HC-SR04 Ultrasonik Mesafe Sensörü / **EN:** [HC-SR04 Ultrasonic Distance Sensor](https://www.sparkfun.com/products/15569)
* **TR:** 2 adet LED (Opsiyonel, kodda `LED1` ve `LED2` olarak tanımlanmış ancak ana döngüde kullanılmıyor) / **EN:** 2x LEDs (Optional, defined in the code as `LED1` and `LED2` but not used in the main loop)
* **TR:** Jumper kablolar ve Breadboard / **EN:** Jumper wires and a Breadboard

### GPIO Bağlantıları / GPIO Connections

**TR:** Kodunuz (BCM pin numaralandırmasına göre) aşağıdaki bağlantıları beklemektedir:
**EN:** Your code (based on BCM pin numbering) expects the following connections:

* **HC-SR04 TRIG:** `GPIO 17`
* **HC-SR04 ECHO:** `GPIO 18`
* **LED 1:** `GPIO 23` (Opsiyonel / Optional)
* **LED 2:** `GPIO 24` (Opsiyonel / Optional)
* **Pi Camera:** CSI port

---

## 📦 Kurulum ve Bağımlılıklar / Setup & Dependencies

**TR:** Bu projenin çalışması için `KIMO-IoT-Codes.py` script'inin yanı sıra bazı harici yazılımlara ve Python kütüphanelerine ihtiyaç vardır.
**EN:** To run this project, you need the `KIMO-IoT-Codes.py` script as well as some external software and Python libraries.

### 1. Python Kütüphaneleri / Python Libraries

**TR:** Kodunuz `picamera` kütüphanesini kullanır. Eğer yüklü değilse:
**EN:** Your code uses the `picamera` library. If it's not installed:
```bash
sudo apt-get update
sudo apt-get install python3-picamera
```

### 2. Video Dönüştürme / Video Conversion (avconv / libav-tools)

**TR:** Kod, `.h264` formatındaki ham kamera çıktısını `.mp4` formatına çevirmek için `avconv` komutunu kullanır. Bu, `libav-tools` paketinin bir parçasıdır.
**EN:** The code uses the `avconv` command to convert the raw `.h264` camera output to `.mp4`. This is part of the `libav-tools` package.
```bash
sudo apt-get install libav-tools
```
**(TR Not:** Bazı sistemlerde `avconv` yerine `ffmpeg` kullanılır. Eğer `avconv` bulunamazsa, koddaki `subprocess.call` satırını `ffmpeg` kullanacak şekilde güncellemeniz gerekebilir.)
**(EN Note:** Some systems use `ffmpeg` instead of `avconv`. If `avconv` is not found, you may need to update the `subprocess.call` line in the code to use `ffmpeg`.)*

### 3. Dropbox Uploader

**TR:** Proje, dosyaları Dropbox'a yüklemek için [Dropbox-Uploader](https://github.com/andreafabritiso/Dropbox-Uploader) adlı bir bash script'ine bağımlıdır.
**EN:** The project depends on a bash script called [Dropbox-Uploader](https://github.com/andreafabritiso/Dropbox-Uploader) to upload files to Dropbox.

* **TR:** Kodunuz, bu script'in `../Dropbox-Uploader/dropbox_uploader.sh` yolunda, yani ana script'inizin **bir üst dizininde** olduğunu varsayar.
    **EN:** Your code assumes this script is located at `../Dropbox-Uploader/dropbox_uploader.sh`, which is in the **parent directory** of your main script.
* **TR:** Bu script'i kurmanız ve `dropbox_uploader.sh config` komutu ile kendi Dropbox hesabınıza bir kereye mahsus bağlamanız gerekmektedir.
    **EN:** You must install this script and link it to your own Dropbox account once using the `dropbox_uploader.sh config` command.

---

## 🔧 Yapılandırma / Configuration

**TR:** Script'i çalıştırmadan önce, dosyanın başındaki değişkenleri kendi bilgilerinize göre düzenlemeniz **şarttır**:
**EN:** Before running the script, it is **mandatory** to edit the variables at the beginning of the file with your own information:

```python
# ... (Diğer değişkenler / Other variables) ...

# === E-POSTA AYARLARI / EMAIL SETTINGS ===

# TR: E-postayı gönderecek Gmail hesabı
# EN: The Gmail account that will send the email
gonderen = "kimoguvenlik00@gmail.com" 

# TR: Gmail için "Uygulama Şifresi" (Normal şifreniz değil!)
# TR: Google Hesap Ayarları > Güvenlik > Uygulama Şifreleri bölümünden alınır.
# EN: Gmail "App Password" (Not your normal password!)
# EN: Get this from Google Account Settings > Security > App Passwords.
gmail_sifresi = "tgwhqcpeftaytlez"  # <-- BU ŞİFREYİ DEĞİŞTİRİN! / CHANGE THIS PASSWORD!

# TR: Bildirimlerin gideceği e-posta adresi
# EN: The email address that will receive the notifications
alici = "homeuser@gmail.com"     # <-- Kendi alıcı adresinizle değiştirin / Change to your own recipient address

# ...

# === DROPBOX AYARLARI (mail_gonder fonksiyonu içinde) / DROPBOX SETTINGS (inside the mail_gonder function) ===
# TR: mail_gonder() fonksiyonu içindeki Dropbox linkini kendi
# TR: Dropbox-Uploader uygulamanızın klasör linki ile güncelleyin.
# EN: Update the Dropbox link inside the mail_gonder() function with the folder link
# EN: from your Dropbox-Uploader app.
html = """
...
Bu <a href="[https://www.dropbox.com/home/Apps/kimo_app2/media](https://www.dropbox.com/home/Apps/kimo_app2/media)">linkten</a> görüntülere ulaşabilirsiniz.
You can access the images from this <a href="[https://www.dropbox.com/home/Apps/kimo_app2/media](https://www.dropbox.com/home/Apps/kimo_app2/media)">link</a>.
...
""" # <-- BU LİNKİ GÜNCELLEYİN! / UPDATE THIS LINK!
```

### ⚠️ ÖNEMLİ GÜVENLİK NOTU / IMPORTANT SECURITY NOTE

**TR:**
Kodunuz, `gmail_sifresi` değişkeninde bir **Uygulama Şifresi** kullanıyor. Bu, güvenlik açısından doğrudur. Eğer bu şifre artık geçerli değilse veya kendi hesabınızı kullanacaksanız, Google Hesabınızın "Güvenlik" bölümünden yeni bir "Uygulama Şifresi" oluşturmalı ve `gmail_sifresi` değişkenine onu girmelisiniz. **Asla normal Gmail şifrenizi koda yazmayın.**

**EN:**
Your code uses an **App Password** in the `gmail_sifresi` variable. This is the correct security practice. If this password is no longer valid, or if you are using your own account, you must generate a new "App Password" from your Google Account's "Security" section and enter it into the `gmail_sifresi` variable. **Never write your normal Gmail password directly in the code.**


ÇALIŞMA PRENSİBİNİN 3D GÖRÜNTÜSÜ
![Ekran görüntüsü 2024-06-30 111255](https://github.com/erentalhatemur/KIMO-IoT-Codes/assets/165311868/056651c7-1a6f-44e8-90a8-fef1ac8931e3)


Gönderilen e-mail'den bir örnek
![image](https://github.com/erentalhatemur/KIMO-IoT-Codes/assets/165311868/1f942fc4-80d0-463a-b669-c41f7b950c02)






