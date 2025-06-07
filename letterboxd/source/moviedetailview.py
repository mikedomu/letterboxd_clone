import customtkinter
import requests
from PIL import Image, ImageTk
from io import BytesIO
from starrating import StarRating

class MovieDetailView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, movie_title, user_id):
        super().__init__(parent)
        self.controller = controller
        self.user_id = user_id
        self.movie_title = movie_title

        movie_data = self.controller.database.get_movie_details(movie_title)
        if not movie_data:
            label = customtkinter.CTkLabel(self, text="Nie znaleziono danych filmu")
            label.pack()
            return

        self.parse_movie_data(movie_data)
        self.build_layout()

    def parse_movie_data(self, movie_data):
        (self.movie_id, self.title, self.genres, self.keywords, self.original_language, self.overview,
         self.production_companies, self.runtime, self.cast, self.director) = movie_data

    def build_layout(self):
        self.scroll_frame = customtkinter.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.content_frame = customtkinter.CTkFrame(self.scroll_frame)
        self.content_frame.pack(padx=20, pady=20, fill="both", expand=True)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=3)

        self.build_header_section()
        self.build_overview_section()
        self.build_rating_section()

    def build_header_section(self):
        poster_url = self.get_poster_url(self.title)
        if poster_url:
            try:
                response = requests.get(poster_url)
                img_data = BytesIO(response.content)
                img = Image.open(img_data).resize((300, 450))
                photo = customtkinter.CTkImage(light_image=img, size=(300, 450))
                poster_label = customtkinter.CTkLabel(self.content_frame, image=photo, text="")
                poster_label.image = photo
                poster_label.grid(row=0, column=0, rowspan=5, sticky="n", padx=10)
            except:
                pass

        title_label = customtkinter.CTkLabel(self.content_frame, text=self.title, font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=1, sticky="w", pady=(0, 10))

        genres_label = customtkinter.CTkLabel(self.content_frame, text=f"Gatunki: {self.genres}", anchor="w", wraplength=600)
        genres_label.grid(row=1, column=1, sticky="w", pady=5)

        runtime_label = customtkinter.CTkLabel(self.content_frame, text=f"Czas trwania: {self.runtime} min", anchor="w")
        runtime_label.grid(row=2, column=1, sticky="w", pady=5)

        director_label = customtkinter.CTkLabel(self.content_frame, text=f"Reżyser: {self.director}", anchor="w")
        director_label.grid(row=3, column=1, sticky="w", pady=5)

        cast_label = customtkinter.CTkLabel(self.content_frame, text=f"Obsada: {self.cast}", anchor="w", wraplength=600)
        cast_label.grid(row=4, column=1, sticky="w", pady=5)

    def build_overview_section(self):
        overview_title = customtkinter.CTkLabel(self.scroll_frame, text="Opis:", font=("Arial", 16, "bold"))
        overview_title.pack(pady=(10, 0))

        overview_text = customtkinter.CTkLabel(self.scroll_frame, text=self.overview, wraplength=900, justify="left")
        overview_text.pack(pady=5, padx=20)

    def build_rating_section(self):
        rating_label = customtkinter.CTkLabel(self.scroll_frame, text="Twoja ocena:", font=("Arial", 14))
        rating_label.pack(pady=10)

        current_rating = self.controller.rating_manager.get_rating(self.user_id, self.movie_id)
        self.star_widget = StarRating(self.scroll_frame, initial_rating=current_rating)
        self.star_widget.pack(pady=5)

        save_button = customtkinter.CTkButton(self.scroll_frame, text="Zapisz ocenę", command=self.save_rating)
        save_button.pack(pady=10)

        back_button = customtkinter.CTkButton(self.scroll_frame, text="Powrót", command=self.go_back)
        back_button.pack(pady=10)

    def save_rating(self):
        rating = self.star_widget.get_rating()
        if rating > 0:
            self.controller.rating_manager.add_or_update_rating(self.user_id, self.movie_id, rating)
            self.controller.show_movies_menu(self.user_id)

    def get_poster_url(self, title):
        api_key = "540192c1f16471866e68fcadc8bfaf28"
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(url)
        data = response.json()
        if data["results"]:
            poster_path = data["results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None

    def go_back(self):
        self.controller.show_movies_menu(self.user_id)
