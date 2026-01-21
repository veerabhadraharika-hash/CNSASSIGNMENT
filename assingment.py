import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pyttsx3

# Text to speech engine
engine = pyttsx3.init()

# Global variables
original_image = None
stego_image = None
image_path = ""

# Convert character to 8-bit binary
def char_to_binary(ch):
    return format(ord(ch), '08b')

# Convert 8-bit binary to character
def binary_to_char(binary):
    return chr(int(binary, 2))

# Select image
def select_image():
    global original_image, image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if image_path:
        original_image = Image.open(image_path).convert("L")  # Convert to grayscale
        display_image(original_image, img_label)

# Display image
def display_image(img, label):
    img = img.resize((250, 250))
    tk_img = ImageTk.PhotoImage(img)
    label.config(image=tk_img)
    label.image = tk_img

# Hide data using LSB
def hide_data():
    global stego_image
    if original_image is None:
        messagebox.showerror("Error", "Please select an image")
        return

    ch = char_entry.get()
    if len(ch) != 1:
        messagebox.showerror("Error", "Enter exactly ONE character")
        return

    binary = char_to_binary(ch)

    pixels = list(original_image.getdata())
    new_pixels = []

    for i in range(8):
        pixel = pixels[i]
        pixel_binary = format(pixel, '08b')
        new_pixel_binary = pixel_binary[:-1] + binary[i]
        new_pixels.append(int(new_pixel_binary, 2))

    new_pixels.extend(pixels[8:])

    stego_image = Image.new("L", original_image.size)
    stego_image.putdata(new_pixels)
    stego_image.save("stego_image.png")

    display_image(stego_image, stego_label)
    messagebox.showinfo("Success", "Character hidden successfully!\nSaved as stego_image.png")

# Extract hidden character
def extract_data():
    global stego_image
    if stego_image is None:
        messagebox.showerror("Error", "No stego image found")
        return

    pixels = list(stego_image.getdata())
    binary = ""

    for i in range(8):
        binary += format(pixels[i], '08b')[-1]

    ch = binary_to_char(binary)
    result_label.config(text="Hidden Character: " + ch)
    speak_button.config(state=tk.NORMAL)

# Speak extracted character
def speak():
    text = result_label.cget("text").replace("Hidden Character: ", "")
    engine.say(text)
    engine.runAndWait()

# GUI
root = tk.Tk()
root.title("Image Steganography using LSB")

tk.Label(root, text="LSB Image Steganography", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack()

img_label = tk.Label(frame, text="Original Image")
img_label.grid(row=0, column=0, padx=20)

stego_label = tk.Label(frame, text="Stego Image")
stego_label.grid(row=0, column=1, padx=20)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Select Image", command=select_image).grid(row=0, column=0, padx=10)
tk.Label(btn_frame, text="Enter Character:").grid(row=0, column=1)
char_entry = tk.Entry(btn_frame, width=5)
char_entry.grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Hide Data", command=hide_data).grid(row=0, column=3, padx=10)
tk.Button(btn_frame, text="Extract Data", command=extract_data).grid(row=0, column=4, padx=10)

result_label = tk.Label(root, text="Hidden Character: ", font=("Arial", 12))
result_label.pack(pady=10)

speak_button = tk.Button(root, text="Speak", command=speak, state=tk.DISABLED)
speak_button.pack()

root.mainloop()
