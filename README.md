# Image Cropper

Image Cropper is a simple Python GUI application that allows users to crop images easily by drawing bounding boxes with their mouse.

## Usage

1. Install the required Python libraries using the following command:

```
pip install -r requirements.txt
```


2. Run the Image Cropper application by specifying the directory containing the images:

```
python image_cropper.py <image_directory>
```


Replace `<image_directory>` with the path to the directory containing the images you want to crop.

## Features

- Navigate through images in the specified directory using the < and > buttons
- Display the filename of the current image
- Crop images by drawing a bounding box with the mouse
- Save or discard cropped images

## Note

This source code and README is (almost) generated and fixed by ChatGPT-4, here is an initial prompt

> Write a Python GUI application called "Image Cropper" that performs the following tasks:
> [User Interface]
> The application should show the images in the directory specified by argv[1] one by one in a sequential manner.
> The application should include two buttons < and > to allow users to navigate between the images.
> The application should display the filename of the current image in a label.
>
> [Cropping feature]
> When the user wants to crop an image, they can use the mouse to draw a bounding box around the area they want to crop. The user > can initiate the crop by clicking and dragging the mouse to create a rectangular box on the image. The application should  display the box as the user is dragging it, with a red border that is 2 pixels wide.
>
> The user can release the mouse button to finalize the crop. Once the crop is finalized, the application should display the cropped image in a separate window, and the user can choose to save the cropped image or discard it.
>
> If the user wants to crop the image again, they can repeat the process by clicking and dragging the mouse to create a new bounding box. The application should allow the user to crop the image as many times as they want.
>
> In summary, the application should provide an intuitive and user-friendly way for the user to crop images by drawing bounding boxes with their mouse.