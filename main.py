from tkinter import *
import requests
from PIL import Image, ImageTk
import math
from tkinter import ttk
import webbrowser
from urllib.request import urlopen
import threading

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
        self.window = Frame(root.root, bg="#3a7002", width=0, height=0,
                            highlightbackground="white",
                            highlightthickness=4)
        self.window.grid(row=0, column=0, sticky="nsew", padx=40, pady=15)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        w,h = 902, 589
        self.instructions_image = Image.open("instructions.png")
        self.img_copy = self.instructions_image.copy()
        # Creating and then gridding the instructions
        self.instructions_label = Label(self.window,
                                     image=ImageTk.PhotoImage(self.instructions_image),
                                   bg="#3a7002", borderwidth=0)
        self.instructions_label.grid(row=0, column=0, sticky="nsew")
        self.instructions_label.bind('<Configure>', self._resize_image)

        self.escape_image = root.format_image("exit.png", (50, 50))
        self.escape_button = Button(self.window, image=self.escape_image,
                                    width=50, height=50, compound="c",
                                    relief="flat",
                                    borderwidth=0,
                                    bg="#3a7002", activebackground="#3a7002",
                                    command=lambda : root.change_frame(
                                        "homepage"))
        self.escape_button.grid(row=0, column=0, sticky="ne")

        self.edamam_image = root.format_image("Edamam_Badge.png", (85, 25))
        self.edamam = Label(self.window, width = 85, height = 25,
                            compound="c", image=self.edamam_image, bg="#3a7002")
        self.edamam.grid(row=0, column=0, sticky="se")
    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.instructions_label.configure(image=self.background_image)

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
        def image_conversion(item,i):
            data = urlopen(item["recipe"]["images"]["THUMBNAIL"][
                               "url"])
            image = ImageTk.PhotoImage(data=data.read())
            b = Button(self.scrollable_frame,
                       text=item["recipe"]["label"], bg="#65a603",
                       command=lambda i=item["recipe"][
                           "url"]:
                       self.callback(i), relief="flat", image=
                       image, compound=TOP, wraplength = 150)
            b.image = image
            if i % 2 == 0:
                b.grid(row=math.floor(i/2), column=i % 2, sticky="nsew",
                       padx=(7,3),
                       pady=2)
            else:
                b.grid(row=math.floor(i / 2), column=i % 2, sticky="nsew",
                       padx=(3,10),
                       pady=2)
        def search_logic(self):
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            key_id_dict = {"Meal Type": "&mealType=", "Dish Type":
                "&dishType=", "Region of Origin": "&cuisineType=",
                           "Dietary Requirements": "&health="}
            query = self.ingredients.get()
            if query != "Enter some ingredients..." and query != "":
                url = "https://api.edamam.com/api/recipes/v2?type=public&q=" + \
                      query + "&app_id=" + api_id + "&app_key=" + api_key

                for filter in self.filter_list:
                    value = filter.get().lower()
                    if value != "any":
                        value = value.split(" ")
                        value = "%20".join(value)
                        url += key_id_dict[
                                   self.filter_types[self.filter_list.index(
                                       filter)]] + value
                request = requests.get(url)
                request = request.json()
                self.scrollable_frame.columnconfigure(0, weight=1)
                self.scrollable_frame.columnconfigure(1, weight=1)
                for i in range(len(request["hits"])):
                    self.scrollable_frame.rowconfigure(math.floor(i / 2),
                                                       weight=1)
                i=0
                for item in request["hits"]:

                    x = threading.Thread(target=image_conversion,
                                         args=(item,i))
                    x.start()
                    i+=1

        root.root.bind('<Return>', lambda a: search_logic(self))
        #######################################################################
        # Level 1
        self.reference = "homepage"
        self.blank = PhotoImage()
        self.filter_list = []
        self.window = Frame(root.root, bg="#f9e99e", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)

        self.window.rowconfigure(0, weight=4)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=9)

        self.top_bar = Frame(self.window, bg="red")
        self.search = Frame(self.window, bg="#65a603")
        self.headers = Frame(self.window, bg="#2f6733")
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
                                      bg="#65a603", activebackground="#65a603",
                                      command=lambda: root.change_frame(
                                          "overlay"))
        self.question_button.pack(side=LEFT, expand=True, fill='both')

        self.title_image = root.format_image("feed.png", (1235
                                                          , 190))
        self.title_screen = Label(self.title, image=self.title_image, width=10,
                                  height=20, compound="c", bg="#f9e99e")
        self.title_screen.pack(side=LEFT, expand=True, fill='both')

        self.escape_image = root.format_image("exit.png", (50, 50))
        self.escape_button = Button(self.escape, image=self.escape_image,
                                    width=10, height=10, compound="c",
                                    relief="flat",
                                    borderwidth=0,
                                    bg="#65a603", activebackground="#65a603",
                                    command=lambda: root.root.destroy())
        self.escape_button.pack(side=LEFT, expand=True, fill='both')

        #######################################################################
        # Headers

        self.headers.columnconfigure(0, weight=2)
        self.headers.columnconfigure(1, weight=2)
        self.filter_header = Label(self.headers, bg="#65a603", anchor="w",
                                   text="Filters", font = ("Open Sans", 12))
        self.results_header = Label(self.headers, bg="#65a603", anchor="w",
                                    text="Results", font = ("Open Sans", 12))
        self.filter_header.grid(row=0, column=0, sticky="nsew")
        self.results_header.grid(row=0, column=1, sticky="nsew")

        #######################################################################
        # Body
        self.body.rowconfigure(0, weight=1)
        self.body.columnconfigure(0, weight=2)
        self.body.columnconfigure(1, weight=1)

        self.filters = Frame(self.body, bg="#3b7302")
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
        # Results
        self.results_frame = Frame(self.body, bg="yellow")
        self.results = Canvas(self.results_frame, bg="#eff2d5",
                              highlightthickness=0)
        self.results_frame.grid(row=0, column=1, sticky="nsew")

        self.scrollbar = Scrollbar(self.results_frame, orient="vertical",
                                       command=self.results.yview)
        self.scrollable_frame = Frame(self.results, bg="#eff2d5")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.results.configure(
                scrollregion=self.results.bbox("all")))

        self.canvas_frame = self.results.create_window((0, 0),
                                           window=self.scrollable_frame,
                                   anchor="nw")
        self.results.pack(side="left", fill="both", expand=True)

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

    def callback(self, url):
        webbrowser.open_new_tab(url)

    def filter_making(self):
        self.strings = [StringVar(), StringVar(), StringVar(),
                        StringVar()]

        # for s in strings:
        #     s.set("Any")
        # default.set("Any")

        self.filter_types = ["Meal Type", "Dish Type", "Region of Origin",
                             "Dietary Requirements"]
        filter_options = [["Any", "Breakfast", "Lunch", "Dinner", "Snack"],
                          ["Any", "Main course", "Side Dish", "Starter",
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
            if i % 2 == 0:
                label = Label(self.filters, bg="#65a603", anchor="w",
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
