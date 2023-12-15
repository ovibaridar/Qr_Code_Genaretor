import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)

# Initialize a variable to track the current theme
current_theme = "forest-dark"
font = ("Times New Roman CE", 10)

# Variable to track whether an image is displayed in frame2
image_displayed = False


def toggle():
    global current_theme
    if current_theme == "forest-dark":
        if "forest-light" not in style.theme_names():
            root.tk.call('source', 'forest-light.tcl')
        style.theme_use('forest-light')
        current_theme = "forest-light"
    else:
        style.theme_use('forest-dark')
        current_theme = "forest-dark"


def creat():
    global image_displayed
    # Clear the existing QR code image
    for widget in frame2.winfo_children():
        widget.destroy()

    text = entry1.get()
    entry1.delete(0, "end")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(text)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image
    filename = 'img/qrcode.png'
    img.save("img/qrcode.png")

    # Display the new QR code image
    img = Image.open(filename)
    img.thumbnail((200, 200))  # Resize the image
    photo = ImageTk.PhotoImage(img)

    l1 = ttk.Label(frame2, image=photo)
    l1.image = photo  # Keep a reference to the image to prevent it from being garbage collected
    l1.pack()

    # Update the variable to indicate that an image is displayed
    image_displayed = True

    # Save the image object to make it accessible in save_image function
    creat.img = img


def save_image():
    if image_displayed:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            creat.img.save(file_path)
    else:
        messagebox.showwarning("Warning", "No image to save. Create a QR code first.")


style = ttk.Style(root)
if "forest-dark" not in style.theme_names():
    root.tk.call('source', 'forest-dark.tcl')
style.theme_use('forest-dark')

frame1 = ttk.Frame(root, height=400, width=600)
frame1.pack()
mode = ttk.Checkbutton(frame1, style="Switch", command=toggle)
mode.place(x=550, y=10)
frame2 = ttk.Frame(frame1, height=200, width=200, relief="groove", borderwidth=2)
frame2.propagate(0)
frame2.place(x=380, y=80)

entry1 = ttk.Entry(frame1, font=30, width=30)
entry1.place(x=60, y=80)

button_create = ttk.Button(text='Create', width=15, command=lambda: creat())
button_create.place(x=140, y=130)

button_save = ttk.Button(text='Save Image', width=15, command=save_image)
button_save.place(x=140, y=180)

root.bind("<Return>", lambda event=None: creat())

root.mainloop()
