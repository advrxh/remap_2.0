import socket
import mouse
import screeninfo
import time

UDP_PORT = 4210

SENS_X = 0.01
SENS_Y = 0.01

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
        for i in data:
            gyro[i.split(":")[0]] = int(i.split(":")[1])

        print(gyro)

        dh = -1 * gyro["gx"] * SENS_X
        dw = -1 * gyro["gz"] * SENS_Y

        mouse.move(dw, dh, absolute=False)

    except socket.timeout:
        continue  
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(0.01)
