import gpiozero
import socket
import time

gpiozero.Device.pin_factory = gpiozero.pins.pigpio.PiGPIOFactory()
s1 = gpiozero.AngularServo(12, min_angle=-45, max_angle=45)
s2 = gpiozero.AngularServo(13, min_angle=-45, max_angle=45)
l = gpiozero.LED(2)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''  # Bind to all interfaces
port = 12345  # Port to listen on
server_socket.bind((host, port))
server_socket.listen(1)
try:
    while True:
        # Accept a new connection
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")

        f = client_socket.makefile("rwb")

        try:
            while True:
                # Receive data from the client

                data = f.readline().decode("utf-8")
                # data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    # No data received, break the inner loop to close the connection
                    break
                print(f"{data=}")
                angle_x, angle_y, state = map(float, data.split(" "))
                assert -45 <= angle_x <= 45
                assert -45 <= angle_y <= 45
                s1.angle = angle_x
                s2.angle = angle_y
                if state != 0:
                    l.on()
                else:
                    l.off()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the connection
            client_socket.close()
            print(f"Connection from {address} has been closed.")
finally:
    server_socket.close()