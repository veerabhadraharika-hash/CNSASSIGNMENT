import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pyttsx3

engine = pyttsx3.init()
original_image = None
stego_image = None

# -------- Binary --------
def char_to_binary(ch):
    return format(ord(ch), '08b')

def binary_to_char(binary):
    return chr(int(binary, 2))

# -------- Show Image --------
def show_image(img, label):
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

# -------- Select Image --------
def select_image():
    global original_image
    path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
    if path:
        original_image = Image.open(path).convert("L")
        show_image(original_image, original_label)

# -------- Hide Data --------
def hide_data():
    global stego_image

    if original_image is None:
        messagebox.showerror("Error", "Select an image first")
        return

    ch = char_entry.get()
    if len(ch) != 1:
        messagebox.showerror("Error", "Enter one character")
        return

    binary = char_to_binary(ch)
    pixels = list(original_image.getdata())
    new_pixels = []

    for i in range(8):
        p = pixels[i]
        b = format(p, '08b')
        new_pixels.append(int(b[:-1] + binary[i], 2))

    new_pixels.extend(pixels[8:])

    stego_image = Image.new("L", original_image.size)
    stego_image.putdata(new_pixels)
    stego_image.save("stego.png")

    show_image(stego_image, stego_label)
    messagebox.showinfo("Done", "Character hidden successfully")

# -------- Extract --------
def extract_data():
    if stego_image is None:
        messagebox.showerror("Error", "No stego image")
        return

    pixels = list(stego_image.getdata())
    binary = ""

    for i in range(8):
        binary += format(pixels[i], '08b')[-1]

    ch = binary_to_char(binary)
    result_label.config(text="Hidden Character: " + ch)
    speak_btn.config(state="normal")

# -------- Speak --------
def speak():
    text = result_label.cget("text").replace("Hidden Character: ", "")
    engine.say(text)
    engine.runAndWait()

# ---------------- UI ----------------
root = tk.Tk()
root.title("LSB Steganography")
root.geometry("750x500")
root.configure(bg="#ddeeff")

tk.Label(root, text="Image Steganography using LSB",
         font=("Arial", 20, "bold"), bg="#ddeeff").pack(pady=10)

# Image frames
frame = tk.Frame(root, bg="#ddeeff")
frame.pack(pady=10)

left = tk.Frame(frame, bg="white", width=220, height=240, relief="ridge", bd=3)
left.grid(row=0, column=0, padx=20)
left.pack_propagate(False)
tk.Label(left, text="Original Image", bg="white").pack()
original_label = tk.Label(left, bg="lightgray")
original_label.pack(fill="both", expand=True, padx=5, pady=5)

right = tk.Frame(frame, bg="white", width=220, height=240, relief="ridge", bd=3)
right.grid(row=0, column=1, padx=20)
right.pack_propagate(False)
tk.Label(right, text="Stego Image", bg="white").pack()
stego_label = tk.Label(right, bg="lightgray")
stego_label.pack(fill="both", expand=True, padx=5, pady=5)

# Controls
controls = tk.Frame(root, bg="#ddeeff")
controls.pack(pady=15)

tk.Button(controls, text="Select Image", width=15, command=select_image).grid(row=0, column=0, padx=10)
tk.Label(controls, text="Character:", bg="#ddeeff").grid(row=0, column=1)
char_entry = tk.Entry(controls, width=5)
char_entry.grid(row=0, column=2, padx=10)
tk.Button(controls, text="Hide Data", width=15, command=hide_data).grid(row=0, column=3, padx=10)
tk.Button(controls, text="Extract Data", width=15, command=extract_data).grid(row=0, column=4, padx=10)

# Result
result_label = tk.Label(root, text="Hidden Character: ", font=("Arial", 14), bg="#ddeeff")
result_label.pack(pady=10)

speak_btn = tk.Button(root, text="Speak", width=15, command=speak, state="disabled")
speak_btn.pack()

root.mainloop()
