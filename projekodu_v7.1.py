# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO              # çağırılan kütüphaneler         
import datetime
import picamera
import time
from time import sleep
import smtplib # email icin
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess # dropbox icin
#######################################################
GPIO.setmode(GPIO.BCM)
TRIG= 17
ECHO= 18
LED1= 23
LED2= 24
# LED_INTERNET = 25
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2,GPIO.OUT)
# GPIO.setup(LED_INTERNET,GPIO.OUT)
GPIO.output(TRIG,False)
sleep(0.5)

sayac = 0
erteleme = 0.2
mesafe_siniri = 50
video_suresi = 3
gonderen = "kimoguvenlik00@gmail.com"
alici = "erentalha24@gmail.com"
######################################################

def mesafe_olc():
   """Sonar mesafe olcer"""
   GPIO.output(TRIG, True)

   # set Trigger after 0.01ms to LOW
   sleep(0.00001)
   GPIO.output(TRIG, False)

   StartTime = time.time()
   StopTime = time.time()

   while GPIO.input(ECHO) == 0:
      StartTime = time.time()

   # save time of arrival
   while GPIO.input(ECHO) == 1:
      StopTime = time.time()

   # time difference between start and arrival
   TimeElapsed = StopTime - StartTime
   # multiply with the sonic speed (34300 cm/s)
   # and divide by 2, because there and back
   mesafe = (TimeElapsed * 34300) / 2

   return round(mesafe, 2)


def fotograf_cek():
   """Kamerayi kullanarak fotograf çeker tarihle dosya ismini geri döndürür"""
   print("Fotograf cekiyorum")
   foto_isim = datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S.jpg") 
   with picamera.PiCamera() as camera:
      camera.capture(foto_isim)

   return foto_isim


def video_cek():
   """Kamerayi kullanarak vidoe çeker tarihle dosya ismini geri döndürür"""
   print("Video Çekiyorum")
   video_isim = datetime.datetime.now().strftime("%d-%m-%Y-%H%M%S.h264")
   with picamera.PiCamera() as camera:
      camera.start_preview()     
      camera.start_recording(video_isim)
      sleep(video_suresi)                                             #VİDEO SÜRESİ AYARI
      camera.stop_recording()
      camera.stop_preview()

   return video_isim


def mail_gonder(goruntu_tipi):
   """Fotoğraf veya video tipini kullanarak kullanıcıya email gönderir. """
   t = datetime.datetime.now()
   tarih = t.strftime(" %d-%m-%Y tarihinde saat %H:%M da")
   
   mesaj = MIMEMultipart('alternative')
   html = """\
   <html>
   <head></head>
   <body>
      <p>Merhaba Eren Talha,<br>
         Kapınızda biri var,<br> """ + tarih + """<br>""" + goruntu_tipi + """
         çektim! Bu <a href="https://www.dropbox.com/sh/h269sw7ja9augmk/AABjPLQb17NRiaXNt8ej_Qrna?dl=0">linkten</a> görüntülere ulaşabilirsiniz.
      </p>
   </body>
   </html>
   """

   mesaj.attach( MIMEText(html, 'html'))
   mesaj['Subject'] = 'Kim O! Projesi'
   mesaj['From'] = gonderen
   mesaj['To'] = alici
   mail= smtplib.SMTP("smtp.gmail.com",587)
   mail.ehlo()
   mail.starttls()
   mail.login("kimoguvenlik00@gmail.com","lozixwuetdagkgnj")   
   mail.send_message(mesaj)
   mail.quit()

def dropboxa_gonder(dosyaismi):
   """Verilen dosyayı mp4 formatına çevirip Dropbox a gönderir."""

   print("../Dropbox-Uploader/dropbox_uploader.sh upload ./{} media/{}".format(dosyaismi, dosyaismi))
   subprocess.call("../Dropbox-Uploader/dropbox_uploader.sh upload ./{} media/{}".format(dosyaismi, dosyaismi), shell=True) 


while True:
   mesafe_listesi = []
   for i in range(5): # Beş farklı ölçüm al.
      mesafe_listesi.append(mesafe_olc())

   mesafe_listesi = sorted(mesafe_listesi)
   mesafe = mesafe_listesi[2] # ortanca değeri seç.
   
   if  mesafe < mesafe_siniri :                                                            
      sayac = sayac + 1
      print(sayac)
      sleep(0.1)
      print ("Çok Yaklaştın! \n")

      if (sayac==3) or (sayac==5) or (sayac==7):  
         # GPIO.output(LED_INTERNET,True)
         GPIO.output(LED1,True)             
         GPIO.output(LED2,True)
         foto_isim = fotograf_cek()   
         mail_gonder("fotoğraf")
         dropboxa_gonder(foto_isim)
         GPIO.output(LED1,False)             
         GPIO.output(LED2,False)             
         # GPIO.output(LED_INTERNET,False)

      # Şüpheli 10 saniyeden fazla oyalanırsa 1 dakikalık video kaydı başlar.
      if sayac == 10:
         GPIO.output(LED1,True)             
         GPIO.output(LED2,True)  
         video_isim = video_cek()
         mail_gonder("video")
         mp4_isim = video_isim.replace('h264', 'mp4')
         subprocess.call("avconv -i {} -vcodec copy -r 252/100 {}".format(video_isim, mp4_isim), shell=True)
         dropboxa_gonder(mp4_isim)
         GPIO.output(LED1,False)             
         GPIO.output(LED2,False)      

   print ("Olculen Mesafe:",mesafe," cm")

   if mesafe > 50:
      sayac = 0
 
   sleep(erteleme)
 

GPIO.cleanup()

 