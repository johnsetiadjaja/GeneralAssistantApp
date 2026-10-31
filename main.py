import tkinter as tk
from model import WeatherModel
from view import WeatherView
from controller import WeatherController

if __name__ == "__main__":
    root = tk.Tk()

    model = WeatherModel()
    view = WeatherView(root)
    controller = WeatherController(model, view)

    root.mainloop()