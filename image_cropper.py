import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

class ImageCropper:
    def __init__(self, master, image_files):
        self.master = master
        self.image_files = image_files
        self.current_image_index = 0
        self.load_image()

        self.filename_label = tk.Label(self.master)
        self.filename_label.pack()

        prev_button = tk.Button(self.master, text="<", command=self.prev_image)
        prev_button.pack(side="left")
        next_button = tk.Button(self.master, text=">", command=self.next_image)
        next_button.pack(side="left")

        self.canvas = tk.Canvas(self.master, width=self.image.width, height=self.image.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def load_image(self):
        self.filepath = self.image_files[self.current_image_index]
        self.image = Image.open(self.filepath)
        self.photo = ImageTk.PhotoImage(self.image)

    def prev_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        self.update_image()

    def next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.update_image()

    def update_image(self):
        self.load_image()
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.filename_label.config(text=os.path.basename(self.filepath))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if self.rect:
            self.canvas.delete(self.rect)

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", width=2)

    def on_button_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        cropped_image = self.image.crop((self.start_x, self.start_y, event.x, event.y))
        self.show_cropped_image(cropped_image)

    def show_cropped_image(self, cropped_image):
        top = tk.Toplevel()
        label = tk.Label(top)
        label.pack()
        photo = ImageTk.PhotoImage(cropped_image)
        label.config(image=photo)
        label.image = photo

        save_button = tk.Button(top, text="Save", command=lambda: self.save_cropped_image(cropped_image))
        save_button.pack()
        discard_button = tk.Button(top, text="Discard", command=top.destroy)
        discard_button.pack()

    def save_cropped_image(self, cropped_image):
        save_path = filedialog.asksaveasfilename(defaultextension=".png")
        if save_path:
            cropped_image.save(save_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python image_cropper.py <image_directory>")
        sys.exit(1)

    image_directory = sys.argv[1]

    image_files = [
        os.path.join(image_directory, f)
        for f in os.listdir(image_directory)
        if os.path.isfile(os.path.join(image_directory, f)) and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
    ]

    if not image_files:
        print("No image files found in the specified directory.")
        sys.exit(1)

    root = tk.Tk()
    root.title("Image Cropper")
    app = ImageCropper(root, image_files)
    root.mainloop()

if __name__ == "__main__":
    main()
