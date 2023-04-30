from tkinter import *
from tkinter import filedialog
from tkinter import font

root = Tk()
root.title("Text Editor")
root.iconbitmap()
root.geometry("480x400")

# Set variable for open file name
global open_status_name
open_status_name = False

global selected
selected = False


# New File Function
def new_file():
    # Delete Previous Text
    my_text.delete("1.0", END)
    root.title('New File - Text Editor')
    status_bar.config(text="New File        ")


# Open File Function
def open_file():
    # Delete Previous Text
    my_text.delete("1.0", END)

    # Grab Filename
    text_file = filedialog.askopenfilename(initialdir="C:/Users/shubh/OneDrive/Documents/", title="Open File",
                                           filetypes=(
                                           ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"),
                                           ("All Files", "*.*")))
    # Change the directory address as per yours

    # Check if already exists
    if text_file:
        global open_status_name
        open_status_name = text_file

    # Update Status Bar
    name = text_file
    name = name.replace("C:/Users/shubh/", "")
    root.title(f'{name} - Text Editor')
    status_bar.config(text=f'Opened: {name}        ')

    # Open the File
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    # Add file to textbox
    my_text.insert(END, stuff)
    # Close the opened file
    text_file.close()


# Save As File Function
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Users/shubh/OneDrive/Documents/",
                                             title="Save File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        # Update Status Bar
        name = text_file
        name = name.replace("C:/Users/shubh/", "")
        root.title(f'Saved: {name} - Text Editor')
        status_bar.config(text=f'Saved: {name}        ')

        # Save the file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        # Close the file
        text_file.close()


# Save File Function
def save_file():
    global open_status_name
    if open_status_name:
        # Save the file
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))

        # Close the file
        text_file.close()

        # Update Status Bar
        name = open_status_name
        name = name.replace("C:/Users/shubh/", "")
        root.title(f'Saved: {name} - Text Editor')
        status_bar.config(text=f'Saved: {name}        ')

    else:
        save_as_file()


# Cut Text
def cut_text(e):
    global selected
    # Check to see if we used keyboard shortcut
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Grab selected text from text box
            selected = my_text.selection_get()
            # Delete selected text from text box
            my_text.delete("sel.first", "sel.last")
            # Clears clipboard and then append
            root.clipboard_clear()
            root.clipboard_append(selected)


# Copy Text:
def copy_text(e):
    global selected
    # Check to see if we used keyboard shortcut
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        # Grab selected text from text box
        selected = my_text.selection_get()
        # Clears clipboard and then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# Paste Text:
def paste_text(e):
    global selected

    # Check to see if we used keyboard shortcut
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# Bold Text
def bold_text():
    # Create Bold Font
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    # Configure a tag
    my_text.tag_configure("bold", font=bold_font)

    # Define current tag
    current_tags = my_text.tag_names("sel.first")

    # To see if tag has been set
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")


# Italics Text
def italics_text():
    # Create Italics Font
    italics_font = font.Font(my_text, my_text.cget("font"))
    italics_font.configure(slant="italic")

    # Configure a tag
    my_text.tag_configure("italic", font=italics_font)

    # Define current tag
    current_tags = my_text.tag_names("sel.first")

    # To see if tag has been set
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")




# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scroll Bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Horizontal Scroll Bar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# Create text Box
my_text = Text(my_frame, width=50, height=15, font=("Times New Roman", 16), selectbackground="Blue",
               selectforeground="White", undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=hor_scroll.set)
my_text.pack()

# Configure Scroll Bar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="    (Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="    (Ctrl+c)")
edit_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="    (Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="    (Ctrl+z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="    (Ctrl+y)")

# Add Format Menu
format_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Format", menu=format_menu)
format_menu.add_command(label="Bold", command=bold_text)
format_menu.add_command(label="Italics", command=italics_text)

# Add Status Bar
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# Edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

root.mainloop()
