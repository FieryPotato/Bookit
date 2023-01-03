from Model import Model
from View import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
