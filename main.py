from deepface import DeepFace
from kivy.app import App
from kivy.lang import Builder

from rutas import ruta_imagenes_login
from screens.login.login import LoginScreen
from screens.register.register import RegisterScreen
from screens.menu.menu import MenuScreen
from screens.archivos.archivos import ArchivosScreen


class MyApp(App):

    def build(self):
        screenManager = Builder.load_file('main.kv')

        #Creamos las pantallas
        self.screen_login = LoginScreen()
        self.screen_login.name = "login"
        screenManager.screens.append(self.screen_login)
#
        #Ponemos la pantalla de register
        self.screen_register = RegisterScreen()
        self.screen_register.name = "register"
        screenManager.screens.append(self.screen_register)
#
        self.screen_menu = MenuScreen()
        self.screen_menu.name = "menu"
        screenManager.screens.append(self.screen_menu)

        self.screen_archivos = ArchivosScreen()
        self.screen_archivos.name = "archivos"
        screenManager.screens.append(self.screen_archivos)

        return screenManager
    def ir_al_menu(self):
        if self.screen_login.login_user():
            self.root.current = "menu"












if __name__ == '__main__':
    #Ejecucion del deepface de prueba para que cargue la libreria al inicio y no cuando se esta ejecutando la aplicacion

    DeepFace.verify(ruta_imagenes_login + "yo.jpg", ruta_imagenes_login + "yo.jpg", model_name="VGG-Face", detector_backend="ssd")
    MyApp().run()