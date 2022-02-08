from PyPDF2 import PdfFileMerger, PdfFileReader
from tkinter import messagebox

def merge(filePaths,save_dir):
    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()

    for file in filePaths:
        mergedObject.append(PdfFileReader(file, 'rb'))

    # Write all the files into a file which is named as shown below
    mergedObject.write(f"{save_dir}/merged.pdf")

    messagebox.showinfo(title='Message', message=f'Done! The merged pdf file is stored in {save_dir}')