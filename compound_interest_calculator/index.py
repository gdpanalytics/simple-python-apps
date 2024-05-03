import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_compound_interest():
    # user input
    P = float(principal_var.get())
    r = float(rate_var.get()) / 100
    t = int(years_var.get())

    # formula compound interest
    n = 1
    amounts = [P * (1 + r / n) ** (n * i) for i in range(t + 1)]

    # update results
    total_amount = amounts[-1]
    interest_earned = total_amount - P
    total_amount_var.set(f"${total_amount:.2f}")
    interest_earned_var.set(f"${interest_earned:.2f}")

    # update chart
    ax.clear()
    ax.plot(amounts, marker="o", linestyle="-", color="b")
    ax.set_title("Capital over time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Capital (€)")
    ax.grid(True)
    canvas.draw()


# main window
root = tk.Tk()
root.title("Compound interest calculator")

# create variables
principal_var = tk.StringVar()
rate_var = tk.StringVar()
years_var = tk.StringVar()
total_amount_var = tk.StringVar()
interest_earned_var = tk.StringVar()

# layout
root.columnconfigure(1, weight=1)

# frame input output
frame = ttk.Frame(root)
frame.grid(column=0, row=0, sticky=tk.NSEW)

# initial capital
principal_label = ttk.Label(frame, text="Initial capital (€):")
principal_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
principal_entry = ttk.Entry(frame, textvariable=principal_var)
principal_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

# annual interest rate
rate_label = ttk.Label(frame, text="Annual interest rate (%):")
rate_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
rate_entry = ttk.Entry(frame, textvariable=rate_var)
rate_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

# number of years
years_label = ttk.Label(frame, text="Number of years:")
years_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
years_entry = ttk.Entry(frame, textvariable=years_var)
years_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

# compute
calculate_button = ttk.Button(
    frame, text="Compute", command=calculate_compound_interest
)
calculate_button.grid(column=1, row=3, padx=5, pady=20, sticky=tk.EW)

# final capital
total_amount_label = ttk.Label(frame, text="Final capital (€):")
total_amount_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)
total_amount_entry = ttk.Entry(frame, textvariable=total_amount_var, state="readonly")
total_amount_entry.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

# interest earned
interest_earned_label = ttk.Label(frame, text="Interest earned (€):")
interest_earned_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)
interest_earned_entry = ttk.Entry(
    frame, textvariable=interest_earned_var, state="readonly"
)
interest_earned_entry.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

# frame matplotlib
chart_frame = ttk.Frame(root)
chart_frame.grid(column=1, row=0, sticky=tk.NSEW)

# set up matplotlib
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# start tkinter
root.mainloop()
