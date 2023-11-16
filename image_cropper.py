import argparse
import sys
import os
import tkinter as tk
from PIL import Image, ImageTk

class ImageCropper:

    LIMIT_PX = 1000

    def __init__(self, master, image_files, confirm):
        self.master = master
        self.image_files = image_files
        self.current_image_index = 0
        self.confirm = confirm
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
        self.canvas.bind("<ButtonRelease-3>", self.on_button_release_noop)

        self.master.bind("<Left>", self.prev_image)
        self.master.bind("<Right>", self.next_image)
        
        self.master.bind("s", self.prev_image)
        self.master.bind("f", self.next_image)
        self.master.bind("d", self.delete_image)

        self.rect = None
        self.start_x = None
        self.start_y = None

    def load_image(self):
        self.filepath = self.image_files[self.current_image_index]
        self.image = Image.open(self.filepath)
        self.image_orig = self.image.copy()

        # Scale the image if its width or height is larger than LIMIT_PX
        if self.image.width > self.LIMIT_PX or self.image.height > self.LIMIT_PX:
            largest_dimension = max(self.image.width, self.image.height)
            self.scale = 1000 / largest_dimension
            new_width = int(self.image.width * self.scale)
            new_height = int(self.image.height * self.scale)
            self.image = self.image.resize((new_width, new_height), Image.BICUBIC)
        else:
            self.scale = 1

        self.photo = ImageTk.PhotoImage(self.image)

    def prev_image(self, event=None):
        self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
        self.update_image()

    def next_image(self, event=None):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.update_image()

    def update_image(self):
        self.load_image()
        self.canvas.config(width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.filename_label.config(text=os.path.basename(self.filepath)[:64])

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
        self.filename_label.config(text=f"{os.path.basename(self.filepath)[:64]} ({width}x{height})")

    def on_button_release(self, event):
        if not self.start_x or not self.start_y:
            return

        x1, y1, x2, y2 = min(self.start_x, event.x), min(self.start_y, event.y), max(self.start_x, event.x), max(self.start_y, event.y)

        x1 = int(x1 / self.scale)
        y1 = int(y1 / self.scale)
        x2 = int(x2 / self.scale)
        y2 = int(y2 / self.scale)

        if x1 != x2 and y1 != y2:
            cropped_image = self.image_orig.crop((x1, y1, x2, y2))
            if not self.confirm:
                self.show_cropped_image(cropped_image)
            else:
                # save without confirmation
                name = os.path.basename(self.filepath)
                new_name = f'cropped_{x1}_{y1}-{x2}_{y2}_{name}'
                cropped_image.save(os.path.join(os.path.dirname(self.filepath), new_name))

    def on_button_release_noop(self, event):
        self.start_x = None
        self.start_y = None
        self.clear_bounding_box()

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

    def delete_image(self, event=None):
        os.remove(self.filepath)
        self.image_files.remove(self.filepath)

        if not self.image_files:
            print("No more image files in the directory.")
            self.master.quit()
            return

        self.current_image_index %= len(self.image_files)
        self.update_image()

def main():
    parser = argparse.ArgumentParser(description="Image Cropper")
    parser.add_argument("image_directory", type=str, help="path to the directory containing image files")
    parser.add_argument("--confirm", action="store_true", help="save images without confirmation")
    args = parser.parse_args()

    image_directory = args.image_directory
    confirm = not args.confirm

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
    app = ImageCropper(root, image_files, confirm)
    root.mainloop()

if __name__ == "__main__":
    main()

