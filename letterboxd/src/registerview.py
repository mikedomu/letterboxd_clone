"""
Moduł implementujący widok rejestracji.
"""

import customtkinter


class RegisterView(customtkinter.CTkFrame):
    """
    Klasa reprezentująca widok rejestracji użytkownika.
    Dziedziczy po customtkinter.CTkFrame.

    :param parent: Widget nadrzędny.
    :type parent: customtkinter.CTkBaseClass
    :param controller: Kontroler aplikacji.
    :type controller: App
    """

    def __init__(self, parent, controller):
        """
        Inicjalizuje widok rejestracji użytkownika.

        Tworzy pola formularza rejestracji oraz przyciski do rejestracji i powrotu do menu.
        """
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="Registration")
        label.pack(pady=20)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Login")
        self.username_entry.pack(pady=5)

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        register_button = customtkinter.CTkButton(self, text="Register", command=self.register)
        register_button.pack(pady=10)

        back_button = customtkinter.CTkButton(self, text="Back", command=self.controller.show_main_menu)
        back_button.pack(pady=10)

        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.pack(pady=5)

    def register(self):
        """
        Obsługuje proces rejestracji użytkownika.

        Pobiera dane z formularza, przekazuje je do kontrolera, a następnie
        wyświetla komunikat o sukcesie lub błędzie rejestracji.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.controller.user_manager.register_user(username, password)
            self.info_label.configure(text="Rejestracja udana!", text_color="green")
        except:
            self.info_label.configure(text="Błąd rejestracji!", text_color="red")
