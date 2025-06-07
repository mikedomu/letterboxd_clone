import customtkinter
import tkinter
from PIL import Image
from starrating import StarRating
import datetime
import csv
from collections import Counter

# Wykres
import matplotlib
matplotlib.use("Agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class MoviesView(customtkinter.CTkFrame):
    def __init__(self, parent, controller, username, user_id):
        super().__init__(parent)
        self.controller = controller
        self.username = username
        self.user_id = user_id

        self.configure_grid()
        self.build_top_bar()
        self.build_rated_movies_panel()
        self.build_search_panel()
        self.build_bottom_section()
        self.load_user_rated_movies()

    def configure_grid(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

    def build_top_bar(self):
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 0))

        logout_button = customtkinter.CTkButton(top_bar, text="Wyloguj", width=100, command=self.logout)
        logout_button.pack(side="left")

        welcome_label = customtkinter.CTkLabel(top_bar, text=f"Witaj, {self.username}!", font=("Arial", 14, "bold"))
        welcome_label.pack(side="left", padx=20)

    def build_rated_movies_panel(self):
        self.left_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)
        self.left_frame.rowconfigure(0, weight=1)

        self.left_scrollable = customtkinter.CTkScrollableFrame(self.left_frame)
        self.left_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        self.left_scrollable.grid_columnconfigure(0, weight=1)

        label = customtkinter.CTkLabel(self.left_scrollable, text="Moje ocenione filmy", font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, pady=10, sticky="ew")

        sort_frame = customtkinter.CTkFrame(self.left_scrollable, fg_color="transparent")
        sort_frame.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="w")

        sort_label = customtkinter.CTkLabel(sort_frame, text="Sortuj:", font=("Arial", 12))
        sort_label.pack(side="left", padx=(0, 10))

        self.sort_var = customtkinter.StringVar(value="A-Z")
        sort_options = ["A-Z", "Ocena rosnąco", "Ocena malejąco"]
        sort_menu = customtkinter.CTkOptionMenu(sort_frame, variable=self.sort_var, values=sort_options, command=self.sort_and_reload)
        sort_menu.pack(side="left")

        export_button = customtkinter.CTkButton(sort_frame, text="Eksportuj do CSV", command=self.export_to_csv)
        export_button.pack(side="left", padx=(10, 0))

        self.rated_movies_listbox = customtkinter.CTkFrame(self.left_scrollable)
        self.rated_movies_listbox.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        date_str = datetime.datetime.now().strftime("%d.%m.%Y")
        self.date_label = customtkinter.CTkLabel(self.left_scrollable, text=f"Dzisiaj: {date_str}", font=("Arial", 12))
        self.date_label.grid(row=3, column=0, pady=(0, 5), sticky="ew")

        self.context_menu = tkinter.Menu(self, tearoff=0)

    def build_search_panel(self):
        self.right_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=1, column=1, sticky="nswe", padx=20, pady=20)

        search_label = customtkinter.CTkLabel(self.right_frame, text="Wyszukaj film:", font=("Arial", 16, "bold"))
        search_label.pack(pady=10)

        self.search_entry = customtkinter.CTkEntry(self.right_frame, width=400)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_movies)

        self.search_results_frame = customtkinter.CTkScrollableFrame(self.right_frame, height=500)
        self.search_results_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def build_bottom_section(self):
        self.bottom_frame = customtkinter.CTkFrame(self)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.bottom_frame.grid_columnconfigure(0, weight=3)
        self.bottom_frame.grid_columnconfigure(1, weight=2)

        self.chart_frame = customtkinter.CTkFrame(self.bottom_frame)
        self.chart_frame.grid(row=0, column=0, padx=10, sticky="nsew")

        self.stats_label = customtkinter.CTkLabel(self.bottom_frame, text="", font=("Arial", 18, "bold"))
        self.stats_label.grid(row=0, column=1, padx=10, sticky="nsew")

    def logout(self):
        self.controller.show_main_menu()

    def load_user_rated_movies(self):
        self.clear_scrollable_frame(self.rated_movies_listbox)
        rated_movies = self.controller.rating_manager.get_user_rated_movies(self.user_id)

        sort_mode = self.sort_var.get()
        if sort_mode == "A-Z":
            rated_movies.sort(key=lambda x: x[0].lower())
        elif sort_mode == "Ocena rosnąco":
            rated_movies.sort(key=lambda x: x[1])
        elif sort_mode == "Ocena malejąco":
            rated_movies.sort(key=lambda x: -x[1])

        if not rated_movies:
            label = customtkinter.CTkLabel(self.rated_movies_listbox, text="Brak ocenionych filmów")
            label.pack(pady=5)
        else:
            for title, rating in rated_movies:
                movie_frame = customtkinter.CTkFrame(self.rated_movies_listbox)
                movie_frame.pack(fill="x", padx=5, pady=5)

                title_button = customtkinter.CTkButton(movie_frame, text=title, width=400)
                title_button.pack(side="left", padx=5, fill="x", expand=True)

                stars_frame = customtkinter.CTkFrame(movie_frame)
                stars_frame.pack(side="right", padx=15)

                star_widget = StarRating(stars_frame, initial_rating=rating)
                star_widget.pack()

                title_button.bind('<Button-1>', lambda e, t=title, r=rating: self.show_context_menu(e, t, r))
                movie_frame.bind('<Button-1>', lambda e, t=title, r=rating: self.show_context_menu(e, t, r))
                stars_frame.bind('<Button-1>', lambda e, t=title, r=rating: self.show_context_menu(e, t, r))

        self.update_statistics()

    def sort_and_reload(self, *args):
        self.load_user_rated_movies()

    def search_movies(self, event=None):
        query = self.search_entry.get()
        results = self.controller.database.search_movies(query)

        self.clear_scrollable_frame(self.search_results_frame)

        if not results:
            label = customtkinter.CTkLabel(self.search_results_frame, text="Brak wyników")
            label.pack(pady=5)
        else:
            for movie in results:
                button = customtkinter.CTkButton(
                    self.search_results_frame,
                    text=movie,
                    command=lambda m=movie: self.show_movie_details(m)
                )
                button.pack(anchor="w", padx=5, pady=5)

    def clear_scrollable_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_movie_details(self, movie_title):
        self.controller.show_movie_detail(movie_title)

    def show_context_menu(self, event, title, rating):
        self.context_menu.delete(0, 'end')
        self.context_menu.add_command(label="Podobne filmy")
        self.context_menu.add_command(label="Edytuj ocenę", command=lambda: self.edit_rating(title))
        self.context_menu.add_command(label="Usuń film", command=lambda: self.delete_rated_movie(title))
        self.context_menu.post(event.x_root, event.y_root)

    def edit_rating(self, movie_title):
        rating_window = customtkinter.CTkToplevel(self)
        rating_window.title("Oceń film")
        rating_window.geometry("400x150")
        rating_window.attributes('-topmost', True)

        label = customtkinter.CTkLabel(rating_window, text=f"Oceń film {movie_title}")
        label.pack(pady=10)

        movie_id = self.controller.rating_manager.get_movie_id_by_title(movie_title)
        current_rating = self.controller.rating_manager.get_rating(self.user_id, movie_id)

        star_widget = StarRating(rating_window, initial_rating=current_rating)
        star_widget.pack(pady=10)

        def save_rating():
            rating = star_widget.get_rating()
            if rating > 0:
                self.controller.rating_manager.add_or_update_rating(self.user_id, movie_id, rating)
                self.load_user_rated_movies()
                rating_window.destroy()

        save_button = customtkinter.CTkButton(rating_window, text="Zapisz ocenę", command=save_rating)
        save_button.pack(pady=10)

    def delete_rated_movie(self, movie_title):
        movie_id = self.controller.rating_manager.get_movie_id_by_title(title=movie_title)
        if movie_id:
            self.controller.rating_manager.delete_rating(self.user_id, movie_id)
            self.load_user_rated_movies()

    def export_to_csv(self):
        rated_movies = self.controller.rating_manager.get_user_rated_movies(self.user_id)
        with open(f"{self.username}_rated_movies.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Tytuł", "Ocena"])
            for title, rating in rated_movies:
                writer.writerow([title, rating])

    def update_statistics(self):
        rated_movies = self.controller.rating_manager.get_user_rated_movies(self.user_id)

        num_movies = len(rated_movies)
        avg_rating = round(sum(r for _, r in rated_movies) / num_movies, 2) if num_movies else 0

        genres = []
        for title, _ in rated_movies:
            movie_id = self.controller.rating_manager.get_movie_id_by_title(title)
            genres_str = self.controller.database.get_genres_by_movie_id(movie_id)
            if genres_str:
                genres.extend(genres_str.split(', '))

        most_common_genre = "-"
        if genres:
            most_common_genre = Counter(genres).most_common(1)[0][0]

        stats_text = (
            f"Filmy: {num_movies}\n"
            f"Średnia ocena: {avg_rating}\n"
            f"Najczęstszy gatunek:\n{most_common_genre}"
        )
        self.stats_label.configure(text=stats_text)
        self.draw_rating_chart(rated_movies)

    def draw_rating_chart(self, rated_movies):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        ratings = [rating for _, rating in rated_movies]
        counts = Counter(ratings)
        all_ratings = [counts.get(i, 0) for i in range(1, 6)]

        fig, ax = plt.subplots(figsize=(3, 2), dpi=100)
        ax.bar([1, 2, 3, 4, 5], all_ratings, color='skyblue')
        ax.set_title("Rozkład ocen")
        ax.set_xlabel("Ocena (★)")
        ax.set_ylabel("Liczba filmów")
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        plt.close(fig)
