"""
Module implementing the main menu of the application.
"""

import customtkinter

class MainMenu(customtkinter.CTkFrame):
    """
    Class representing the main menu of the application.
    Inherits from customtkinter.CTkFrame.

    :param parent: Parent widget.
    :type parent: customtkinter.CTkBaseClass
    :param controller: Application controller.
    :type controller: App
    """

    def __init__(self, parent, controller):
        """
        Initializes the main menu of the application.

        Creates navigation buttons for login and registration.
        """
        super().__init__(parent)
        self.controller = controller

        center_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        center_frame.pack(expand=True)

        label = customtkinter.CTkLabel(center_frame, text="Main Menu", font=("Arial", 24, "bold"))
        label.pack(pady=(0, 20))

        login_button = customtkinter.CTkButton(center_frame, text="Login", width=200, height=40,
                                               command=self.controller.show_login)
        login_button.pack(pady=10)

        register_button = customtkinter.CTkButton(center_frame, text="Register",
                                                  width=200, height=40, command=self.controller.show_register)
        register_button.pack(pady=10)
