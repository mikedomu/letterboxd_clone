"""
Main application module responsible for user interface management.
"""

import customtkinter
from src.database import Database
from src.mainmenu import MainMenu
from src.moviedetailview import MovieDetailView
from src.recommendationview import RecommendationView
from src.usermanager import UserManager
from src.loginview import LoginView
from src.registerview import RegisterView
from src.mainview import MainView
from src.ratingmanager import RatingManager
from src.recommender import Recommender


class App(customtkinter.CTk):
    """
    Main application class managing user interface and navigation.
    Inherits from customtkinter.CTk.
    """

    def __init__(self):
        """
        Initializes the main application window and all necessary components.
        """
        super().__init__()
        self.center_window(1000, 500)
        self.title("Review movie app")

        # Inicjalizacja bazy danych i połączenia
        self.database = Database(csv_path="data/dataset.csv")
        self.database.create_connection()
        self.database.create_tables()
        self.database.insert_movies_data_if_needed()

        self.user_manager = UserManager(self.database.cursor, self.database.conn)
        self.rating_manager = RatingManager(self.database.cursor, self.database.conn)
        self.recommender = Recommender(self.database)

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    def show_main_menu(self):
        """
        Displays the main menu of the application.
        """
        self.clear_container()
        MainMenu(self.container, self).pack(fill="both", expand=True)

    def show_login(self):
        """
        Displays the login screen.
        """
        self.clear_container()
        LoginView(self.container, self).pack(fill="both", expand=True)

    def show_register(self):
        """
        Displays the registration screen.
        """
        self.clear_container()
        RegisterView(self.container, self).pack(fill="both", expand=True)

    def show_movies_menu(self, user_id):
        """
        Displays the movies menu.

        :param user_id: ID of the logged-in user.
        :type user_id: int
        """
        self.clear_container()
        MainView(self.container, self, self.current_username, user_id).pack(fill="both", expand=True)

    def on_successful_login(self, username, user_id):
        """
        Handles successful user login.

        :param username: Username of the logged-in user.
        :type username: str
        :param user_id: ID of the logged-in user.
        :type user_id: int
        """
        self.current_username = username
        self.current_user_id = user_id
        self.clear_container()
        MainView(self.container, self, username, user_id).pack(fill="both", expand=True)

    def show_movie_detail(self, movie_title, came_from_recommendation=False):
        """
        Displays details of the selected movie.

        :param movie_title: Title of the movie.
        :type movie_title: str
        :param came_from_recommendation: Whether view was called from recommendations.
        :type came_from_recommendation: bool
        """
        self.clear_container()
        MovieDetailView(self.container, self, movie_title, self.current_user_id).pack(fill="both", expand=True)

    def show_recommendation(self, movie_title):
        """
        Displays recommendations for the selected movie.

        :param movie_title: Title of the movie.
        :type movie_title: str
        """
        self.clear_container()
        RecommendationView(self.container, self, movie_title).pack(fill="both", expand=True)

    def get_recommendations(self, movie_title, selected_features):
        """
        Retrieves recommendations for the selected movie.

        :param movie_title: Title of the movie.
        :type movie_title: str
        :param selected_features: List of selected features for analysis.
        :type selected_features: list
        :return: List of recommended movies.
        :rtype: list
        """
        return self.recommender.recommend(movie_title, selected_features)

    def clear_container(self):
        """
        Clears the content of the main window container.
        """
        for widget in self.container.winfo_children():
            widget.destroy()

    def center_window(self, width, height):
        """
        Centers the application window on the screen.

        :param width: Window width.
        :type width: int
        :param height: Window height.
        :type height: int
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
