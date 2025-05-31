import RPi.GPIO as GPIO
import time
import requests
from picamera import PiCamera

# Telegram config
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

# Setup
PIR_PIN = 4  # GPIO pin connected to PIR sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

camera = PiCamera()
camera.resolution = (1024, 768)

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def send_photo(photo_path):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    with open(photo_path, 'rb') as photo:
        requests.post(url, files={'photo': photo}, data={'chat_id': CHAT_ID})

try:
    print("Motion sensor active. Waiting for motion...")
    send_telegram_message("🟢 Security system activated.")
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            image_path = f"/home/pi/motion_{timestamp}.jpg"
            camera.capture(image_path)
            send_telegram_message("⚠️ Motion detected! Sending photo...")
            send_photo(image_path)
            time.sleep(10)  # delay to avoid multiple alerts
        time.sleep(1)

except KeyboardInterrupt:
    print("System stopped by user.")
    GPIO.cleanup()
    send_telegram_message("🔴 Security system deactivated.")
