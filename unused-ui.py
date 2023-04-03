from tkinter import *
import tkinter as tk
from char import *

root = Tk()
#Set the geometry of tkinter frame
root.geometry("750x250")

# Initializations
min_id_length_entry = None
max_id_length_entry = None

# Number of rows of data
Label(root, text="Number of rows (int): ", font=('Century 10')).grid(row=0, column=2)
num_rows_entry = Entry(root)
num_rows_entry.grid(row=0, column=3)

def callback_id():
   global min_id_length_entry
   global max_id_length_entry
   Label(root, text="Minimum length (int): ", font=('Century 10')).grid(row=1, column=2)
   min_id_length_entry = Entry(root)
   min_id_length_entry.grid(row=1, column=3)
   Label(root, text="Maximum length (int): ", font=('Century 10')).grid(row=1, column=4)
   max_id_length_entry = Entry(root)
   max_id_length_entry.grid(row=1, column=5)

def callback_postcode():
   global num_of_postcode
   Label(root, text="Numebr of postcode ", font=('Century 10')).grid(row=2, column=2)
   num_of_postcode = Entry(root)
   num_of_postcode.grid(row=2, column=3)

def callback_random_string():
    global length_entry
    global num_strings_entry
    global pattern_entry
    # UI elements for random strings
    Label(root, text="Length (int): ", font=('Century 10')).grid(row=3, column=2)
    length_entry = Entry(root)
    length_entry.grid(row=3, column=3)

    Label(root, text="Number of strings (int): ", font=('Century 10')).grid(row=3, column=4)
    num_strings_entry = Entry(root)
    num_strings_entry.grid(row=3, column=5)

    # UI elements for pattern
    Label(root, text="Pattern (l for letter/d for digit/n for None): ", font=('Century 10')).grid(row=3, column=6)
    pattern_entry = Entry(root)
    pattern_entry.grid(row=3, column=7)

def callback_final():
    if id_flag.get():
        ids = id_generator()
        print(ids)

    if postcode_flag.get():
        postcode = postcode_generator(int(num_of_postcode.get()))
        print(postcode)

    if string_flag.get():
        length = int(length_entry.get())
        num_strings = int(num_strings_entry.get())

        # Read pattern input and convert to list of character types
        pattern_input = pattern_entry.get()
        pattern = ''
        if pattern_input:
            pattern = [{'l': 'letter', 'd': 'digit'}.get(char) for char in pattern_input]
        else:
            pattern = [None] * length

        generated_strings = generate_random_strings(length=length, pattern=pattern, num_strings=num_strings)
        print(generated_strings)


# ID
id_label = Label(root, text="ID: ", font=('Century 10 bold')).grid(row=1, column=0)
id_flag = tk.IntVar()
Radiobutton(root, 
            text="Yes",
            padx = 10, 
            variable=id_flag, 
            value=1,
            command=callback_id).grid(row=1, column=1)


# Postcode
postcode_label = Label(root, text="Postcode: ", font=('Century 10 bold')).grid(row=2, column=0)
postcode_flag = tk.IntVar()
Radiobutton(root, 
            text="Yes",
            padx = 10, 
            variable=postcode_flag, 
            value=1,
            command=callback_postcode).grid(row=2, column=1)

# String
string_label = Label(root, text="String: ", font=('Century 10 bold')).grid(row=3, column=0)
string_flag = tk.IntVar()
Radiobutton(root, 
            text="Yes",
            padx = 10, 
            variable=string_flag, 
            value=1,
            command=callback_random_string).grid(row=3, column=1)




#Create a Label and a Button widget
btn=Button(root, text="Generate Data", command= callback_final)
btn.grid(row=10, column=2)
# btn.pack(ipadx=10)
root.bind('<Return>',lambda event:callback_final())
root.mainloop()