from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk, ImageEnhance
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename, asksaveasfilename
from brightness_window import BrightnessWindow
from binaryzation_window import BinaryzationWindow


class MainWindow(Tk):
    file_types = [
        ('All files', '*'),
        ('JPEG files', '*.jpg;*.jpeg'),
        ('PNG files', '*.png'),
        ('BMP files', '*.bmp'),
        ('TIF files', '*tif'),
    ]
    BASE_IMAGE = None

    def __init__(self):
        super().__init__()
        self.image = None
        self.title("ImageApp")
        self.geometry("800x600")
        self.resizable(False, False)
        self.global_image = None
        self.menu_bar = Menu(self.master)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Zoom In")
        self.edit_menu.add_command(label="Zoom Out")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.config(menu=self.menu_bar)

        self.leftFrameStyle = Style().configure("Left.TFrame")
        self.leftFrame = Frame(self, width="620", height="580", style="Left.TFrame")
        self.leftFrame.pack_propagate(0)
        self.leftFrame.pack(fill=X, side=LEFT, padx=(10, 5), pady=10)

        self.image_canvas = Canvas(self.leftFrame, width="620", height="580", scrollregion=(0, 0, 0, 0))

        self.image_canvas.scrollX = Scrollbar(self.leftFrame, orient=HORIZONTAL)
        self.image_canvas.scrollY = Scrollbar(self.leftFrame, orient=VERTICAL)

        # now tie the three together. This is standard boilerplate text
        self.image_canvas['xscrollcommand'] = self.image_canvas.scrollX.set
        self.image_canvas['yscrollcommand'] = self.image_canvas.scrollY.set
        self.image_canvas.scrollX['command'] = self.image_canvas.xview
        self.image_canvas.scrollY['command'] = self.image_canvas.yview

        # pack 'em up
        self.image_canvas.scrollX.pack(side=BOTTOM, fill=X)
        self.image_canvas.scrollY.pack(side=RIGHT, fill=Y)
        self.image_canvas.pack(side=LEFT)

        self.rightFrameStyle = Style().configure("Right.TFrame")
        self.rightFrame = Frame(master=self, style="Right.TFrame", relief="groove")
        self.rightFrame.pack_propagate(0)
        self.rightFrame.pack(fill=BOTH, expand=True, side=RIGHT, padx=(5, 10), pady=10)

        self.colorLabel = Label(master=self.rightFrame, text="Color")
        self.colorLabel.pack(side=TOP, pady=(10, 0))

        self.colorSquareFrame = Frame(master=self.rightFrame, height="130", relief="solid")
        self.colorSquareFrame.pack(fill=BOTH, side=TOP, padx=10, pady=10)

        self.rgbValuesFrame = Frame(master=self.rightFrame, height="130")
        self.rgbValuesFrame.pack(fill=BOTH, side=TOP, padx=10, pady=10)

        # rValue element
        self.rValueFrame = Frame(master=self.rgbValuesFrame)
        self.rValueFrame.pack(pady=10)
        self.rValueLabel = Label(master=self.rValueFrame, text="R: ", width=3)
        self.rValueLabel.pack(side=LEFT, expand=True)
        self.rValueEntry = Entry(master=self.rValueFrame, width=4)
        self.rValueEntry.pack()

        # gValue element
        self.gValueFrame = Frame(master=self.rgbValuesFrame)
        self.gValueFrame.pack(pady=10)
        self.gValueLabel = Label(master=self.gValueFrame, text="G: ", width=3)
        self.gValueLabel.pack(side=LEFT, expand=True)
        self.gValueEntry = Entry(master=self.gValueFrame, width=4)
        self.gValueEntry.pack()

        # bValue element
        self.bValueFrame = Frame(master=self.rgbValuesFrame)
        self.bValueFrame.pack(pady=10)
        self.bValueLabel = Label(master=self.bValueFrame, text="B: ", width=3)
        self.bValueLabel.pack(side=LEFT, expand=True)
        self.bValueEntry = Entry(master=self.bValueFrame, width=4)
        self.bValueEntry.pack()

        self.histogram_button = Button(master=self.rightFrame, text="Histogram", command=self.histogram)
        self.histogram_button.pack()

        self.brightness_button = Button(master=self.rightFrame, text="Brightness", command=self.brightness_setup_window)
        self.brightness_button.pack(pady=10)

        self.binaryzation_button = Button(master=self.rightFrame, text="Binaryzation", command=self.binaryzation_setup_window)
        self.binaryzation_button.pack(pady=10)

    def binaryzation_setup_window(self):
        BinaryzationWindow(self, self.image, self.binaryzation_handler)

    def brightness_setup_window(self):
        BrightnessWindow(self, self.image, self.brightness_handler)

    def histogram(self):
        print("DZIAŁA")
        histogram_values = self.image.histogram()

        r_values = histogram_values[0:256]
        g_values = histogram_values[256:512]
        b_values = histogram_values[512:768]

        plt.subplot(3, 1, 1)
        plt.title("R value")
        for i in range(0, 256):
            plt.bar(i, r_values[i], color=self.get_red(i), edgecolor=self.get_red(i), alpha=0.3)

        plt.subplot(3, 1, 2)
        plt.title("G value")
        plt.ylabel("Ilość wystąpień")
        for i in range(0, 256):
            plt.bar(i, g_values[i], color=self.get_green(i), edgecolor=self.get_green(i), alpha=0.3)

        plt.subplot(3, 1, 3)
        plt.title("B value")
        for i in range(0, 256):
            plt.bar(i, b_values[i], color=self.get_blue(i), edgecolor=self.get_blue(i), alpha=0.3)

    @staticmethod
    def get_red(red_val):
        return '#%02x%02x%02x' % (red_val, 0, 0)

    @staticmethod
    def get_green(green_val):
        return '#%02x%02x%02x' % (0, green_val, 0)

    @staticmethod
    def get_blue(blue_val):
        return '#%02x%02x%02x' % (0, 0, blue_val)

    def save_file(self):
        self.image.save(asksaveasfilename(filetypes=self.file_types))

    def display(self, image):
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_canvas.configure(scrollregion=(0, 0, self.tk_image.width(), self.tk_image.height()))
        self.image_canvas.bind("<Button-3>", self.grab_pixel)
        self.image_canvas.bind("<Button-1>", self.put_pixel)
        self.imageTMP = self.image_canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

    def grab_pixel(self, event):
        x = self.image_canvas.canvasx(event.x)
        y = self.image_canvas.canvasy(event.y)
        self.image = self.image.convert('RGB')
        self.pixmap = self.image.load()
        self.color = self.pixmap[x, y]

        self.rValStrVar = StringVar()
        self.gValStrVar = StringVar()
        self.bValStrVar = StringVar()

        self.rValueEntry['textvariable'] = self.rValStrVar
        self.gValueEntry['textvariable'] = self.gValStrVar
        self.bValueEntry['textvariable'] = self.bValStrVar

        self.rValStrVar.set(self.color[0])
        self.gValStrVar.set(self.color[1])
        self.bValStrVar.set(self.color[2])

        self.newColorSquareStyle = Style()
        self.newColorSquareStyle.configure("New.TFrame", background=('#%02x%02x%02x' % self.color))
        self.colorSquareFrame['style'] = "New.TFrame"

    def put_pixel(self, event):
        x = self.image_canvas.canvasx(event.x)
        y = self.image_canvas.canvasy(event.y)
        raw_image = self.image.load()
        raw_image[x, y] = (int(self.rValueEntry.get()), int(self.gValueEntry.get()), int(self.bValueEntry.get()))
        self.display(self.image)

    def open_image(self):
        file_path = askopenfilename(filetypes=self.file_types)
        self.BASE_IMAGE = Image.open(file_path)
        self.image = Image.open(file_path)
        self.display(self.image)

    def brightness_handler(self, changed_image):
        self.image = changed_image
        self.display(changed_image)

    def binaryzation_handler(self):
        pass


def main():
    main_window = MainWindow()
    main_window.mainloop()


if __name__ == '__main__':
    main()
