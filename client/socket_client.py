import socket
import math

class SocketClient:
    _socket: socket.socket
    _host: str
    _port: int

    def __init__(self, host: str, port: int) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port
        pass

    def __enter__(self) -> 'SocketClient':
        self._socket.connect((self._host, self._port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket.close()

    def send_state(self, x: float, y: float, state: bool):
        x = max(min(x, 1), 0)
        y = max(min(y, 1), 0)
        y = 1 - y
        ang_x = -math.degrees(math.atan(x * 2 - 1))
        ang_y = -math.degrees(math.atan(y * 2 - 1))
        data = f"{ang_x} {ang_y} {1 if state else 0}\n"
        print(f"sending data {data}")
        self._socket.send(data.encode('utf-8'))
