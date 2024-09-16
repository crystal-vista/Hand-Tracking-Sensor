import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

class HandTracker():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    
    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms, handType in zip(self.results.multi_hand_landmarks, self.results.multi_handedness):
                if handType.classification[0].label == 'Left' and draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image
    
    def positionFinder(self, image, draw=True):
        lmlists = [[], []]
        index_finger_tip = None
        thumb_tip = None

        if not self.results.multi_hand_landmarks:
            return []

        for i, Hand in enumerate(self.results.multi_hand_landmarks):
            if i > 1:
                break
            handObj = self.results.multi_handedness
            myHand = handObj[0].classification[0].label
            if (myHand == 'Right'): break
            for id, lm in enumerate(Hand.landmark):
                # if classification == 'Left': break
                # Get the index finger tip and thumb tip positions
                if id == 8:  # Index finger tip
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    index_finger_tip = (cx, cy)
                    lmlists[i].append([id, cx, cy])
                    if draw:
                        cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                elif id == 4:  # Thumb tip
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    thumb_tip = (cx, cy)
                    lmlists[i].append([id, cx, cy])
                    if draw:
                        cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        
        # If both the index finger and thumb were found, draw a line between them
        if index_finger_tip and thumb_tip:
            cv2.line(image, index_finger_tip, thumb_tip, (255, 255, 0), thickness=2)
        
        return lmlists
    