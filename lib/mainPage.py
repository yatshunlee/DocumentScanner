import tkinter as tk
from tkinter import filedialog
from .reorderPage import *

window = tk.Tk()
window.title('Scan Duck App')
window.iconbitmap('Martin-Berube-Square-Animal-Duck.ico')
window.geometry('400x300')
window.config(background='#5088F4')

def convert():
    files = filedialog.askopenfilename(title='Select files',multiple=True)
    filePaths = window.tk.splitlist(files)
    if filePaths:
        order(filePaths, function='convert')

def combine():
    files = filedialog.askopenfilename(title='Select files', multiple=True)
    filePaths = window.tk.splitlist(files)

    if filePaths:
        # merge(filePaths, save_dir)
        order(filePaths, function='merge')

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