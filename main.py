# -*- coding: UTF-8 -*-
__author__ = 'arvin.zhou'

from typing import Callable
from sync import get_models, create_new_model
import customtkinter
from components import ProjectInfoForm

def start_window(generate_content):
    app = customtkinter.CTk()
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    app.wm_title('Hygraph Share')
    app.geometry("1050x400")
    generate_content(app)
    app.mainloop()

def generate_content(app):
    def form_command():
        print(share_project_form.get())
        print(target_project_form.get())

    share_project_form = ProjectInfoForm(master=app, command=form_command, title='Share Project Info', is_share=True)
    share_project_form.grid(row=0, column=0, columnspan=1, padx=3, pady=3, sticky="new")

    target_project_form = ProjectInfoForm(master=app, command=form_command, title='Targrt Project Info')
    target_project_form.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="new")

    frame = customtkinter.CTkFrame(master=app, width=800, height=70, fg_color="transparent")
    frame.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky="ew")

    button = customtkinter.CTkButton(master=frame, text="Submit", command=form_command, width=200)
    button.place(relx=0.5, rely=0.5, anchor='center')

start_window(generate_content)