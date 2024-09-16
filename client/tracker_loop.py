from typing import Callable

import cv2

from client_config import bottom_right, top_left
from hand_tracker import HandTracker

def tracker_loop(on_track: Callable[[list | list[list]], None] | None):
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Change to 0 for default camera
    tracker = HandTracker()
    try:
        while True:
            success, image = cap.read()

            # Draw the rectangle on the image
            cv2.rectangle(image, top_left, bottom_right, (255, 0, 0), 3)
            if success:
                image = tracker.handsFinder(image)
                lmList = tracker.positionFinder(image)

                if on_track is not None:
                    on_track(lmList)

                cv2.imshow("Video", image)
                
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Corrected key event handling
                    break
            else:
                print("Failed to capture image")
    finally:
        # Move the release and destroy commands outside the while loop
        cap.release()
        cv2.destroyAllWindows()