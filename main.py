from tkinter import *
import requests
from PIL import Image, ImageTk

class MainProgram():
    def __init__(self):
        self.root = Tk()
        self.root.title("Recipe Finder")
        self.root.geometry("800x500")
        self.root.configure(background="white")


        self.homepage = HomePage(self)
        self.overlay = Overlay(self)
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

        self.font = ("Noto Sans SemiBold", 14)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=8)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=1)
        info = Frame(self.window, bg="purple")
        title = Frame(self.window, bg="orange")
        escape = Frame(self.window, bg="cyan")

        info.grid(row=0, column=0, sticky="nsew")
        title.grid(row=0, column=1, sticky="nsew")
        escape.grid(row=0, column=2, sticky="nsew")

class HomePage():
    def __init__(self, root):
        self.reference = "homepage"
        self.blank = PhotoImage()
        self.grid_objects = []
        self.window = Frame(root.root, bg="blue", width=0, height=0)
        self.window.grid(row=0, column=0, sticky="nsew")

        self.window.columnconfigure(0, weight=1)

        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=2)
        self.window.rowconfigure(2, weight=5)

        self.top_bar = Frame(self.window, bg="red")
        self.search = Frame(self.window, bg="green")
        self.body = Frame(self.window, bg="yellow")

        self.top_bar.grid(row=0, column=0, sticky="nsew")
        self.search.grid(row=1, column=0, sticky="nsew")
        self.body.grid(row=2, column=0, sticky="nsew")


if __name__ == "__main__":
    MainProgram()