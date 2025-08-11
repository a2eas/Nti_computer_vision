import cv2




def detect_faces(image):
    # Initialize the MTCNN face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)


    print(faces)
    # Show the result
    return len(faces),image


