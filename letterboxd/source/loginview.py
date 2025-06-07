import customtkinter


class LoginView(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="Logowanie")
        label.pack(pady=20)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Login")
        self.username_entry.pack(pady=5)

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Hasło", show="*")
        self.password_entry.pack(pady=5)

        login_button = customtkinter.CTkButton(self, text="Zaloguj", command=self.login)
        login_button.pack(pady=10)

        back_button = customtkinter.CTkButton(self, text="Wróć", command=self.controller.show_main_menu)
        back_button.pack(pady=10)

        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, user_id = self.controller.user_manager.login_user(username, password)
        if success:
            self.controller.on_successful_login(username, user_id)
        else:
            self.info_label.configure(text="Niepoprawne dane logowania", text_color="red")
