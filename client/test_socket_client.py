from socket_client import SocketClient
import math
import time

# move in a circle around the center
# fixed amount of time
def circle(client, radius = 0.5):
    for i in range(0, 361, 2):
        x = 0.5 + (radius) * math.cos(i * (2*math.pi/360))
        y = 0.5 +  (radius) * math.sin(i * (2*math.pi/360))
        client.send_state(x, y, 1)
        time.sleep(0.01)
    client.send_state(0.5, 0.5, 0)


host = "raspberrypi.local"
port = 12345
with SocketClient(host=host, port=port) as client:
    while True:
        x, y, s = map(float, input().split())

        if (s < 0):
            if (abs(s) <= 0.5):
                circle(client, abs(s))
            else:
                circle(client)
            continue

        x = max(min(x, 1), 0)
        y = max(min(y, 1), 0)
        client.send_state(x, y, s)
    
