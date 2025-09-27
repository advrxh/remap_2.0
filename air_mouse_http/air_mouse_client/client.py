import screeninfo
import requests
import mouse
import time

ESP_IP = input("Enter IP of ESP server:")
URL = f"http://{ESP_IP}:80/"

SENS_X = 0.025
SENS_Y = 0.025

monitor = screeninfo.get_monitors()[0]
SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height

mouse.move(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

while True:
    try:
        r = requests.get(URL, timeout=5)
        if r.status_code == 200:
            data = r.text.strip().split(";")

            gyro = {}
            mouse_data = {}

            for i in data[:2]:
                gyro[i.split(":")[0]] = int(i.split(":")[1])

            for i in data[2:]:
                mouse_data[i.split(":")[0]]  = i.split(":")[1] == "ON"


            dh = -1 * gyro["gx"] * SENS_X
            dw = -1 * gyro["gz"] * SENS_Y

            if mouse_data["left_btn"]:
                mouse.click("left")

            if mouse_data["right_btn"]:
                mouse.click("right")

            mouse.move(dw, dh, absolute=False)

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(0.0075)
