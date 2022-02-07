import tkinter as tk
from tkinter import filedialog, Listbox, Button

popup = tk.Tk()
popup.title('Select')
popup.geometry('400x300')
popup.config(background='#5088F4')

files = filedialog.askopenfilename(title='Select files',multiple=True)
filePaths = popup.tk.splitlist(files)
pdfs = []

for f in filePaths:
    pdfs.append(f)

if not pdfs:
    import menu
    popup.destroy()

else:
    listbox = Listbox(popup)

    # Function for printing the selected listbox value(s)
    def selected_item():
        # Traverse the tuple returned by curselection method and print corresponding value(s) in the listbox
        for i in listbox.curselection():
            print(listbox.get(i))

    # Create a button widget and map the command parameter to selected_item function
    btn = Button(popup, text='Print Selected', command=selected_item)
    btn.pack(side='bottom')

    for i, pdf in enumerate(pdfs):
        listbox.insert(i+1, pdf)

    # save_dir = filedialog.askdirectory(title='Saving directory')
    # merge(filePaths,save_dir)
    # messagebox.showinfo(title='Message', message=f'Done! The merged pdf file is stored in {save_dir}')

    listbox.pack()
    popup.mainloop()
