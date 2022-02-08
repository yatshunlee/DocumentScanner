import tkinter as tk
from tkinter import filedialog

from .documentScanner import *
from .jpgToPdf import *
from .reorderPdf import *

window = tk.Tk()
window.title('Scan Duck App')
window.geometry('400x300')
window.config(background='#5088F4')

def convert():
    files = filedialog.askopenfilename(title='Select files',multiple=True)

    filePaths = window.tk.splitlist(files)
    if filePaths:
        messagebox.showinfo(
            title='Message',
            message='''Press ENTER to go. Press ESC to stop the process.
[REMINDER] You can press E to edit the range of interest in the auto document detecting process.'''
        )
        for f in filePaths:
            documentScanner(f)
        save_dir = filedialog.askdirectory(title='Saving directory')
        jpgToPdf(save_dir)
        messagebox.showinfo(title='Message', message=f'Done! The pdf file is stored in {save_dir}')

def combine():
    files = filedialog.askopenfilename(title='Select files', multiple=True)
    filePaths = window.tk.splitlist(files)

    if filePaths:
        # merge(filePaths, save_dir)
        sort_pdf(filePaths)
        messagebox.showinfo(title='Message', message=f'Done! The merged pdf file is stored in {save_dir}')

header1_label = tk.Label(window,
                        text='img2pdf converter',
                        font = ('Arial', 24),
                        fg='white',bg='#5088F4',
                        width = 15, height = 2)
header1_label.pack()

convert_img_to_pdf_btn = tk.Button(window,
                                   text='convert', relief="raised",
                                   fg='white', bg='#5088F4',
                                   command = convert)
convert_img_to_pdf_btn.pack()

header2_label = tk.Label(window,
                        text='combine multiple pdf',
                        font = ('Arial', 24),
                        fg='white', bg='#5088F4',
                        width = 15, height = 2)
header2_label.pack()

combine_pdf_btn = tk.Button(window,
                            text='combine', relief="raised",
                            fg='white', bg='#5088F4',
                            command = combine)
combine_pdf_btn.pack()

window.mainloop()