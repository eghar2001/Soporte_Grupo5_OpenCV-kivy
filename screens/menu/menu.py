from copy import deepcopy
from datetime import datetime

import cv2
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from custom_components import CameraOpenCv
from rutas import ruta_imagenes


class MenuScreen(Screen):
    def __init__(self,**kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        layout = Builder.load_file(".\\screens\\menu\\menu.kv")
        self.add_widget(layout)
        self.camera_menu = layout.ids.get('camera_menu')
        self.camera_menu.hasFacialRecognition = True
        self.camera_menu.hasHandsRecognition = True


        self._seconds_left_hand = 0
        self._mano_derecha_levantada_anterior = False
        self._update_time = 1/2
        self._imagen_valida = True
        self._scheduleValidar = None
        self._scheduleLeftHand = None
        self._scheduleRightHand = None


    def on_enter(self):
        self.camera_menu.start_video()
        self._scheduleUpdate = Clock.schedule_interval(self._update, self._update_time)

    def on_leave(self):
        self.camera_menu.stop_video()
        if self._scheduleUpdate:
            self._scheduleUpdate.cancel()
        cv2.destroyAllWindows()

    def _reset(self):
        self._seconds_left_hand = 0
        self._mano_derecha_levantada_anterior = False

    def _update(self, *args):
        if self.camera_menu.hasRightHands() and self.camera_menu.hasLeftHands():
            self._reset()
            print("No se pueden tener ambas manos a la vez")
            return
        if not self.camera_menu.hasFaces():
            self._reset()
            print("Debe haber al menos una cara")
            return
        mano_derecha_levantada = self.camera_menu.hasRightHands()
        mano_izquierda_levantada  = self.camera_menu.hasLeftHands()
        if mano_izquierda_levantada:
            if self._seconds_left_hand % 1 == 0:
                print(f"Faltan {5 - self._seconds_left_hand} segundos para tomar una foto")
            if 0 <= self._seconds_left_hand < 5 :
                self._seconds_left_hand += self._update_time
            elif (self._seconds_left_hand >= 5):
                fecha_hora_actual = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                foto = deepcopy(self.camera_menu.frame)
                cv2.imwrite(f"{ruta_imagenes}{fecha_hora_actual}.jpg", self.camera_menu.frame)
                print("Se ha tomado una foto!")
                cv2.imshow("Foto", foto)
                self._seconds_left_hand = 0
        else:
            self._seconds_left_hand = 0


        if not self._mano_derecha_levantada_anterior and mano_derecha_levantada:
            print("Se empezó a grabar")
            self.camera_menu.start_recording()
        if self._mano_derecha_levantada_anterior and not mano_derecha_levantada:
            print("Se dejo de grabar")
            self.camera_menu.stop_recording()
        self._mano_derecha_levantada_anterior = mano_derecha_levantada











