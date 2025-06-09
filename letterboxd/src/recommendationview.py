"""
Module implementing the movie recommendation view.
"""

import customtkinter

class RecommendationView(customtkinter.CTkFrame):
    """
    Class representing the movie recommendations view.
    Inherits from customtkinter.CTkFrame.

    :param parent: Parent widget.
    :type parent: customtkinter.CTkBaseClass
    :param controller: Application controller.
    :type controller: App
    :param movie_title: Title of the movie for which recommendations are generated.
    :type movie_title: str
    """

    def __init__(self, parent, controller, movie_title):
        super().__init__(parent)
        self.controller = controller
        self.movie_title = movie_title

        label = customtkinter.CTkLabel(self, text=f"Recommendations for: {movie_title}", font=("Arial", 24, "bold"))
        label.pack(pady=20)

        self.features = {
            'genres': customtkinter.BooleanVar(value=False),
            'keywords': customtkinter.BooleanVar(value=False),
            'cast': customtkinter.BooleanVar(value=False),
            'director': customtkinter.BooleanVar(value=False),
            'overview': customtkinter.BooleanVar(value=False),
            'runtime': customtkinter.BooleanVar(value=False),
        }

        checkbox_frame = customtkinter.CTkFrame(self)
        checkbox_frame.pack(pady=10)

        for feature, var in self.features.items():
            cb = customtkinter.CTkCheckBox(checkbox_frame, text=feature.capitalize(), variable=var)
            cb.pack(anchor="w", padx=10, pady=5)

        generate_button = customtkinter.CTkButton(self, text="Generate Recommendations", command=self.generate_recommendations)
        generate_button.pack(pady=20)

        self.results_frame = customtkinter.CTkScrollableFrame(self, height=400)
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=10)

        back_button = customtkinter.CTkButton(self, text="Back", command=self.go_back)
        back_button.pack(pady=20)

    def generate_recommendations(self):
        """
        Generates and displays movie recommendations based on selected features.
        Clears previous recommendations and displays new results in results_frame.
        If no features are selected or no recommendations are found,
        displays an appropriate message.
        """
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        selected_features = [f for f, var in self.features.items() if var.get()]

        if not selected_features:
            label = customtkinter.CTkLabel(self.results_frame, text="You must select at least one feature!")
            label.pack(pady=10)
            return

        recommendations = self.controller.get_recommendations(self.movie_title, selected_features)

        if not recommendations:
            label = customtkinter.CTkLabel(self.results_frame, text="No recommendations found.")
            label.pack(pady=10)
        else:
            for title, score in recommendations:
                rec_frame = customtkinter.CTkFrame(self.results_frame)
                rec_frame.pack(pady=5, fill="x")

                text = f"{title} (similarity: {score:.2f})"
                rec_label = customtkinter.CTkLabel(rec_frame, text=text, font=("Arial", 16))
                rec_label.pack(side="left", padx=10)

                detail_button = customtkinter.CTkButton(rec_frame, text="Details", width=100,
                                command=lambda m=title: self.controller.show_movie_detail(m))
                detail_button.pack(side="right", padx=10)

    def go_back(self):
        """
        Returns to the movies list view.
        """
        self.controller.show_movies_menu(self.controller.current_user_id)