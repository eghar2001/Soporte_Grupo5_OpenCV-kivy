"""
Es una tarea dada el 24/08
La computadora al reconocer una mano, abre una ventana nueva mostrando unicamente la mano
"""


import cv2
import mediapipe as mp
from deepface import DeepFace
from google.protobuf.json_format import MessageToDict

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ruta_imagenes = "K:\\Proyectos\\Python\\opencv-kivy\\fotos_login\\"
with mp_face_detection.FaceDetection() as face_detection:
    while True:

        ret,frame = cap.read()
        if not ret:
            print("No hay imagen")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        height,width,_ = frame.shape
        if results.detections:
            for detection in results.detections:
                xmin = int(detection.location_data.relative_bounding_box.xmin*width)
                ymin = int(detection.location_data.relative_bounding_box.ymin*height)
                xmax = xmin + int(detection.location_data.relative_bounding_box.width * width)
                ymax = xmin + int(detection.location_data.relative_bounding_box.height * height)
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'Cara', (xmin, ymax), font, 1, (0, 255, 255), 2, cv2.LINE_AA)





        cv2.imshow("Image",frame)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()

