import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

class ArchivosScreen(Screen):
    def __init__(self,**kwargs):
        super(ArchivosScreen, self).__init__(**kwargs)
        layout = Builder.load_file(".\\screens\\archivos\\archivos.kv")
        file_chooser = layout.ids["filechooser"]

        file_chooser.rootpath = "."
        self.add_widget(layout)

        def on_selection(instance, selection):
            if selection:
                #Solo windows
                # En sistemas basados en unix hay que cambiar el metodo por os.system(f'xdg-open "{ruta_imagen}"')
                os.startfile(selection[0])
        file_chooser.bind(selection = on_selection)