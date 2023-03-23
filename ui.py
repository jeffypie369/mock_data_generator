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

def callback_final():
    if id_flag.get():
        ids = id_generator()
        print(ids)

    if postcode_flag.get():
        postcode = postcode_generator(int(num_of_postcode.get()))
        print(postcode)


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




#Create a Label and a Button widget
btn=Button(root, text="Generate Data", command= callback_final)
btn.grid(row=3, column=2)
# btn.pack(ipadx=10)
root.bind('<Return>',lambda event:callback_final())
root.mainloop()