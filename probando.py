"""
Es una tarea dada el 24/08
La computadora al reconocer una mano, abre una ventana nueva mostrando unicamente la mano
"""


import cv2
import mediapipe as mp
from deepface import DeepFace

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ruta_imagenes = "K:\\Proyectos\\Python\\opencv-kivy\\fotos_login\\"
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while True:

        ret,frame = cap.read()
        if not ret:
            print("No hay imagen")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        detectado = None
        try:
            detectado = DeepFace.verify(frame,ruta_imagenes+"yo.jpg", model_name="VGG-Face", detector_backend='ssd')
        except Exception :
            pass

        if detectado and detectado["verified"] :
            print(detectado)
            (x_min, y_min )= (detectado['facial_areas']['img1']['x'], detectado['facial_areas']['img1']['y'])
            (x_max, y_max) = (x_min + detectado['facial_areas']['img1']['w'], y_min + detectado['facial_areas']['img1']['h'])
            cv2.rectangle(frame, (x_min,y_min),(x_max, y_max), (0,255,0),10)
            cv2.putText(frame, 'Nahuel',(x_min, y_max+20), cv2.FONT_ITALIC, 1,(255,255,255),2,cv2.LINE_AA)

        cv2.imshow("Image",frame)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()

