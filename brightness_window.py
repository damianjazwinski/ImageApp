from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk, ImageEnhance


class BrightnessWindow(Toplevel):
    ORIGINAL_IMAGE = None

    def __init__(self, parent, image, window_handler):
        super().__init__()
        self.brightness_handler = window_handler
        self.master = parent
        self.title("Brightness")
        self.geometry("600x600")
        self.resizable(False, False)

        self.ORIGINAL_IMAGE = image
        self.image_small = self.ORIGINAL_IMAGE.copy()
        self.image_small.thumbnail((500, 500), Image.ANTIALIAS)

        self.tk_image = ImageTk.PhotoImage(self.image_small)
        self.brightness_enhancer = ImageEnhance.Brightness(self.image_small)

        self.canvas = Canvas(self, width=700, height=500)
        self.canvas.grid(row=1, column=1)
        self.image_on_canvas = self.canvas.create_image(50, 50, anchor=NW, image=self.tk_image)

        self.scale_value = DoubleVar()
        self.scale = Scale(master=self, from_=0, to=2, length=200, variable=self.scale_value, command=self.scale_handler)
        self.scale.grid(row=2, column=1)
        self.scale.set(1.0)

        self.ok_button = Button(master=self, text="OK", command=self.ok)
        self.ok_button.grid(row=3, column=1)

    def scale_handler(self, event):
        self.scale_val = round(self.scale_value.get(), 2)
        changed_image = self.brightness_enhancer.enhance(self.scale_val)
        self._tk_image = ImageTk.PhotoImage(changed_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self._tk_image)
        self.image_small = changed_image

    def ok(self):
        enhancer = ImageEnhance.Brightness(self.ORIGINAL_IMAGE)
        self.brightness_handler(enhancer.enhance(self.scale_val))
        self.destroy()
