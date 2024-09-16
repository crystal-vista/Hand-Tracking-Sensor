import math

from client_config import host, port, bottom_right, top_left, motor_bottom, motor_left, motor_right, motor_top
from socket_client import SocketClient
from tracker_loop import tracker_loop

def main():
    with SocketClient(host=host, port=port) as socket_client:
        on_last = False
        save_x = 0
        save_y = 0
        toggle = False
        def on_track(lm_list: list | list[list]):
            max_dist = 0
            lmListMain = None
            nonlocal on_last
            nonlocal save_x
            nonlocal save_y
            nonlocal toggle

            # check which of the hands has greater pointer-thumb distance, follow that one
            for l in lm_list:
                if not l:
                    continue
                distance = math.hypot(l[0][1] - l[1][1], l[0][2] - l[1][2])
                print(distance)
                if distance > max_dist:
                    max_dist = distance
                    lmListMain = l

            if lmListMain: 
                # second element is the index finger, first is thumb
                distance = math.hypot(lmListMain[0][1] - lmListMain[1][1], lmListMain[0][2] - lmListMain[1][2])

                # Calculate destination motor coordinates
                x = (lmListMain[0][1] + lmListMain[1][1]) / 2
                y = (lmListMain[0][2] + lmListMain[1][2]) / 2
                sx = (x - top_left[0]) / (bottom_right[0] - top_left[0])
                sy = (y - top_left[1]) / (bottom_right[1] - top_left[1])
                sy = 1 - sy
                mx = motor_left + sx * (motor_right - motor_left)
                my = motor_bottom + sy * (motor_top - motor_bottom)

                print(f"{mx=} {my=} {distance=}")
                cur = distance > 20
                if cur and not on_last:
                    toggle = not toggle
                if cur and toggle:
                    save_x = mx
                    save_y = my
                on_last = cur
                socket_client.send_state(save_x, save_y, toggle)
        
        tracker_loop(on_track)

if __name__ == "__main__":
    main()
