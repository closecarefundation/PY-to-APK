# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary scri"pt file.
"""



# main.py

import pandas as pd
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from datetime import datetime, time
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.uix.list import ThreeLineListItem
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
import re
from github import Github
from io import BytesIO
import requests
from kivy.core.image import Image as CoreImage
from kivy.uix.image import AsyncImage

# Tu nombre de usuario de GitHub y tu token de acceso personal
username = 'closecare'
token = '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'

width = Window.width
height = Window.height

Window.jeyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = 'below_target'
Window.fullscreen = 'auto'



class LoginScreen(MDScreen):
    image_source = StringProperty('')
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Login Screen'))
        g = Github(token)

        # Obtiene el repositorio por nombre
        repo = g.get_user().get_repo('PY-to-APK')


        content = repo.get_contents("closecare.xlsx")

        # Lee el contenido del archivo Excel
        excel_content = content.decoded_content

        # Por ejemplo, para listar los archivos en la raíz del repositorio
        with BytesIO(excel_content) as b:
            sheet = pd.read_excel(b, 'familiar')
            
        self.sheet = sheet.set_index(sheet.columns[0]).to_dict('index')
        
        content = repo.get_contents("logo.png")

        # Lee el contenido del archivo Excel
        png_url = content.download_url

        # Crea un widget de imagen Kivy y asigna la textura
        self.image_widget = AsyncImage(source=png_url, size_hint_y=0.4, pos_hint={'center_y': 0.85})
        self.add_widget(self.image_widget)
    
    def log_out(self):
        self.ids.username_input.text = ''
        self.ids.password_input.text = ''
        
    def validate_user(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        # Lógica de validación de inicio de sesión
        # excel = pd.ExcelFile("C:/Users/Adria/Downloads/closecare.xlsx")
        # sheet = pd.read_excel(excel, 'familiar')
        
        # Crea una instancia de la clase Github con tu token de acceso personal
        if username in self.sheet.keys():
            if password == self.sheet[username]['Password']:
                app = MDApp.get_running_app()
                app.username = username
                self.manager.current = 'menu'  # Cambiar a la pantalla del menú principal
            else:
                self.ids.info_label.text = 'Contraseña incorrecta'
        else:
            self.ids.info_label.text = 'DNI incorrecto'
            
    def toggle_password_visibility(self):
        password_input = self.ids.password_input
        password_input.password = not password_input.password


class MyApp(MDApp):
    username = StringProperty('')
    width = NumericProperty(Window.width)
    height = NumericProperty(Window.height)

    def build(self):
        Builder.load_file('mi_app.kv')
        
        sm = ScreenManager()

        sm.add_widget(LoginScreen(name='login'))

        return sm
    
    def callback(self):
        pass

    
if __name__ == '__main__':
    MyApp().run()

    
        