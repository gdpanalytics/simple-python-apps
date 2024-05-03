import tkinter as tk
import sqlite3


class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")

        # db connection
        self.conn = sqlite3.connect("todo_app.db")
        self.c = self.conn.cursor()
        self.create_table()

        self.tasks = self.load_tasks()

        # task input
        self.task_entry = tk.Entry(self.master, width=30)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        # button "Add task"
        add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=1, padx=10, pady=10)

        # box task list
        self.task_listbox = tk.Listbox(
            self.master, selectmode=tk.SINGLE, height=10, width=40
        )
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.update_task_list()

        # button "Remove task"
        remove_button = tk.Button(
            self.master, text="Remove Task", command=self.remove_task
        )
        remove_button.grid(row=2, column=0, padx=10, pady=10)

        # button "Clear all"
        clear_button = tk.Button(
            self.master, text="Clear All", command=self.clear_tasks
        )
        clear_button.grid(row=2, column=1, padx=10, pady=10)

    # create a table if not exists
    def create_table(self):
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS tasks
                          (task TEXT)"""
        )
        self.conn.commit()

    # load tasks
    def load_tasks(self):
        self.c.execute("SELECT * FROM tasks")
        return [task[0] for task in self.c.fetchall()]

    # add task
    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.c.execute("INSERT INTO tasks VALUES (?)", (task,))
            self.conn.commit()
            self.update_task_list()
            self.task_entry.delete(0, tk.END)

    # remove task
    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = int(selected_task_index[0])
            self.c.execute(
                "DELETE FROM tasks WHERE task=?", (self.tasks[selected_task_index],)
            )
            self.conn.commit()
            del self.tasks[selected_task_index]
            self.update_task_list()

    # clear task
    def clear_tasks(self):
        self.tasks = []
        self.c.execute("DELETE FROM tasks")
        self.conn.commit()
        self.update_task_list()

    # update list
    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    # close connection
    def __del__(self):
        self.conn.close()


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
