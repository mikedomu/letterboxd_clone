"""
Module implementing the login view.
"""

import customtkinter


class LoginView(customtkinter.CTkFrame):
    """
    Class representing the user login view.
    Inherits from customtkinter.CTkFrame.

    :param parent: Parent widget.
    :type parent: customtkinter.CTkBaseClass
    :param controller: Application controller.
    :type controller: App
    """

    def __init__(self, parent, controller):
        """
        Initializes the login view, creating all necessary widgets.
        """
        super().__init__(parent)
        self.controller = controller

        label = customtkinter.CTkLabel(self, text="Login")
        label.pack(pady=20)

        self.username_entry = customtkinter.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=5)

        self.password_entry = customtkinter.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=5)

        login_button = customtkinter.CTkButton(self, text="Login", command=self.login)
        login_button.pack(pady=10)

        back_button = customtkinter.CTkButton(self, text="Back", command=self.controller.show_main_menu)
        back_button.pack(pady=10)

        self.info_label = customtkinter.CTkLabel(self, text="")
        self.info_label.pack(pady=5)

    def login(self):
        """
        Handles the user login process.

        Verifies login credentials and redirects the user to the movies view
        upon success. In case of an error, displays an invalid credentials message.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, user_id = self.controller.user_manager.login_user(username, password)
        if success:
            self.controller.on_successful_login(username, user_id)
        else:
            self.info_label.configure(text="Invalid login credentials", text_color="red")
