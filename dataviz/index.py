import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter, AutoDateLocator
from datetime import timedelta


class DataVizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Data Viz!")

        self.control_frame = tk.Frame(master)
        self.control_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        # "Upload CSV"
        self.load_csv_button = tk.Button(
            self.control_frame, text="Upload CSV", command=self.load_csv
        )
        self.load_csv_button.pack(side=tk.LEFT, padx=(0, 20))

        # label and dropdown to select chart
        tk.Label(self.control_frame, text="Chart:").pack(side=tk.LEFT)
        self.plot_type_var = tk.StringVar()
        self.plot_type_selector = ttk.Combobox(
            self.control_frame,
            textvariable=self.plot_type_var,
            state="readonly",
            values=("Scatter Plot", "Line Chart", "Bar Chart"),
        )
        self.plot_type_selector.pack(side=tk.LEFT, padx=(5, 5))

        # label and dropdown to select x axis
        tk.Label(self.control_frame, text="X-axis:").pack(side=tk.LEFT, padx=(20, 0))
        self.x_axis_var = tk.StringVar()
        self.x_axis_selector = ttk.Combobox(
            self.control_frame, textvariable=self.x_axis_var, state="readonly", width=20
        )
        self.x_axis_selector.pack(side=tk.LEFT, padx=(5, 5))

        # label and dropdown to select y axis
        tk.Label(self.control_frame, text="Y-axis:").pack(side=tk.LEFT, padx=(20, 0))
        self.y_axis_var = tk.StringVar()
        self.y_axis_selector = ttk.Combobox(
            self.control_frame, textvariable=self.y_axis_var, state="readonly", width=20
        )
        self.y_axis_selector.pack(side=tk.LEFT, padx=(5, 20))

        # "Generate"
        self.plot_button = tk.Button(
            self.control_frame,
            text="Generate",
            command=self.plot_graph,
            bg="#3777F7",
            fg="white",
        )
        self.plot_button.pack(side=tk.RIGHT, padx=(0, 10))

        # PanedWindow to resize
        self.paned_window = ttk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame table and scrollbar
        self.table_frame = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.table_frame, weight=1)

        # Frame chart
        self.plot_frame = ttk.Frame(self.paned_window, width=400)
        self.paned_window.add(self.plot_frame, weight=3)

        # initialize df
        self.df = None

        # placeholder canvas and tree widget
        self.canvas = None
        self.tree = None

    # function to show table with data
    def display_table(self, dataframe):
        if self.tree:
            self.tree.destroy()
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.table_frame, show="headings", selectmode="browse")
        self.vsb = ttk.Scrollbar(
            self.table_frame, orient="vertical", command=self.tree.yview
        )
        self.hsb = ttk.Scrollbar(
            self.table_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree["columns"] = dataframe.columns.tolist()
        for column in dataframe.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor=tk.CENTER, width=100)

        for _, row in dataframe.iterrows():
            self.tree.insert("", tk.END, values=row.tolist())

    # function to upload csv
    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            columns = self.df.columns.tolist()
            self.x_axis_selector["values"] = columns
            self.y_axis_selector["values"] = columns
            self.plot_type_selector["values"] = [
                "Scatter Plot",
                "Line Chart",
                "Bar Chart",
            ]
            self.display_table(self.df)

    # function to generate selected chart
    def plot_graph(self):
        if (
            self.df is not None
            and self.x_axis_var.get()
            and self.y_axis_var.get()
            and self.plot_type_var.get()
        ):
            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)

            # verifica se l'asse x contiene date
            x_data = self.df[self.x_axis_var.get()]
            try:
                x_data_converted = pd.to_datetime(x_data)
                x_is_date = True
                if self.plot_type_var.get() != "Scatter Plot":
                    ax.xaxis.set_major_locator(AutoDateLocator())
                    ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            except ValueError:
                x_is_date = False
                x_data_converted = x_data

            if self.plot_type_var.get() == "Line Chart":
                ax.plot(
                    x_data_converted,
                    self.df[self.y_axis_var.get()],
                    label=self.y_axis_var.get(),
                )
            elif self.plot_type_var.get() == "Bar Chart":
                if x_is_date:
                    date_range = (x_data_converted.max() - x_data_converted.min()).days
                    bar_width = max(1, date_range / len(self.df) * 0.8)
                    ax.bar(
                        x_data_converted,
                        self.df[self.y_axis_var.get()],
                        width=timedelta(days=int(bar_width)),
                        label=self.y_axis_var.get(),
                        align="center",
                    )
                else:
                    ax.bar(
                        x_data,
                        self.df[self.y_axis_var.get()],
                        label=self.y_axis_var.get(),
                    )
            elif self.plot_type_var.get() == "Scatter Plot":
                ax.scatter(
                    x_data_converted,
                    self.df[self.y_axis_var.get()],
                    label=self.y_axis_var.get(),
                )

            if self.plot_type_var.get() != "Bar Chart" and x_is_date:
                fig.autofmt_xdate()

            ax.set_xlabel(self.x_axis_var.get())
            ax.set_ylabel(self.y_axis_var.get())
            ax.legend()

            self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = DataVizApp(root)
    root.mainloop()
