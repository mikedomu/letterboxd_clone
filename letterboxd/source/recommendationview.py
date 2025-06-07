import customtkinter
class RecommendationView(customtkinter.CtkFrame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller
