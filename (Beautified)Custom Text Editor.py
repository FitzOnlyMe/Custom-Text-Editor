import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

text_contents = dict()

def create_file(content="", title="Untitled"):
    container = ttk.Frame(notebook)
    container.pack()

    text_area = tk.Text(container, font=("Consolas", 12), bg="#fefefe", fg="#333", wrap="word", undo=True)
    text_area.insert("end", content)
    text_area.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    notebook.add(container, text=title)
    notebook.select(container)
    container.focus()

    text_contents[str(text_area)] = hash(content)

    text_scroll = ttk.Scrollbar(container, orient="vertical", command=text_area.yview, style="Vertical.TScrollbar")
    text_scroll.pack(side="right", fill="y", padx=2, pady=2)
    text_area["yscrollcommand"] = text_scroll.set


def check_for_changes():
    current = get_text_widget()
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if not name.endswith("*"):
            notebook.tab("current", text=name + "*")
    else:
        if name.endswith("*"):
            notebook.tab("current", text=name[:-1])


def get_text_widget():
    tab_widget = root.nametowidget(notebook.select())
    text_widget = tab_widget.winfo_children()[0]
    return text_widget


def close_current_tab():
    current_tab = notebook.select()
    if current_tab_unsaved() and not confirm_close():
        return

    if len(notebook.tabs()) == 1:
        create_file()

    notebook.forget(current_tab)


def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get("1.0", "end-1c")
    return hash(content) != text_contents[str(text_widget)]


def confirm_close():
    return messagebox.askyesno(
        message="Close with unsaved changes?",
        icon="question",
        title="Unsaved Changes!"
    )


def confirm_quit():
    unsaved = False

    for tab in notebook.tabs():
        tab_widget = root.nametowidget(tab)
        text_widget = tab_widget.winfo_children()[0]
        content = text_widget.get("1.0", "end-1c")

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved and not confirm_close():
        return

    root.destroy()


def save_file():
    file_path = filedialog.asksaveasfilename()

    if not file_path:
        return

    try:
        filename = os.path.basename(file_path)
        text_widget = get_text_widget()
        content = text_widget.get("1.0", "end-1c")

        with open(file_path, "w") as file:
            file.write((content))
    except (AttributeError, FileNotFoundError):
        print("Save Cancelled!")
        return

    notebook.tab("current", text=filename)
    text_contents[str(text_widget)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    try:
        filename = os.path.basename(file_path)

        with open(file_path, "r") as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print("Open Cancelled!")
        return

    create_file(content, filename)


def show_about_info():
    messagebox.showinfo(
        title="About",
        message="A simple tabbed text editor made with Python & Tkinter"
    )


def toggle_dark_mode():
    if style.theme_use() == "clam":
        style.theme_use("alt")
        root.config(bg="#2e2e2e")
        main.config(bg="#2e2e2e")
    else:
        style.theme_use("clam")
        root.config(bg="#f0f0f0")
        main.config(bg="#f0f0f0")


root = tk.Tk()
root.title("Marks Text Editor")
root.option_add("*tearOff", False)
#root.iconbitmap('your_icon.ico')  # Set your own icon file

style = ttk.Style()
style.theme_use("clam")  # You can switch to "alt" for dark mode or others like "default"
style.configure("TNotebook", background="#f0f0f0")
style.configure("TNotebook.Tab", padding=[10, 5], font=("Helvetica", 10))
style.configure("Vertical.TScrollbar", gripcount=0, background="#888", darkcolor="#555", lightcolor="#bbb", troughcolor="#ddd", bordercolor="#888", arrowcolor="#555")

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=10, pady=(10, 0))

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)
menubar.add_cascade(menu=file_menu, label="File")
menubar.add_cascade(menu=help_menu, label="Help")

file_menu.add_command(label="New", command=create_file, accelerator="Ctrl + N")
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl + O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl + S")
file_menu.add_command(label="Close Tab", command=close_current_tab, accelerator="Ctrl + W")
file_menu.add_command(label="Exit", command=confirm_quit, accelerator="Ctrl + Q")
file_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)

help_menu.add_command(label="About", command=show_about_info)

notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True, padx=5, pady=5)

create_file()

status = ttk.Label(root, text="Ready", anchor="w", relief="sunken", padding=5)
status.pack(side="bottom", fill="x")

root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-q>", lambda event: confirm_quit())
root.bind("<Control-w>", lambda event: close_current_tab())

root.mainloop()
