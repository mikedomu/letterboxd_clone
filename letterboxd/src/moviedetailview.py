"""
Module implementing the movie details view.
"""

import customtkinter
import requests
from PIL import Image, ImageTk
from io import BytesIO
from src.starrating import StarRating


class MovieDetailView(customtkinter.CTkFrame):
    """
    Class representing the movie details view.
    Inherits from customtkinter.CTkFrame.

    :param parent: Parent widget.
    :type parent: customtkinter.CTkBaseClass
    :param controller: Application controller.
    :type controller: App
    :param movie_title: Movie title.
    :type movie_title: str
    :param user_id: ID of the logged-in user.
    :type user_id: int
    """

    def __init__(self, parent, controller, movie_title, user_id):
        """
        Initializes the movie details view and builds its layout.

        :param parent: Parent widget.
        :type parent: customtkinter.CTkBaseClass
        :param controller: Application controller.
        :type controller: App
        :param movie_title: Movie title.
        :type movie_title: str
        :param user_id: ID of the logged-in user.
        :type user_id: int
        """
        super().__init__(parent)
        self.controller = controller
        self.user_id = user_id
        self.movie_title = movie_title

        movie_data = self.controller.database.get_movie_details(movie_title)
        if not movie_data:
            label = customtkinter.CTkLabel(self, text="Movie data not found")
            label.pack()
            return

        self.parse_movie_data(movie_data)
        self.build_layout()

    def parse_movie_data(self, movie_data):
        """
        Parses movie data from the database into class attributes.

        :param movie_data: Tuple containing movie data.
        :type movie_data: tuple
        """
        (self.movie_id, self.title, self.genres, self.keywords, self.original_language, self.overview,
         self.production_companies, self.runtime, self.cast, self.director) = movie_data

    def build_layout(self):
        """
        Builds the main layout of the movie details view.
        """
        self.scroll_frame = customtkinter.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.content_frame = customtkinter.CTkFrame(self.scroll_frame)
        self.content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=3)

        self.build_header_section()
        self.build_overview()
        self.build_rating()

    def build_header_section(self):
        """
        Builds the header section with basic movie information.
        """
        poster_url = self.get_poster_url(self.title)
        if poster_url:
            try:
                response = requests.get(poster_url)
                img_data = BytesIO(response.content)
                img = Image.open(img_data).resize((300, 450))
                photo = customtkinter.CTkImage(light_image=img, size=(300, 450))
                poster_label = customtkinter.CTkLabel(self.content_frame, image=photo,text="")
                poster_label.image = photo
                poster_label.grid(row=0, column=0, rowspan=5, padx=10)
            except:
                pass

        title_label = customtkinter.CTkLabel(self.content_frame, text=self.title, font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=1, sticky="w", pady=(15, 10))

        genres_label = customtkinter.CTkLabel(self.content_frame, text=f"Genres: {self.genres}", wraplength=600)
        genres_label.grid(row=1, column=1, sticky="w", pady=5)

        runtime_label = customtkinter.CTkLabel(self.content_frame, text=f"Runtime: {self.runtime} min", )
        runtime_label.grid(row=2, column=1, sticky="w", pady=5)

        director_label = customtkinter.CTkLabel(self.content_frame, text=f"Director: {self.director}",)
        director_label.grid(row=3, column=1, sticky="w", pady=5)

        cast_label = customtkinter.CTkLabel(self.content_frame, text=f"Cast: {self.cast}", wraplength=600)
        cast_label.grid(row=4, column=1, sticky="w", pady=5)

    def build_overview(self):
        """
        Builds the movie overview section.
        """
        overview_title = customtkinter.CTkLabel(self.scroll_frame, text="Overview:", font=("Arial", 16, "bold"))
        overview_title.pack(pady=(10, 0))

        overview_text = customtkinter.CTkLabel(self.scroll_frame, text=self.overview, wraplength=700, justify="left")
        overview_text.pack(pady=5, padx=20)

    def build_rating(self):
        """
        Builds the movie rating section with the rating widget.
        """
        rating_label = customtkinter.CTkLabel(self.scroll_frame, text="Your Rating:", font=("Arial", 14))
        rating_label.pack(pady=10)

        current_rating = self.controller.rating_manager.get_rating(self.user_id, self.movie_id)
        self.star_widget = StarRating(self.scroll_frame, initial_rating=current_rating)
        self.star_widget.pack(pady=5)

        save_button = customtkinter.CTkButton(self.scroll_frame, text="Save Rating", command=self.save_rating)
        save_button.pack(pady=10)

        back_button_main = customtkinter.CTkButton(self.scroll_frame, text="Back to Menu", command=self.go_back_main)
        back_button_main.pack(pady=10)

    def save_rating(self):
        """
        Saves the movie rating and returns to the movies list view.
        """
        rating = self.star_widget.get_rating()
        if rating > 0:
            self.controller.rating_manager.add_or_update_rating(self.user_id, self.movie_id, rating)
            self.controller.show_movies_menu(self.user_id)

    def get_poster_url(self, title):
        """
        Retrieves the movie poster URL from the TMDB API.

        :param title: Movie title.
        :type title: str
        :return: Movie poster URL or None if not found.
        :rtype: str or None
        """
        api_key = "540192c1f16471866e68fcadc8bfaf28"
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(url)
        data = response.json()
        if data["results"]:
            poster_path = data["results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None

    def go_back_main(self):
        """
        Returns to the movies list view.
        """
        self.controller.show_movies_menu(self.user_id)
