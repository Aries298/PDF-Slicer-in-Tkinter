import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
from math import ceil, floor
from PyPDF2 import PdfFileReader, PdfFileWriter

output_folder_path = os.path.join(os.getcwd(), 'Output')
print(f'Output Path - {output_folder_path}')


def SelectFile():
    path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    filename.set(path)


def SliceInto():
    pdf = PdfFileReader(filename.get())
    counter = 0
    if int(e1.get()) > int(pdf.numPages):
        messagebox.showerror("Error", "Slice number greater than the number of pages.")
        return
    try:
        if int(e1.get()) > 0:
            file = filename.get().replace('.pdf', '')  # get just the filepath without the extension
            namefile = file.split("/")[-1]  # get just the name of the file
            folder = file + '_sliced'  # generate a folder name for temporary images
            combined = folder + '/' + namefile  # come up with temporary export path
            # create folder
            if not os.path.exists(folder):  # make the temporary folder
                os.makedirs(folder)
            slicenum = int(e1.get())
            for i in range(slicenum):
                pdfWriter = PdfFileWriter()
                while counter < (i + 1) * ceil(pdf.numPages / slicenum) and counter <= pdf.numPages - 1:
                    print(floor(int(pdf.numPages) / slicenum) * (i + 1))
                    pdfWriter.addPage(pdf.getPage(counter))
                    counter += 1
                with open('{0}_Part{1}.pdf'.format(combined, i + 1), 'wb') as f:
                    pdfWriter.write(f)
                    f.close()
                # This handles the situation when the input files number is too great
                # e.g.
                # 283 pages file gets divided into 20 parts
                # 283 / 20 = 15 * 18 + 13
                # 283 / 20 = 14 * 20 + 3
                # It would either need 19 pages or 21, in this case it chooses the former deleting the unecessary empty pdf
                temppdf = PdfFileReader('{0}_Part{1}.pdf'.format(combined, i + 1))
                if temppdf.numPages == 0:
                    os.remove('{0}_Part{1}.pdf'.format(combined, i + 1))
    except:
        messagebox.showerror("Error", "Unexpected error occured.")
        return
    messagebox.showinfo("Done", "File sliced successfully!")


def SliceEvery():
    pdf = PdfFileReader(filename.get())
    counter = 0
    try:
        if int(e2.get()) > 0:
            file = filename.get().replace('.pdf', '')  # get just the filepath without the extension
            namefile = file.split("/")[-1]  # get just the name of the file
            folder = file + '_sliced'  # generate a folder name for temporary images
            combined = folder + '/' + namefile  # come up with temporary export path
            # create folder
            if not os.path.exists(folder):  # make the temporary folder
                os.makedirs(folder)
            slicenum = int(e2.get())
            for i in range(ceil(pdf.numPages / slicenum)):
                pdfWriter = PdfFileWriter()
                while counter < slicenum * (i + 1) and counter <= pdf.numPages - 1:
                    pdfWriter.addPage(pdf.getPage(counter))
                    counter += 1
                with open('{0}_Part{1}.pdf'.format(combined, i), 'wb') as f:
                    pdfWriter.write(f)
                    f.close()

    except:
        messagebox.showerror("Error", "Unexpected error occured.")
        return
    messagebox.showinfo("Done", "File sliced successfully!")


root = tk.Tk()

root.geometry("600x80")
root.title("PDF Slicer")

filename = tk.StringVar()
filename.set("None")

b1 = tk.Button(root, text="Select file", command=SelectFile)
l1 = tk.Label(root, text="Selected pdf file:")
l2 = tk.Label(root, textvariable=filename, width=50)

l3 = tk.Label(root, text="Slice pdf file into")
l4 = tk.Label(root, text="Slice pdf file every")

l5 = tk.Label(root, text="files")
l6 = tk.Label(root, text="th page")

e1 = tk.Entry(root)
e2 = tk.Entry(root)

b2 = tk.Button(root, text="Slice", width=20, command=SliceInto)
b3 = tk.Button(root, text="Slice", width=20, command=SliceEvery)

b1.grid(row=0, column=0)
l1.grid(row=0, column=1)
l2.grid(row=0, column=2, columnspan=2)

l3.grid(row=1, column=0)
e1.grid(row=1, column=1)
l5.grid(row=1, column=2)
b2.grid(row=1, column=3, sticky='E')

l4.grid(row=2, column=0)
e2.grid(row=2, column=1)
l6.grid(row=2, column=2)
b3.grid(row=2, column=3, sticky='E')

root.mainloop()
