"""
Module implementing star rating widget.
"""

import customtkinter
from PIL import Image

class StarRating(customtkinter.CTkFrame):
    """
    Widget enabling rating from 0.5 to 5 stars.
    Inherits from customtkinter.CTkFrame.

    :param parent: Parent widget.
    :type parent: customtkinter.CTkBaseClass
    :param image_path: Path to the directory with star images.
    :type image_path: str
    :param initial_rating: Initial rating value.
    :type initial_rating: float
    :param on_rating_change: Callback called when rating changes.
    :type on_rating_change: callable or None
    """

    def __init__(self, parent, image_path="images", initial_rating=0, readonly=False):
        """
        Initializes the star rating widget and builds its interface.

        :param parent: Parent widget.
        :type parent: customtkinter.CTkBaseClass
        :param image_path: Path to the directory with star images.
        :type image_path: str
        :param initial_rating: Initial rating value.
        :type initial_rating: float
        :param on_rating_change: Callback called when rating changes.
        :type on_rating_change: callable or None
        """
        super().__init__(parent)
        self.rating = initial_rating
        self.readonly=readonly
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
        """
        Builds the user interface of the widget.
        """
        for i in range(5):
            star_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            star_frame.pack(side="left", padx=2)
            star_label = customtkinter.CTkLabel(star_frame, text="", image=self.star_empty)
            star_label.pack()
            self.star_labels.append(star_label)

            if not self.readonly:

                star_frame.bind('<Button-1>', lambda e, idx=i: self.set_rating(idx + 1))
                star_frame.bind('<Button-3>', lambda e, idx=i: self.set_rating(idx + 0.5))
                star_label.bind('<Button-1>', lambda e, idx=i: self.set_rating(idx + 1))
                star_label.bind('<Button-3>', lambda e, idx=i: self.set_rating(idx + 0.5))

    def set_rating(self, rating):
        """
        Sets the rating and updates star appearance.

        :param rating: New rating (0.5-5.0).
        :type rating: float
        """
        self.rating = rating
        for i, star_label in enumerate(self.star_labels):
            if i < int(self.rating):
                star_label.configure(image=self.star_full)
            elif i == int(self.rating) and self.rating % 1 != 0:
                star_label.configure(image=self.star_half)
            else:
                star_label.configure(image=self.star_empty)

    def get_rating(self):
        """
        Returns the current rating.

        :return: Current rating value.
        :rtype: float
        """
        return self.rating
