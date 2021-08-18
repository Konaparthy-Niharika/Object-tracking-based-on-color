# Import the required packages
import imutils
import cv2

# Set upper and lower valued for HSV for red color
whiteLower = (47, 0, 53)
whiteUpper = (179, 255, 255)

# Grab reference to webcam
camera = cv2.VideoCapture(0)

# Keep looping
while True:
    # Grab the current frame
    (grabbed, frame) = camera.read()

    # Resize the frame, blur it and covnert to HSV
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Create a mask for red color
    mask = cv2.inRange(hsv, whiteLower, whiteUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # FId the contours in image
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Initilaize the center
    center = None

    # Check if atleast one contour is found
    if len(contours) > 0:
        # FInd the biggest conotur and find moments and center
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # If radius is greater than 10 draw circle
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            print(center, radius)

            if radius > 250:
                print("stop")
            else:

                # Check if it is right left or center
                if center[0] < 150:
                    text1="Left"
                    print(text1)
                    cv2.putText(frame,text1,(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                elif center[0] > 450:
                    text2="Right"
                    print(text2)
                    cv2.putText(frame,text2,(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                elif radius < 250:
                    text3="Front"
                    print(text3)
                    cv2.putText(frame,text3,(10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                else:
                    print("Stop")

    # Display the current frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("s"):
            cv2.imwrite("screenshot.png", frame)

# Close webcam and close al windows
camera.release()
cv2.destroyAllWindows()
             
