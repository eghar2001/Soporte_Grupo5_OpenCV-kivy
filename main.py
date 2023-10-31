import datetime
import os
from copy import deepcopy
from functools import partial
import mediapipe as mp
import cv2
from deepface import DeepFace
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from custom_components import CameraOpenCv
ruta_imagenes_login = "fotos_login\\"




class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = Builder.load_file("login.kv")
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

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = Builder.load_file("register.kv")
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
        fecha_hora_actual = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        cv2.imwrite(f"{ruta_imagenes_login}{fecha_hora_actual}.jpg",frame)
        print("Usuario creado con exito!!")




class MenuScreen(Screen):
    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = Builder.load_file("menu.kv")
        self.add_widget(layout)
        self.camera_menu = layout.ids.get('camera_menu')
        self.camera_menu.hasFacialRecognition = True
        self.camera_menu.hasHandsRecognition = True

    def on_enter(self):
        self.camera_menu.start_video()

    def on_leave(self):
        self.camera_menu.stop_video()




class MyApp(App):

    def build(self):
        screenManager = Builder.load_file('main.kv')

        #Creamos la pantalla del login
        self.screen_login = LoginScreen()
        self.screen_login.name = "login"
        screenManager.screens.append(self.screen_login)

        #Ponemos la pantalla de register
        self.screen_register = RegisterScreen()
        self.screen_register.name = "register"
        screenManager.screens.append(self.screen_register)

        self.screen_menu = MenuScreen()
        self.screen_menu.name = "menu"
        screenManager.screens.append(self.screen_menu)
        return screenManager






    def ir_al_menu(self):
        if self.screen_login.login_user():
            #self.screen_menu.start_video()
            self.root.current = "menu"












if __name__ == '__main__':
    DeepFace.verify(ruta_imagenes_login + "yo.jpg", ruta_imagenes_login + "yo.jpg", model_name="VGG-Face", detector_backend="ssd")
    MyApp().run()