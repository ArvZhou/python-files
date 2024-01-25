from types import UnionType
from typing import Callable, Union
import customtkinter

class Input(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 800,
                 height: int = 70,
                 input_value: str = '',
                 command: Callable = None,
                 label_text: str = '',
                 placeholder_text: str = '',
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.input_value = input_value
        self.command = command

        self.configure(fg_color=("transparent"))  # set frame color

        label = customtkinter.CTkLabel(master=self, text=label_text, text_color='#999', width=180, height=30, anchor='e')
        label.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.entry =  customtkinter.CTkEntry(master=self, text_color='#000', width=300, height=35, border_width=1, border_color="#999", placeholder_text=placeholder_text)
        self.entry.grid(row=0, column=2, padx=(0, 3), pady=3)

    def get(self) -> str:
        try:
            return self.entry.get()
        except ValueError:
            return None

class ProjectInfoForm(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 800,
                 height: int = 70,
                 command: Callable = None,
                 title: str = '',
                 is_share: bool = False,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)


        self.form_value = {}
        self.command = command
        self.is_share = is_share
        self.configure(fg_color=("transparent"))  # set frame color

        label = customtkinter.CTkLabel(self, text=title, text_color='#000', width=500, height=50, anchor='center', font=('Arial', 16, 'bold'))
        label.grid(row=0, column=0, columnspan=1, padx=3, pady=5, sticky="nw")

        self.project_id_input = Input(self, label_text="Project ID", placeholder_text="Input Project ID")
        self.project_id_input.grid(row=1, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        self.environment_input = Input(self, label_text="Environment", placeholder_text="Input Environment")
        self.environment_input.grid(row=2, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        self.token_input = Input(self, label_text="Token", placeholder_text="Input Token")
        self.token_input.grid(row=3, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        self.url_input = Input(self, label_text="Management URL", placeholder_text="Input Management URL")
        self.url_input.grid(row=4, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        if (is_share):
            self.model_name_input = Input(self, label_text="Model or Component Name", placeholder_text="Input Model or Component Name")
            self.model_name_input.grid(row=5, column=0, columnspan=1, padx=3, pady=3, sticky="ew")
    
    def get(self) -> dict:
        print(self.form_value)
        self.form_value['PROJECT_ID'] = self.project_id_input.get()
        self.form_value['ENVIRONMENT'] = self.environment_input.get()
        self.form_value['TOKEN'] = self.token_input.get()
        self.form_value['MANAGEMENT_URL'] = self.url_input.get()
        if (self.is_share):
            self.form_value['MODEL_NAME'] = self.model_name_input.get()
        return self.form_value
