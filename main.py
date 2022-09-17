from tkinter import *
import requests
from PIL import Image, ImageTk
import math
from tkinter import ttk

api_id = "b2e4769a"
api_key = "ebb05e24a1f6b55f2f229af673c8ed2a"


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

        def edit_entry(self):
            text = self.get()
            if text == "Enter some ingredients...":
                self.delete(0, END)
            self["fg"] = "black"

        def redo_entry(self):
            text = self.get()
            if text.strip() == "":
                self["fg"] = "grey"
                self.insert(0, "Enter some ingredients...")

        def search_logic(self):
            key_id_dict = {"Meal Type": "&mealType=", "Dish Type":
                "&dishType=", "Region of Origin": "&cuisineType=",
                           "Dietary Requirements": "&health="}
            query = self.ingredients.get()
            print(api_id, api_key)
            if query != "Enter some ingredients..." and query != "":
                url = "https://api.edamam.com/api/recipes/v2?type=public&q=" + \
                      query + "&app_id=" + api_id + "&app_key=" + api_key
                for filter in self.filter_list:
                    value = filter.get().lower()
                    if value != "any":
                        url += key_id_dict[
                                   self.filter_types[self.filter_list.index(
                                       filter)]] + value
                print(url)
                request = requests.get(url)
                request = request.json()
                print(request)
                for item in request["hits"]:
                    print(item["recipe"]["url"])

        #######################################################################
        # Level 1
        self.reference = "homepage"
        self.blank = PhotoImage()
        self.filter_list = []
        self.window = Frame(root.root, bg="blue", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)

        self.window.rowconfigure(0, weight=4)
        self.window.rowconfigure(1, weight=1)
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

        #######################################################################
        # Top Bar

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

        self.question_image = root.format_image("question.png", (50, 50))
        self.question_button = Button(self.info, image=self.question_image,
                                      width=10, height=10, compound="c",
                                      relief="flat",
                                      borderwidth=0,
                                      bg="green", activebackground="green",
                                      command=lambda: root.change_frame(
                                          "overlay"))
        self.question_button.pack(side=LEFT, expand=True, fill='both')

        self.escape_image = root.format_image("exit.png", (50, 50))
        self.escape_button = Button(self.escape, image=self.escape_image,
                                    width=10, height=10, compound="c",
                                    relief="flat",
                                    borderwidth=0,
                                    bg="green", activebackground="green",
                                    command=lambda: root.root.destroy())
        self.escape_button.pack(side=LEFT, expand=True, fill='both')

        #######################################################################
        # Headers

        self.headers.columnconfigure(0, weight=2)
        self.headers.columnconfigure(1, weight=2)
        self.filter_header = Label(self.headers, bg="green", anchor="w",
                                   text="Filters")
        self.results_header = Label(self.headers, bg="green", anchor="w",
                                    text="Results")
        self.filter_header.grid(row=0, column=0, sticky="nsew")
        self.results_header.grid(row=0, column=1, sticky="nsew")

        #######################################################################
        # Body
        self.body.rowconfigure(0, weight=1)
        self.body.columnconfigure(0, weight=2)
        self.body.columnconfigure(1, weight=1)

        self.filters = Frame(self.body, bg="red")
        self.filters.grid(row=0, column=0, sticky="nsew")

        self.search.columnconfigure(0, weight=4)
        self.search.columnconfigure(1, weight=1)
        self.search.rowconfigure(0, weight=1)

        self.enter = Button(self.search, text="Search", relief="flat",
                            bg="white", command=lambda: search_logic(
                self))

        self.ingredients = Entry(self.search, font=root.font, fg="Grey",
                                 relief="flat")
        self.ingredients.insert(END, "Enter some ingredients...")

        self.ingredients.grid(row=0, column=0, padx=(10, 0),
                              pady=15, sticky="nsew")
        self.enter.grid(row=0, column=1, padx=(1, 10),
                        pady=15, sticky="nsew")

        self.ingredients.bind("<Button-1>", lambda a:
        edit_entry(self.ingredients))
        self.ingredients.bind("<FocusOut>", lambda a:
        redo_entry(self.ingredients))

        self.filter_making()
        #######################################################################
        # Scroll bar
        self.results_frame = Frame(self.body, bg="yellow")
        self.results = Canvas(self.results_frame, bg="blue",
                              highlightthickness=0)
        self.results_frame.grid(row=0, column=1, sticky="nsew")

        self.scrollbar = Scrollbar(self.results_frame, orient="vertical",
                                       command=self.results.yview)
        self.scrollable_frame = Frame(self.results, bg="pink")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results.configure(
                scrollregion=self.results.bbox("all")))

        self.canvas_frame = self.results.create_window((0, 0),
                                           window=self.scrollable_frame,
                                   anchor="nw")
        self.results.pack(side="left", fill="both", expand=True)
        for i in range(50):
            Label(self.scrollable_frame,
                      text="Sample scrolling label: "+str(i)).pack(
                side="top", fill="both", expand=True)
        self.results.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.results.bind('<Configure>', self.FrameWidth)
        self.scrollable_frame.bind("<Configure>", self.OnFrameConfigure)


        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.results.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.results.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.results.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def FrameWidth(self, event):
        canvas_width = event.width
        self.results.itemconfig(self.canvas_frame, width=canvas_width)

    def OnFrameConfigure(self, event):
        self.results.configure(scrollregion=self.results.bbox("all"))

    def filter_making(self):
        self.strings = [StringVar(), StringVar(), StringVar(),
                        StringVar()]

        # for s in strings:
        #     s.set("Any")
        # default.set("Any")

        self.filter_types = ["Meal Type", "Dish Type", "Region of Origin",
                             "Dietary Requirements"]
        filter_options = [["Any", "Breakfast", "Lunch", "Dinner", "Snack"],
                          ["Any", "Maincourse", "Side Dish", "Starter",
                           "Desserts",
                           "Alcohol Cocktail"], ["Any", "Italian", "Chinese",
                                                 "Indian", "Japanese",
                                                 "korean", "Mediterranean",
                                                 "Mexican", "Central Europe",
                                                 "Eastern Europe", "Asian",
                                                 "British", "American",
                                                 "South American"], ["Any",
                                                                     "Vegetarian",
                                                                     "Vegan",
                                                                     "Dairy-Free",
                                                                     "Peanut-Free"]]
        for i in range(8):
            print(i, math.floor(i / 2))
            # self.filters.rowconfigure(0, weight=1)
            if i % 2 == 0:
                label = Label(self.filters, bg="green", anchor="w",
                              text=self.filter_types[math.floor(i / 2)])
                label.pack(side=TOP, expand=True, fill='both', padx=(0, 20),
                           pady=5)
            if i % 2 == 1:
                menu = ttk.Combobox(self.filters, textvariable=self.strings[
                    math.floor(i / 2)])
                menu['values'] = filter_options[
                    math.floor(i / 2)]
                menu.current(0)
                menu['state'] = 'readonly'
                self.filter_list.append(menu)
                menu.pack(side=TOP, expand=True, fill='both', padx=(20, 0),
                          pady=5)


if __name__ == "__main__":
    MainProgram()
