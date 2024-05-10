import tkinter as tk
from tkinter import Canvas, Frame, Button


class FlowchartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flowchart")

        # sidebar
        self.sidebar = Frame(
            root, width=200, bg="#f0f0f0", height=600, relief="sunken", borderwidth=2
        )
        self.sidebar.pack(expand=False, fill="y", side="left", anchor="nw")

        # workspace
        self.canvas = Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(expand=True, fill="both", side="right")

        # buttons
        self.create_button("Line", self.use_line_tool)
        self.create_button("Rectangle", self.use_rectangle_tool)
        self.create_button("Diamond", self.use_rhombus_tool)
        self.create_button("Circle", self.use_circle_tool)
        self.create_button("Free draw", self.use_free_draw_tool)
        self.create_button("Text", self.use_text_tool)
        self.create_button("Clear", self.clear_canvas, bg="#ffdddd")

        # initialize mouse position
        self.start_x = self.start_y = 0
        self.drawing_tool = "none"
        self.shape = None
        self.text_id = None
        self.moving_text = False

        # bind mouse events to methods
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def create_button(self, text, command, bg="#ffffff"):
        btn = Button(
            self.sidebar, text=text, command=command, bg=bg, activebackground="#cccccc"
        )
        btn.pack(fill="x", padx=10, pady=5)

    def use_line_tool(self):
        self.drawing_tool = "line"

    def use_rectangle_tool(self):
        self.drawing_tool = "rectangle"

    def use_rhombus_tool(self):
        self.drawing_tool = "rhombus"

    def use_circle_tool(self):
        self.drawing_tool = "circle"

    def use_free_draw_tool(self):
        self.drawing_tool = "free draw"

    def use_text_tool(self):
        self.drawing_tool = "text"

    def clear_canvas(self):
        self.canvas.delete("all")

    def on_click(self, event):
        if self.drawing_tool == "text" and not self.moving_text:
            if self.text_id is None:
                self.text_id = self.canvas.create_text(
                    event.x,
                    event.y,
                    text="",
                    font=("Helvetica", 12),
                    fill="black",
                    anchor="nw",
                )
                self.canvas.focus_set()
                self.canvas.bind("<Key>", self.text_input)
            else:
                # drag text
                item = self.canvas.find_closest(event.x, event.y)
                if item and item[0] == self.text_id:
                    self.start_x, self.start_y = event.x, event.y
                    self.moving_text = True
        else:
            self.create_shape(event)

    def text_input(self, event):
        if event.keysym.lower() == "return":
            self.canvas.unbind("<Key>")
            self.text_id = None
        elif event.keysym == "BackSpace":
            current_text = self.canvas.itemcget(self.text_id, "text")
            self.canvas.itemconfig(self.text_id, text=current_text[:-1])
        else:
            current_text = self.canvas.itemcget(self.text_id, "text")
            self.canvas.itemconfig(self.text_id, text=current_text + event.char)

    def on_drag(self, event):
        if self.drawing_tool == "text" and self.moving_text:
            dx, dy = event.x - self.start_x, event.y - self.start_y
            self.canvas.move(self.text_id, dx, dy)
            self.start_x, self.start_y = event.x, event.y
        elif self.drawing_tool != "text":
            self.update_shape_coords(event)

    def on_release(self, event):
        if self.drawing_tool == "text" and self.moving_text:
            self.moving_text = False
        else:
            self.shape = None

    def create_shape(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.drawing_tool == "rectangle":
            self.shape = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y, outline="black"
            )
        elif self.drawing_tool == "rhombus":
            dx = abs(event.y - self.start_y)
            self.shape = self.canvas.create_polygon(
                self.start_x,
                self.start_y - dx,
                self.start_x + dx,
                self.start_y,
                self.start_x,
                self.start_y + dx,
                self.start_x - dx,
                self.start_y,
                outline="black",
                fill="",
            )
        elif self.drawing_tool == "circle":
            self.shape = self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y, outline="black"
            )
        elif self.drawing_tool == "line":
            self.shape = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y, fill="black", width=2
            )
        elif self.drawing_tool == "free draw":
            self.shape = self.canvas.create_line(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                fill="black",
                width=2,
                smooth=True,
            )

    def update_shape_coords(self, event):
        if self.drawing_tool == "rectangle" or self.drawing_tool == "circle":
            self.canvas.coords(self.shape, self.start_x, self.start_y, event.x, event.y)
        elif self.drawing_tool == "rhombus":
            dx = abs(event.x - self.start_x)
            dy = abs(event.y - self.start_y)
            self.canvas.coords(
                self.shape,
                self.start_x,
                self.start_y - dy,
                self.start_x + dx,
                self.start_y,
                self.start_x,
                self.start_y + dy,
                self.start_x - dx,
                self.start_y,
            )
        elif self.drawing_tool == "free draw":
            coords = self.canvas.coords(self.shape)
            coords.extend([event.x, event.y])
            self.canvas.coords(self.shape, *coords)
        elif self.drawing_tool == "line" and self.shape is not None:
            self.canvas.coords(self.shape, self.start_x, self.start_y, event.x, event.y)


if __name__ == "__main__":
    root = tk.Tk()
    app = FlowchartApp(root)
    root.mainloop()
