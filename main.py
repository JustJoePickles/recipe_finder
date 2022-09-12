from tkinter import *
import requests
from PIL import Image, ImageTk
import math
from tkinter import ttk

class MainProgram():
    def __init__(self):
        self.root = Tk()
        self.root.title("Recipe Finder")
        self.root.geometry("800x500")
        self.root.configure(background="white")
        self.font = ("Noto Sans SemiBold", 14)

        self.overlay = Overlay(self)

        self.homepage = HomePage(self)

        self.frames = {}
        for f in (self.homepage, self.overlay):
            page_name = f.reference
            frame = f.window
            self.frames[page_name] = frame
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.mainloop()

    def change_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        self.top_layer = page_name

    def format_image(self, i, size):
        image = Image.open(i)
        image = image.resize(size)
        image = ImageTk.PhotoImage(image)
        return image


class Overlay():
    def __init__(self, root):
        self.reference = "overlay"
        self.window = Frame(root.root, bg="pink", width=0, height=0,
                            highlightbackground="white",
                            highlightthickness=0)
        self.window.grid(row=0, column=0, sticky="nsew", padx=40, pady=15)


        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=8)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=1)
        # info = Frame(self.window, bg="purple")
        # title = Frame(self.window, bg="orange")
        # escape = Frame(self.window, bg="cyan")
        #
        # info.grid(row=0, column=0, sticky="nsew")
        # title.grid(row=0, column=1, sticky="nsew")
        # escape.grid(row=0, column=2, sticky="nsew")


class HomePage():
    def __init__(self, root):
        self.reference = "homepage"
        self.blank = PhotoImage()
        self.grid_objects = []
        self.filter_list=[]
        self.window = Frame(root.root, bg="blue", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)

        self.window.rowconfigure(0, weight=2)
        self.window.rowconfigure(1, weight=3)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=9)

        self.top_bar = Frame(self.window, bg="red")
        self.search = Frame(self.window, bg="green")
        self.headers = Frame(self.window, bg="dark green")
        self.body = Frame(self.window, bg="yellow")

        self.top_bar.grid(row=0, column=0, sticky="nsew")
        self.search.grid(row=1, column=0, sticky="nsew")
        self.headers.grid(row=2, column=0, sticky="nsew")
        self.body.grid(row=3, column=0, sticky="nsew")

        self.top_bar.rowconfigure(0, weight=1)
        self.top_bar.columnconfigure(0, weight=1)
        self.top_bar.columnconfigure(1, weight=8)
        self.top_bar.columnconfigure(2, weight=1)

        self.info = Frame(self.top_bar, bg="purple")
        self.title = Frame(self.top_bar, bg="navy")
        self.escape = Frame(self.top_bar, bg="grey")

        self.info.grid(row=0, column=0, sticky="nsew")
        self.title.grid(row=0, column=1, sticky="nsew")
        self.escape.grid(row=0, column=2, sticky="nsew")

        self.body.rowconfigure(0, weight=1)
        self.body.columnconfigure(0,weight=1)
        self.body.columnconfigure(1,weight=2)
        self.filters = Frame(self.body, bg="red")
        self.results = Frame(self.body, bg="yellow")

        self.filters.grid(row=0, column=0, sticky="nsew")
        self.results.grid(row=0, column=1, sticky="nsew")

        self.ingredients = Entry(self.search, font=root.font)
        self.ingredients.pack(side=TOP, expand=True, fill='both', padx=20,
                              pady=30)

        self.filter_making()

    def filter_making(self):
        self.strings = [StringVar(), StringVar(), StringVar(),
                   StringVar()]

        # for s in strings:
        #     s.set("Any")
        # default.set("Any")

        filter_list = ["Meal Type", "Dish Type", "Region of Origin",
                          "Dietary Requirements"]
        filter_options =[["Any", "Breakfast", "Lunch/Dinner", "Snack"],
                         ["Any", "Maincourse", "Side Dish", "Starter",
                          "Desserts",
                          "Alcohol Cocktail"], ["Any", "Italian", "Chinese",
                                                "Indian", "Japanese",
                                                "korean", "Mediterranean",
                                                "Mexican", "Central Europe",
                                                "Eastern Europe", "Asian",
                                                "British", "American",
                                                "South American"], ["Any",
                         "Vegetarian", "Vegan", "Dairy-Free", "Peanut-Free"]]
        for i in range(8):
            print(i, math.floor(i/2))
            # self.filters.rowconfigure(0, weight=1)
            if i % 2 == 0:
                label = Label(self.filters, bg="green", anchor = "w",
                              text = filter_list[math.floor(i/2)])
                label.pack(side=TOP, expand=True, fill='both', padx=(0,20),
                              pady=5)
            if i % 2 == 1:
                menu = ttk.Combobox(self.filters, textvariable=self.strings[
                    math.floor(i/2)])
                menu['values'] = filter_options[
                    math.floor(i/2)]
                menu.current(0)
                menu['state'] = 'readonly'
                self.filter_list.append(menu)
                menu.pack(side=TOP, expand=True, fill='both', padx=(20,0),
                              pady=5)

        print(self.filter_list)

if __name__ == "__main__":
    MainProgram()
