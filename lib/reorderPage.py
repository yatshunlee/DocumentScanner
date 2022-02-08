import tkinter as tk
from tkinter import *
from .documentScanner import *
from .outputPdf import *

def order(filePaths, function):
    class MyListbox(tk.Listbox):
        def __init__(self, *args, **kwargs):
            tk.Listbox.__init__(self, *args, **kwargs)
            self.bind("<Home>", lambda *args: self.select(0))
            self.bind("<End>", lambda *args: self.select("end"))

        def move_up(self, anchor):
            """ Moves the item at position pos up by one """
            pos = self.index(anchor)
            item = self.get(anchor)
            count = listbox.size()
            if pos == 0:
                return

            listbox.delete(pos)
            listbox.insert(pos - 1, item)

            del filePaths[pos]
            filePaths.insert(pos - 1, item)

        def move_down(self, anchor):
            """ Moves the item at position pos up by one """
            pos = self.index(anchor)
            item = self.get(anchor)
            count = listbox.size()
            if pos == count - 1:
                return

            listbox.delete(pos)
            listbox.insert(pos + 1, item)

            del filePaths[pos]
            filePaths.insert(pos + 1, item)


    def can_proceed():
        try:
            main.destroy()
        except:
            pass
        # save_dir = filedialog.askdirectory(title='Saving directory')
        save_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            title="Save as",
            filetypes=[('pdf file', '*.pdf')]
        )
        if function=='convert' and save_filename:
            for f in filePaths:
                messagebox.showinfo(
                    title='Message',
                    message='''Press ENTER to go. Press ESC to stop the process.
[REMINDER] You can press E to edit the range of interest in the auto document detecting process.'''
                )
                documentScanner(f)
            jpgToPdf(filePaths, save_filename)
        if function=='merge' and save_filename:
            merge(filePaths, save_filename)

    if len(filePaths)==1 and function=='convert':
        can_proceed()

    main = tk.Tk()
    main.iconbitmap('Martin-Berube-Square-Animal-Duck.ico')
    main.title('Select order')
    main.geometry('600x300')
    listbox = MyListbox(main, selectmode="extended", width = 70)

    filePaths = list(filePaths)
    for x in filePaths:
        listbox.insert("end", x)

    listbox.pack(side=LEFT, fill=BOTH)

    scrollbar = Scrollbar(main)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    move_up_btn = Button(main, text=" ↑ ", command=lambda listbox=listbox: listbox.move_up(ANCHOR))
    move_up_btn.pack(pady=20,)
    move_down_btn = Button(main, text=" ↓ ", command=lambda listbox=listbox: listbox.move_down(ANCHOR))
    move_down_btn.pack(pady=5)
    move_down_btn = Button(main, text="ok!", command=can_proceed)
    move_down_btn.pack(pady=20)

    tk.mainloop()