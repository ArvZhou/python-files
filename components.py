from typing import Callable
import customtkinter
from tkinter import filedialog
from utils import get_json

class Input(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 500,
                 height: int = 60,
                 input_value: str = '',
                 command: Callable = None,
                 label_text: str = '',
                 placeholder_text: str = '',
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.input_value = input_value
        self.command = command

        self.configure(fg_color=("transparent"))  # set frame color

        customtkinter.CTkLabel(
            master=self,
            text=f'{label_text}:',
            text_color='#999',
            width=150,
            height=30,
            anchor='e',
            font=('Arial', 12)
        ).grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.entry =  customtkinter.CTkEntry(
            master=self,
            placeholder_text_color='#999',
            text_color='#000',
            width=300,
            height=35,
            border_width=1,
            border_color="#999",
            placeholder_text=placeholder_text,
            font=('Arial', 12)
        )
        self.entry.grid(row=0, column=2, padx=(0, 3), pady=3)

    def get(self) -> str:
        try:
            return self.entry.get()
        except ValueError:
            return None

class ProjectInfoForm(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 1000,
                 height: int = 200,
                 command: Callable = None,
                 title: str = '',
                 is_share: bool = False,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)


        self.form_value = {}
        self.command = command
        self.is_share = is_share
        self.configure(fg_color=("transparent"))  # set frame color

        label = customtkinter.CTkLabel(self, text=title, text_color='#000', width=500, height=30, anchor='w', font=('Arial', 14, 'bold'))
        label.grid(row=0, column=0, columnspan=1, padx=3, pady=5, sticky="nw")

        self.project_id_input = Input(self, label_text="Project ID", placeholder_text="Input Project ID")
        self.project_id_input.grid(row=1, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        self.environment_input = Input(self, label_text="Environment", placeholder_text="Input Environment")
        self.environment_input.grid(row=1, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.token_input = Input(self, label_text="Token", placeholder_text="Input Token")
        self.token_input.grid(row=2, column=0, columnspan=1, padx=3, pady=3, sticky="ew")

        self.url_input = Input(self, label_text="Management URL", placeholder_text="Input Management URL")
        self.url_input.grid(row=2, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        if (is_share):
            self.model_name_input = Input(self, label_text="Model or Component Name", placeholder_text="Input Model or Component Name")
            self.model_name_input.grid(row=5, column=0, columnspan=1, padx=3, pady=3, sticky="ew")
    
    def get(self) -> dict:
        self.form_value['PROJECT_ID'] = self.project_id_input.get()
        self.form_value['ENVIRONMENT'] = self.environment_input.get()
        self.form_value['TOKEN'] = self.token_input.get()
        self.form_value['MANAGEMENT_URL'] = self.url_input.get()
        if (self.is_share):
            self.form_value['MODEL_NAME'] = self.model_name_input.get()
        return self.form_value
    def set(self, form_value):
        self.project_id_input.entry.insert(0, form_value['PROJECT_ID'])
        self.environment_input.entry.insert(0, form_value['ENVIRONMENT'])
        self.token_input.entry.insert(0, form_value['TOKEN'])
        self.url_input.entry.insert(0, form_value['MANAGEMENT_URL'])
        if (self.is_share):
            self.model_name_input.entry.insert(0, form_value['MODEL_NAME'])

class ProjectPage(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 1000,
                 height: int = 600,
                 submit_command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(fg_color=("transparent"))
        self.submit_command = submit_command
        self.share_project_form = ProjectInfoForm(master=self, title='Share Project Info', is_share=True)
        self.share_project_form.grid(row=0, column=0, columnspan=1, padx=3, pady=3, sticky="new")

        self.target_project_form = ProjectInfoForm(master=self, title='Targrt Project Info')
        self.target_project_form.grid(row=1, column=0, columnspan=1, padx=3, pady=3, sticky="new")

        frame = customtkinter.CTkFrame(master=self, width=1000, height=70, fg_color="transparent")
        frame.grid(row=2, column=0, columnspan=2, padx=3, pady=30, sticky="ew")

        button = customtkinter.CTkButton(master=frame, text="Submit", command=self.submit, width=200)
        button.place(relx=0.5, rely=0.5, anchor='center')

        button = customtkinter.CTkButton(master=self, text="Import Project Infomation", command=self.choose_file, width=200)
        button.place(x=765, y=15, anchor='w')
    def choose_file(self):
        file_name = filedialog.askopenfilename()
        default_json = get_json(file_name)
        self.share_project_form.set(default_json['SHARE_PROJECT'])
        self.target_project_form.set(default_json['TARGET_PROJECT'])

    def submit(self) -> None:
        self.submit_command(project_info={
            'share': self.share_project_form.get(),
            'target': self.target_project_form.get()
        })