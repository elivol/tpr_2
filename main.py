import tkinter as tk
from funcs import *

root = tk.Tk()

#class MainWindow():
def first(event):
    print(savidj(np.array([[10, -2, 8], [-3, 5.2, 6], [7.5, 9, -1]], dtype=float)))

btn = tk.Button(root, text='Привет', width=30, height=5, bg='#ef3ef5', fg='black')
btn.bind('<Button-1>', first)
btn.pack()

root.mainloop()