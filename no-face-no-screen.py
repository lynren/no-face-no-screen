import time
import os
import cv2

# load cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# capture input from camera
cap = cv2.VideoCapture(0)

# amount of consecutive seconds w/ no face for screen shutoff
SCREEN_ON_THRESHOLD = 10
# amount of consevutive seconds w/ face for screen turn on
SCREEN_OFF_THRESHOLD = 3
# consecutive seconds with no face counter
no_face_timer = 0
# consective seconds with face counter
face_timer = 0
screen_off = False

print("Started program at: %s" % time.strftime("%H:%M:%S"))

while True:
    # read in a frame
    _, img = cap.read()
    # convert to grayscale (facial recog only works with grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # if no faces found
    if len(faces) == 0:
        face_timer = 0
        no_face_timer = no_face_timer + 1

        # if no face for > SCREEN_ON_THRESHOLD seconds
        if no_face_timer > SCREEN_ON_THRESHOLD and not screen_off:
            print("shutting off at: %s" % time.strftime("%H:%M:%S"))
            no_face_timer = 0
            screen_off = True
            os.system("xset dpms force off")
        time.sleep(1)

    # if face found, but screen is off
    elif screen_off:
        no_face_timer = 0
        face_timer = face_timer + 1

        # if face found for > SCREEN_OFF_THRESHOLD seconds
        if face_timer > SCREEN_OFF_THRESHOLD:
            print("turning on at: %s" % time.strftime("%H:%M:%S"))
            face_timer = 0
            screen_off = False
            os.system("xset dpms force on")
            os.system("xdotool mousemove 0 0 mousemove restore")
        time.sleep(1)
    else:
        time.sleep(10)

cap.release()
