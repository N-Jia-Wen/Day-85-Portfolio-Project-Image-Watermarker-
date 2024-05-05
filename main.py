from tkinter import Tk, Label, Entry, Canvas, Button, filedialog, messagebox, END
from PIL import Image, ImageTk, ImageDraw, ImageFont
from ctypes import windll
import pyglet

# By convention, while we install the Pillow package, we still import Image from PIL instead of Pillow.

# Last value alters opacity, with 255 being completely opaque and 0 being completely transparent:
watermark_colour_rgb = (255, 255, 255, 130)


class ImageWatermarker:

    def upload_img(self):
        file_path = filedialog.askopenfilename(filetypes=(("PNG Image files", "*.png"),
                                                          ("JPEG Image files", "*.jpg;*.jpeg")))
        # Checks if file_path is truthy. If user does not upload file, code does not execute.
        if file_path:
            self.img = Image.open(file_path).convert("RGBA")

    def add_watermark(self):
        watermark_text = self.watermark_entry.get()

        if self.img is None:
            messagebox.showinfo(title="No Image Uploaded",
                                message="Please upload the image you want to watermark first.")
        elif watermark_text == "":
            messagebox.showinfo(title="No Watermark Text",
                                message="Please enter the text you would like to use as your watermark.")
        else:
            # From: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#example-draw-partial-opacity-text
            img_width, img_height = self.img.size
            with self.img as base:

                # Scales text size in relation to image size and centres text. Taken from
                # https://stackoverflow.com/questions/4902198/pil-how-to-scale-text-size-
                # in-relation-to-the-size-of-the-image. Uses font.getlength() instead of getsize().
                # See docs: https://pillow.readthedocs.io/en/stable/reference/ImageFont.html
                img_fraction = 0.50
                font_size = 1
                jump_size = 75
                font_path = "./fonts/Libre_Franklin/static/LibreFranklin-Bold.ttf"
                font = ImageFont.truetype(font_path, font_size)
                break_point = img_fraction * base.size[0]

                while True:
                    if font.getlength(watermark_text) < break_point:
                        font_size += jump_size
                    else:
                        jump_size = jump_size // 2
                        font_size -= jump_size
                    font = ImageFont.truetype(font_path, font_size)
                    if jump_size <= 1:
                        break

                txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt)
                text_width = draw.textlength(watermark_text, font=font)
                x = (img_width - text_width) / 2
                y = (img_height - font_size) / 2

                draw.text((x, y),
                          text=watermark_text,
                          font=font,
                          fill=watermark_colour_rgb)

                output = Image.alpha_composite(base, txt)
                output.show()

    def __init__(self):
        # To fix blurry tkinter font AND blurry pop-up box when uploading img file. Taken from https://stackoverflow.com
        # /questions/41315873/attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp
        # /43046744#43046744
        windll.shcore.SetProcessDpiAwareness(1)

        # Rendering custom fonts. Taken from https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
        pyglet.font.add_file("./fonts/Libre_Franklin/LibreFranklin-VariableFont_wght.ttf")

        # Creates window
        self.window = Tk()
        self.window.title("Watermark your image!")
        self.window.minsize(width=1000, height=1000)
        self.window.config(padx=20, pady=20, bg="white")

        # Creates title text:
        self.title_label = Label(text="Image Watermarker", font=("Libre Franklin Thin", 40, "underline"), fg="#5582BF",
                                 bg="white")
        self.title_label.config(padx=20, pady=20)
        self.title_label.grid(column=0, row=0, columnspan=2)

        # Creates canvas:
        self.canvas = Canvas(width=1000, height=600, bg="white", highlightthickness=0)
        # img taken from https://images.app.goo.gl/94XY9Z4aRpeC5H5K7.
        # Some problems encountered when using PhotoImage from tkinter, so uses PIL's ImageTk.PhotoImage instead.
        # See https://stackoverflow.com/questions/47357090/tkinter-error-couldnt-recognize-data-in-image-file.
        example_img = ImageTk.PhotoImage(Image.open("./img/example-img.png"))
        self.canvas.create_image(500, 300, image=example_img)
        self.canvas.grid(column=0, row=1, columnspan=2)

        # Creates watermark label:
        self.watermark_label = Label(text="Your watermark text: ", font=("Libre Franklin Thin", 23, "normal"))
        self.watermark_label.config(pady=20, bg="white")
        self.watermark_label.grid(column=0, row=2)

        # Creates watermark entry (for user to enter their watermark text):
        self.watermark_entry = Entry(width=20, font=("Libre Franklin Thin", 23, "normal"))
        self.watermark_entry.insert(END, string="© ")
        self.watermark_entry.grid(column=1, row=2)

        # Creates button to upload image:
        self.upload_button = Button(text="Upload Image", font=("Arial", 16, "normal"), command=self.upload_img)
        self.upload_button.grid(column=0, row=3)

        # Creates button to watermark image:
        self.watermark_button = Button(text="Watermark Image", font=("Arial", 16, "normal"), command=self.add_watermark)
        self.watermark_button.grid(column=1, row=3)

        # Image that user wants to watermark:
        self.img = None

        self.window.mainloop()


watermarker = ImageWatermarker()
