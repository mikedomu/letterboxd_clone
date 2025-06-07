import customtkinter
from database import Database
from mainmenu import MainMenu
from moviedetailview import MovieDetailView
from usermanager import UserManager
from loginview import LoginView
from registerview import RegisterView
from moviesview import MoviesView
from ratingmanager import RatingManager

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.center_window(1000, 500)
        self.title("Review movie")
        self.database = Database(csv_path="dataset.csv")
        self.database.create_connection()
        self.database.create_tables()
        self.database.insert_movies_data_if_needed()

        self.user_manager = UserManager(self.database.cursor, self.database.conn)
        self.rating_manager = RatingManager(self.database.cursor, self.database.conn)
        self._set_appearance_mode("dark")

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    def show_main_menu(self):
        self.clear_container()
        MainMenu(self.container, self).pack(fill="both", expand=True)

    def show_login(self):
        self.clear_container()
        LoginView(self.container, self).pack(fill="both", expand=True)

    def on_successful_login(self, username, user_id):
        self.current_username = username
        self.current_user_id = user_id
        self.clear_container()
        MoviesView(self.container, self, username, user_id).pack(fill="both", expand=True)

    def show_register(self):
        self.clear_container()
        RegisterView(self.container, self).pack(fill="both", expand=True)

    def show_movie_detail(self, movie_title):
        self.clear_container()
        MovieDetailView(self.container, self, movie_title, self.current_user_id).pack(fill="both", expand=True)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_movies_menu(self, user_id):
        self.clear_container()
        MoviesView(self.container, self, self.current_username, user_id).pack(fill="both", expand=True)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = App()
    app.mainloop()