import cv2
import math
from hand_tracker import HandTracker

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Change to 0 for default camera
    tracker = HandTracker()

    # host = "raspberrypi.local"
    # port = 12345
    motor_left = 0.304
    motor_right = 0.72
    motor_bottom = 0.466
    motor_top = 0.89

    top_left = (120, 40)
    bottom_right = (520, 440)
    # with SocketClient(host=host, port=port) as socket_client:
    while True:
        success, image = cap.read()
        # draw rectangle
        # Get the dimensions of the image
        height, width, _ = image.shape
        # # Calculate the center of the image
        # center_y, center_x = height // 2, width // 2

        # # # Define the size of the square
        # square_size = 1000

        # # # Calculate the top left and bottom right points of the square
        # top_left = (center_x - square_size // 2, center_y - square_size // 2)
        # bottom_right = (center_x + square_size // 2, center_y + square_size // 2)

        def inSquare(point):
            # check if point is in square printed above
            if point[0] > top_left[0] and point[0] < bottom_right[0]:
                if point[1] > top_left[1] and point[1] < bottom_right[1]:
                    return True
            return False

        cv2.rectangle(image, top_left, bottom_right, (255, 0, 0), 3)
        if success:
            image = tracker.handsFinder(image)
            lmList = tracker.positionFinder(image)

            # Check if the landmark list is not empty

            max_dist = 0
            lmListMain = None
            # check which of the hands has greater pointer-thumb distance, follow that one
            for l in lmList:
                if not l:
                    continue
                distance = math.hypot(l[0][1] - l[1][1], l[0][2] - l[1][2])
                # print(distance)
                if distance > max_dist:
                    max_dist = distance
                    lmListMain = l

            if lmListMain: 
                # second element is the index finger, first is thumb
                distance = math.hypot(lmListMain[0][1] - lmListMain[1][1], lmListMain[0][2] - lmListMain[1][2])

                # Convert the list to a string and send it
                x = lmListMain[1][1]
                y = lmListMain[1][2]
                sx = (x - top_left[0]) / (bottom_right[0] - top_left[0])
                sy = (y - top_left[1]) / (bottom_right[1] - top_left[1])
                sy = 1 - sy
                mx = motor_left + sx * (motor_right - motor_left)
                my = motor_bottom + sy * (motor_top - motor_bottom)

                # if distance>100 and inSquare((lmList[1][1],lmList[1][2])):
                # socket_client.send_state(mx, my, True)
                print(f"mx: {mx}, my: {my}")
                # print(f"active")
                    # print(lmList)
                # socket_client.send_state(mx, my, False)

                    # print("Off")


            cv2.imshow("Video", image)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Corrected key event handling
                break
            
            # Draw the square on the image


        else:
            print("Failed to capture image")

    # Move the release and destroy commands outside the while loop
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
