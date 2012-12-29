import cv
HAAR_CASCADE_PATH = 'palm.xml' 

def detect_faces(frame):
    faces = []
    detected = cv.HaarDetectObjects(frame, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100, 100))
    
    if detected:
        for (x, y, w, h), n in detected:
            faces.append((x,y,w,h))

    return faces

if __name__ == '__main__':
    cv.NamedWindow("video")
    capture = cv.CaptureFromCAM(-1)
    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []

    i = 0
    while True:
        frame = cv.QueryFrame(capture)
        if i % 5 == 0:
            faces = detect_faces(frame)
        for (x,y,w,h) in faces:
            cv.Rectangle(frame, (x,y), (x+w, y+h), 255)

        cv.ShowImage("video", frame)
        c = cv.WaitKey(10)
        if c != -1:
            break
        i += 1
