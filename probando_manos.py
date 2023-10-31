"""
Es una tarea dada el 24/08
La computadora al reconocer una mano, abre una ventana nueva mostrando unicamente la mano
"""


import cv2
import mediapipe as mp
from deepface import DeepFace
from google.protobuf.json_format import MessageToDict

mp_hands_detection = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ruta_imagenes = "K:\\Proyectos\\Python\\opencv-kivy\\fotos_login\\"
with mp_hands_detection.Hands() as hands_detection:
    while True:

        ret,frame = cap.read()
        if not ret:
            print("No hay imagen")
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands_detection.process(frame_rgb)
        height,width,_ = frame.shape
        if results.multi_hand_landmarks is not None:
            # Dibujando los puntos y las conexiones mediante mp_drawing
            for (hand_landmarks, handedness) in zip(results.multi_hand_landmarks,results.multi_handedness ):
                y_1 = int(hand_landmarks.landmark[mp_hands_detection.HandLandmark.WRIST].y*height)
                y_2 = int(hand_landmarks.landmark[mp_hands_detection.HandLandmark.MIDDLE_FINGER_TIP].y*height)
                x_1 = int(hand_landmarks.landmark[mp_hands_detection.HandLandmark.THUMB_TIP].x* width)
                x_2 =int(hand_landmarks.landmark[mp_hands_detection.HandLandmark.PINKY_DIP].x* width)
                cv2.rectangle(frame,(x_1,y_1),(x_2,y_2),(0,255,0),1)

                x_text = min([x_1, x_2])
                y_text = max([y_1, y_2]) + 5
                font = cv2.FONT_HERSHEY_SIMPLEX
                tipo_mano = MessageToDict(handedness)["classification"][0]["label"]

                if tipo_mano == "Right":
                    cv2.putText(frame, 'Derecha', (x_text, y_text), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
                else:
                    cv2.putText(frame, 'Izquierda', (x_text, y_text), font, 1, (0, 255, 255), 2, cv2.LINE_AA)





        cv2.imshow("Image",frame)
        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()

