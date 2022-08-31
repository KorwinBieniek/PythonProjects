import cv2

cap = cv2.VideoCapture("input_videos/bridge.mp4")

if cap.isOpened() == False:
    print('Error opening a video file')

while cap.isOpened():
    ret, frame = cap.read()
    if ret != True:
        break

    cv2.imshow('Frame', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        print('Closing the video')
        break

cap.release()

cv2.destroyAllWindows()