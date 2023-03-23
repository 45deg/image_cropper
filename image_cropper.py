import sys
import os
import tkinter as tk
from PIL import Image, ImageTk

class ImageCropper:
    def __init__(self, master, image_files):
        self.master = master
        self.image_files = image_files
        self.current_image_index = 0
        self.load_image()

        self.filename_label = tk.Label(self.master)
        self.filename_label.pack()

        button_frame = tk.Frame(self.master)
        button_frame.pack(side="bottom", fill="x")

        prev_button = tk.Button(button_frame, text="<", command=self.prev_image)
        prev_button.pack(side="left", fill="x", expand=True)
        next_button = tk.Button(button_frame, text=">", command=self.next_image)
        next_button.pack(side="left", fill="x", expand=True)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_image)
        delete_button.pack(side="bottom", fill="x")
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
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.filename_label.config(text=f"{os.path.basename(self.filepath)} ({width}x{height})")

    def on_button_release(self, event):
        x1, y1, x2, y2 = min(self.start_x, event.x), min(self.start_y, event.y), max(self.start_x, event.x), max(self.start_y, event.y)

        if x1 != x2 and y1 != y2:
            cropped_image = self.image.crop((x1, y1, x2, y2))
            self.show_cropped_image(cropped_image)

    def clear_bounding_box(self):
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None

    def save_cropped_image(self, cropped_image):
        cropped_image.save(self.filepath)
        self.load_image()
        self.update_image()
        self.top.destroy()

    def show_cropped_image(self, cropped_image):
        self.top = tk.Toplevel()
        self.top.protocol("WM_DELETE_WINDOW", self.clear_bounding_box_and_close)

        label = tk.Label(self.top)
        label.pack()
        photo = ImageTk.PhotoImage(cropped_image)
        label.config(image=photo)
        label.image = photo

        save_button = tk.Button(self.top, text="Save", command=lambda: self.save_cropped_image(cropped_image))
        save_button.pack()
        discard_button = tk.Button(self.top, text="Discard", command=self.clear_bounding_box_and_close)
        discard_button.pack()

    def clear_bounding_box_and_close(self):
        self.clear_bounding_box()
        self.top.destroy()

    def delete_image(self):
        os.remove(self.filepath)
        self.image_files.remove(self.filepath)

        if not self.image_files:
            print("No more image files in the directory.")
            self.master.quit()
            return

        self.current_image_index %= len(self.image_files)
        self.update_image()

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

