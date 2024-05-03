import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calendar App")
        self.root.geometry("650x400")
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.events = {}

        self.root.grid_rowconfigure(1, weight=1)
        for i in range(8):
            self.root.grid_columnconfigure(i, weight=1)

        self.cal = Calendar(
            self.root,
            selectmode="day",
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day,
            firstweekday="monday",
        )
        self.cal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.cal.bind("<<CalendarSelected>>", self.display_events)

        self.event_listbox = tk.Listbox(self.root, height=8, width=50)
        self.event_listbox.grid(
            row=0, column=1, columnspan=7, padx=10, pady=10, sticky="nsew"
        )

        self.event_details_frame = ttk.Frame(self.root)
        self.event_details_frame.grid(
            row=1, column=0, columnspan=8, padx=10, pady=10, sticky="ew"
        )
        self.event_name = tk.StringVar()
        self.event_date = tk.StringVar(value=self.cal.get_date())
        self.event_time = tk.StringVar()
        self.event_location = tk.StringVar()
        self.event_description = tk.StringVar()

        ttk.Label(self.event_details_frame, text="New event:").grid(row=0, column=0)
        ttk.Entry(self.event_details_frame, textvariable=self.event_name).grid(
            row=0, column=1, sticky="ew"
        )

        ttk.Label(self.event_details_frame, text="Date & Time:").grid(row=0, column=2)
        ttk.Entry(
            self.event_details_frame, textvariable=self.event_date, width=10
        ).grid(row=0, column=3, sticky="ew")
        ttk.Entry(
            self.event_details_frame, textvariable=self.event_time, width=10
        ).grid(row=0, column=4, sticky="ew")

        ttk.Label(self.event_details_frame, text="Location:").grid(row=0, column=5)
        ttk.Entry(self.event_details_frame, textvariable=self.event_location).grid(
            row=0, column=6, columnspan=2, sticky="ew"
        )

        ttk.Label(self.event_details_frame, text="Description:").grid(row=1, column=0)
        ttk.Entry(
            self.event_details_frame, textvariable=self.event_description, width=70
        ).grid(row=1, column=1, columnspan=7, sticky="ew")

        ttk.Button(
            self.event_details_frame, text="Save event", command=self.save_event
        ).grid(row=2, column=2, pady=10)
        ttk.Button(
            self.event_details_frame, text="Remove event", command=self.remove_event
        ).grid(row=2, column=4, pady=10)

    def save_event(self):
        event_details = {
            "name": self.event_name.get(),
            "date": self.event_date.get(),
            "time": self.event_time.get(),
            "location": self.event_location.get(),
            "description": self.event_description.get(),
        }
        date_key = self.event_date.get()
        if date_key in self.events:
            self.events[date_key].append(event_details)
        else:
            self.events[date_key] = [event_details]
        self.display_events()

    def remove_event(self):
        try:
            selected_index = self.event_listbox.curselection()[0]
            selected_date = self.cal.get_date()
            del self.events[selected_date][selected_index]
            self.event_listbox.delete(selected_index)
        except IndexError:
            messagebox.showerror("Error", "Select an event to remove.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_events(self, event=None):
        selected_date = self.cal.get_date()
        self.event_date.set(selected_date)
        self.event_listbox.delete(0, tk.END)
        if selected_date in self.events:
            for event in self.events[selected_date]:
                event_info = (
                    f"{event['name']} at {event['time']} in {event['location']}"
                )
                self.event_listbox.insert(tk.END, event_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
