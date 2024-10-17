import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

text_contents = dict()

def create_file(content = "", title = "Untitled"):
    container = ttk.Frame(notebook)
    container.pack()

    text_area = tk.Text(container)
    text_area.insert("end", content)
    text_area.pack(side = "left", fill = "both", expand = True)

    notebook.add(container, text = title)
    notebook.select(container)
    container.focus()

    text_contents[str(text_area)] = hash(content)

    text_scroll = ttk.Scrollbar(container, orient="vertical", command = text_area.yview) # yview is used to modify the Y (delta) of the container
    text_scroll.pack(side = "right", fill = "y")
    text_area["yscrollcommand"] = text_scroll.set


def check_for_changes():
    current = get_text_widget()
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if not name.endswith("*"):
            notebook.tab("current", text=name + "*")  # if the file is BOTH unsaved & DOES NOT have a * at the end of the file name, this will add the *
    else:
        if name.endswith("*"):
            notebook.tab("current", text=name[:-1])  # Remove asterisk if no changes



def get_text_widget():
    tab_widget = root.nametowidget(notebook.select())
    text_widget = tab_widget.winfo_children()[0] # goes into tab widget, gets the widget & the children of the widget
    return text_widget


def close_current_tab():
    current_tab = notebook.select()  # Get the currently selected tab
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
        message = "Close with unsaved changes?",
        icon = "question",
        title = "Unsaved Changes!"
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
        return  # User canceled save dialog

    try:
        filename = os.path.basename(file_path)
        text_widget = get_text_widget()
        content = text_widget.get("1.0","end-1c")

        with open(file_path, "w") as file:
            file.write((content))
    except (AttributeError, FileNotFoundError):
        print("Save Cancelled!")
        return
    notebook.tab("current", text = filename) # changes name of current tab to the file name

    text_contents[str(text_widget)] = hash(content)


def open_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return  # User canceled open dialog

    try:
        filename = os.path.basename(file_path)

        with open (file_path, "r") as file:
            content = file.read()

    except (AttributeError, FileNotFoundError):
        print("Open Cancelled!")
        return

    create_file(content, filename)


def show_about_info():
    messagebox.showinfo(
        title = "About",
        message = "A simple tabbed text editor made with Python & Tkinter"
    )


root = tk.Tk()
root.title("Marks Text Editor")
root.option_add("*tearOff", False) # enables you to change the behaviour of certain elements/things within different OS (*tearOff means menu items cannot be removed)


main = ttk.Frame(root)
main.pack(fill = "both", expand = True, padx = 1, pady = (4, 0))

menubar = tk.Menu()
root.config(menu = menubar)

file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)
menubar.add_cascade(menu = file_menu, label = "File")
menubar.add_cascade(menu = help_menu, label = "Help")

file_menu.add_command(label = "New", command = create_file, accelerator= "Ctrl + N")
file_menu.add_command(label = "Open...", command = open_file, accelerator= "Ctrl + O")
file_menu.add_command(label = "Save", command = save_file, accelerator= "Ctrl + S")
file_menu.add_command(label = "Close Tab", command = close_current_tab, accelerator= "Ctrl + W")
file_menu.add_command(label = "Exit", command = confirm_quit, accelerator= "Ctrl + Q")

help_menu.add_command(label = "About", command = show_about_info)

notebook = ttk.Notebook(main)
notebook.pack(fill = "both", expand = True)
create_file()


root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file()) # When you bind a shortcut, the 2nd argument must be a function that takes in an even & does something
root.bind("<Control-o>", lambda event: open_file()) # bound to the root means that shortcut will always run
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-q>", lambda event: confirm_quit())
root.bind("<Control-w>", lambda event: close_current_tab())


root.mainloop()