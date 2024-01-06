from pynput.mouse import Listener
import pyautogui
import tkinter as tk

import os

import pytesseract
from PIL import Image

import pyperclip

image_path = "screenshot_area.png"
tesseract_exe = r'C:\Program Files\Tesseract\tesseract.exe'
language_target = "jpn" #use language trained data in your tesseract/tessdata

class CaptureImproved :

    def capture_and_copy(self):
        self.capture_screen()
        text = self.extract_text_from_image(image_path)
        print(text)
        pyperclip.copy(text)

    def capture_screen(self):
        root = tk.Tk()

        def close_window():
            root.quit()
            root.destroy()

        ########################## Set Variables ##########################
        start_x = start_y = end_x = end_y = 0

        # Get the current screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root_geometry = str(screen_width) + 'x' + str(screen_height)  # Creates a geometric string argument
        root.geometry(root_geometry)  # Sets the geometry string value

        root.overrideredirect(True)
        root.wait_visibility(root)
        root.wm_attributes("-alpha", 0.3)  # Set windows transparent

        canvas = tk.Canvas(root, width=screen_width, height=screen_height)  # Create canvas
        canvas.config(cursor="cross")  # Change mouse pointer to cross
        canvas.pack()

        # Start and end coordinates for the rectangle
        rect = None

        def on_mouse_move(event):
            nonlocal start_x, start_y, end_x, end_y, rect
            end_x, end_y = event.x, event.y
            if rect:
                canvas.delete(rect)
            rect = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red")

        def on_mouse_press(event):
            nonlocal start_x, start_y
            start_x, start_y = event.x, event.y

        def on_mouse_release(event):
            nonlocal start_x, start_y, end_x, end_y

            left = min(start_x,end_x)
            top = min(start_y,end_y)
            width = abs(end_x - start_x)
            height = abs(end_y - start_y)

            root.wm_attributes("-alpha", 0)
            img = pyautogui.screenshot(region=(left, top, width, height))  # Take the screenshot
            img.save(image_path)  # Save the screenshot
            close_window()  # Remove tkinter window

        # Bind events to the canvas
        canvas.bind("<B1-Motion>", on_mouse_move)
        canvas.bind("<Button-1>", on_mouse_press)
        canvas.bind("<ButtonRelease-1>", on_mouse_release)

        root.protocol("WM_DELETE_WINDOW", close_window)  # Handle closing the window
        root.mainloop()  # Start tkinter window
        


    # Path to your Tesseract installation (modify this path as per your system's Tesseract installation)
    pytesseract.pytesseract.tesseract_cmd = tesseract_exe


    def extract_text_from_image(self,image_path):
        # Open the image file using PIL
        img = Image.open(image_path)

        # Use Tesseract OCR to extract text from the image
        extracted_text = pytesseract.image_to_string(img, lang=language_target)

        return extracted_text

if __name__ == "__main__":
    ci = CaptureImproved()
    ci.capture_and_copy()