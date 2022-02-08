import os
from PIL import Image
from tkinter import messagebox
from PyPDF2 import PdfFileMerger, PdfFileReader
from tkinter import messagebox

def merge(filePaths,save_filename):
    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()

    for file in filePaths:
        mergedObject.append(PdfFileReader(file, 'rb'))

    # Write all the files into a file which is named as shown below
    mergedObject.write(save_filename)

    messagebox.showinfo(title='Message', message=f'Done! The merged pdf file is saved as {save_filename}')

def jpgToPdf(filePaths, save_filename):
    filePaths = [f.split('/')[-1].split('.')[0] + "_tmp." + f.split('/')[-1].split('.')[1] for f in filePaths]

    im1, imagelist = [], []
    for f in filePaths:
        f = f.lower()
        if not (f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')):
            continue
        dir = './tmp/' + f
        img = Image.open(dir)
        img = img.convert('RGB')
        if im1:
            imagelist.append(img)
            continue
        im1.append(img)

    im1[0].save(save_filename, save_all=True, append_images=imagelist)
    messagebox.showinfo(title='Message', message=f'Done! The converted pdf file is saved as {save_filename}')

    for f in filePaths:
        dir = './tmp/' + f
        os.remove(dir)