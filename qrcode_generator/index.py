import tkinter as tk
from tkinter import ttk
import qrcode
from PIL import Image, ImageTk


class QRCodeGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("QR Code Generator")

        # user input
        self.input_entry = ttk.Entry(self.master, width=40)
        self.input_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # generate button
        generate_button = ttk.Button(
            self.master, text="Generate QR Code", command=self.generate_qr_code
        )
        generate_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # Canvas to show QR code
        self.qr_canvas = tk.Canvas(self.master, width=200, height=200)
        self.qr_canvas.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    def generate_qr_code(self):
        data = self.input_entry.get()
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")

            # save QR code image
            qr_img.save("qr_code_generated.png")

            # show QR code on canvas
            self.display_qr_code(qr_img)

    def display_qr_code(self, qr_img):
        # convert PIL Image to PhotoImage for Tkinter
        tk_img = ImageTk.PhotoImage(qr_img)

        # update canvas with new image
        self.qr_canvas.config(width=tk_img.width(), height=tk_img.height())
        self.qr_canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)
        self.qr_canvas.image = tk_img


def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
