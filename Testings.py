import numpy as np
import time
import imutils
import cv2

avg = None
cap = cv2.VideoCapture(0)
xvalues = list()
motion = list()
count1 = 0
count2 = 0
counter = 0

def save_img(frame,counter):
    cv2.imwrite('frame ' + str(counter) + '.jpg', frame)
    print('Captured frame num ' + str(counter))



def find_majority(k):
    myMap = {}
    maximum = ('', 0)  # (occurring element, occurrences)
    for n in k:
        if n in myMap:
            myMap[n] += 1
        else:
            myMap[n] = 1

        # Keep track of maximum on the go
        if myMap[n] > maximum[1]: maximum = (n, myMap[n])

    return maximum


while 1:
    (ret, frame) = cap.read()
    flag = True
    text = ""

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        # print(avg)
        continue

    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
    # thresh2 = cv2.adaptiveThreshold(frameDelta, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    # thresh2 = cv2.dilate(thresh2, None, iterations=2)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    for c in contours:

        # print(cv2.contourArea(c))
        if cv2.contourArea(c) < 5000:
            continue

        #counter = counter+1
        #save_img(frame, counter)


        (x, y, w, h) = cv2.boundingRect(c)
        xvalues.append(x)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        flag = False

    no_x = len(xvalues)

    if (no_x > 2):
        difference = xvalues[no_x - 1] - xvalues[no_x - 2]
        if (difference > 0):
            motion.append(1)
        else:
            motion.append(0)

    if flag is True:
        if (no_x > 5):
            val, times = find_majority(motion)
            if val == 1 and times >= 15:
                count1 += 1
            else:
                count2 += 1

        xvalues = list()
        motion = list()

    cv2.line(frame, (260, 0), (260, 480), (0, 255, 0), 2)
    cv2.line(frame, (420, 0), (420, 480), (0, 255, 0), 2)
    cv2.putText(frame, "In: {}".format(count1), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Out: {}".format(count2), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Frame", frame)
    cv2.imshow("Gray", gray)
    cv2.imshow("FrameDelta", frameDelta)
    # cv2.imshow("tresh", thresh)
    # cv2.imshow("tresh2", thresh2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
