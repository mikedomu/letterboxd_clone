import customtkinter
from PIL import Image

class StarRating(customtkinter.CTkFrame):
    def __init__(self, parent, image_path="images", initial_rating=0, on_rating_change=None):
        super().__init__(parent)
        self.on_rating_change = on_rating_change
        self.rating = initial_rating
        self.star_empty = customtkinter.CTkImage(
            light_image=Image.open(f"{image_path}/emptystar.png"),
            dark_image=Image.open(f"{image_path}/emptystar.png"),
            size=(20, 20)
        )
        self.star_half = customtkinter.CTkImage(
            light_image=Image.open(f"{image_path}/halfstar.png"),
            dark_image=Image.open(f"{image_path}/halfstar.png"),
            size=(20, 20)
        )
        self.star_full = customtkinter.CTkImage(
            light_image=Image.open(f"{image_path}/star.png"),
            dark_image=Image.open(f"{image_path}/star.png"),
            size=(20, 20)
        )
        self.star_labels = []
        self.build_ui()
        self.set_rating(initial_rating)

    def build_ui(self):
        for i in range(5):
            star_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            star_frame.pack(side="left", padx=2)
            star_label = customtkinter.CTkLabel(star_frame, text="", image=self.star_empty)
            star_label.pack()
            self.star_labels.append(star_label)
            # Obsługa kliknięć: lewy i prawy przycisk myszy
            star_frame.bind('<Button-1>', lambda e, idx=i: self.set_rating(idx + 1))
            star_frame.bind('<Button-3>', lambda e, idx=i: self.set_rating(idx + 0.5))
            star_label.bind('<Button-1>', lambda e, idx=i: self.set_rating(idx + 1))
            star_label.bind('<Button-3>', lambda e, idx=i: self.set_rating(idx + 0.5))

    def set_rating(self, rating):
        self.rating = rating
        for i, star_label in enumerate(self.star_labels):
            if i < int(self.rating):
                star_label.configure(image=self.star_full)
            elif i == int(self.rating) and self.rating % 1 != 0:
                star_label.configure(image=self.star_half)
            else:
                star_label.configure(image=self.star_empty)
        if self.on_rating_change:
            self.on_rating_change(self.rating)

    def get_rating(self):
        return self.rating