# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

from typing import Callable
import customtkinter
import logging
import os
from components import ProjectPage
from sync import SyncSchema


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
print('Log saved in: ' + os.path.dirname(os.path.abspath(__file__)) + '/sync.log')
logging.basicConfig(filename=f'{os.path.dirname(os.path.abspath(__file__))}/sync.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

class App():
    def __init__(self, setup_content: Callable = None):
        self.app = customtkinter.CTk()
        self.setup_content = setup_content
        customtkinter.set_appearance_mode("Light")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.app.wm_title('Hygraph Share Script')
        self.app.geometry("1000x450")
    def run(self):
        self.setup_content(app=self.app)
        self.app.mainloop()

def setup_content(app):
    page = ProjectPage(master=app, submit_command=SyncSchema)
    page.grid(row=0, column=0, columnspan=1, padx=3, pady=3, sticky="new")

App(setup_content).run()