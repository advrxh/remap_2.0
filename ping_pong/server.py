from ping_pong import PongGame
import socket
import time

UDP_PORT = 4210
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", UDP_PORT))
sock.setblocking(False)

def get_gyro_data():
    try:
        data, addr = sock.recvfrom(1024)
        text = data.decode().strip().split(";")
        gyro = {i.split(":")[0]: int(i.split(":")[1]) for i in text}
        return gyro
    except BlockingIOError:
        return None
    except Exception as e:
        print(f"UDP Error: {e}")
        return None

game = PongGame()
running = True

while running:
    game.clock.tick(game.FPS)
    running = game.handle_events()
    gyro_data = get_gyro_data()
    game.update(gyro_data, sens_y=0.02)
    game.draw()

game.quit()

