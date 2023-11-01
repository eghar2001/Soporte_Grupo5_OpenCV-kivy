import os
from copy import deepcopy

import cv2
from deepface import DeepFace
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

import mediapipe as mp
from custom_components import CameraOpenCv
from rutas import ruta_imagenes_login


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = Builder.load_file(".\\screens\\login\\login.kv")
        self.add_widget(layout)
        self.camera_login = layout.ids.get('camera_login')


    def on_enter(self, *args):
        self.camera_login.start_video()
    def on_leave(self, *args):
        self.camera_login.stop_video()

    def login_user(self):

        frame = deepcopy(self.camera_login.frame)

        with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame_rgb)

            if not results.detections:
                print("No hay ninguna cara")
                return False

        file_list = os.listdir(ruta_imagenes_login)


        image_files = [file for file in file_list if file.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
        for image in image_files:
            detectado = None
            try:
                detectado = DeepFace.verify(frame, ruta_imagenes_login + image, model_name="VGG-Face", detector_backend="ssd")
            except Exception:
                pass


            if detectado and detectado["verified"]:
                print("Estas logueado correctamente")
                return True

        print("No pudimos identificarte")
        return False
