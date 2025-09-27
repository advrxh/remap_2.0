import socket
import mouse
import screeninfo
import time
import math

UDP_PORT = 4210

SENS_X = 0.01
SENS_Y = 0.01

BTN_DELAY = .5
LEFT_LAST_CLICKED = 0
RIGHT_LAST_CLICKED = 0

monitor = screeninfo.get_monitors()[0]
SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height

mouse.move(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))
sock.settimeout(1.0)

print("UDP client running, waiting for data...")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        data = data.decode().strip().split(";")

        gyro = {}
        mouse_data = {}

        for i in data[:2]:
            gyro[i.split(":")[0]] = int(i.split(":")[1])

        for i in data[2:]:
            mouse_data[i.split(":")[0]] = i.split(":")[1] == "ON"

        dh = -1 * math.floor(gyro["gx"]/1.1) * SENS_X
        dw = -1 * math.floor(gyro["gz"]/1.1) * SENS_Y

        if mouse_data["left_btn"] and time.time() - LEFT_LAST_CLICKED > BTN_DELAY:
            mouse.click("left")
            LEFT_LAST_CLICKED = time.time()

        if mouse_data["right_btn"] and time.time() - RIGHT_LAST_CLICKED > BTN_DELAY:
            mouse.click("right")
            RIGHT_LAST_CLICKED = time.time()

        mouse.move(dw, dh, absolute=False)

    except socket.timeout:
        continue  
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(0.01)
