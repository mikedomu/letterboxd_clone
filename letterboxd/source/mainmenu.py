import customtkinter

class MainMenu(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        center_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True)

        label = customtkinter.CTkLabel(center_frame, text="Menu główne", font=("Arial", 24, "bold"))
        label.pack(pady=(0, 20))

        login_button = customtkinter.CTkButton(center_frame, text="Logowanie", width=200, height=40, command=self.controller.show_login)
        login_button.pack(pady=10)

        register_button = customtkinter.CTkButton(center_frame, text="Rejestracja", width=200, height=40, command=self.controller.show_register)
        register_button.pack(pady=10)
