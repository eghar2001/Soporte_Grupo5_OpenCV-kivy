from copy import deepcopy
from datetime import datetime

import cv2
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import mediapipe as mp
from custom_components import CameraOpenCv
from rutas import ruta_imagenes_login


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = Builder.load_file(".\\screens\\register\\register.kv")
        self.add_widget(layout)
        self.camera_register = layout.ids.get('camera_register')

    def on_enter(self, *args):
        self.camera_register.start_video()
    def on_leave(self, *args):
        self.camera_register.stop_video()
    def register_user(self):
        frame = deepcopy(self.camera_register.frame)
        with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame_rgb)
            if not results.detections:
                print("No hay ninguna cara")
                return False
        fecha_hora_actual = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        cv2.imwrite(f"{ruta_imagenes_login}{fecha_hora_actual}.jpg",frame)
        print("Usuario creado con exito!!")