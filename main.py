from ttkthemes import ThemedTk
from tkinter import ttk
import tkinter as tk

def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def main():
    root = ThemedTk(theme="breeze")
    root.config(bg=rgb(200,200,200))
    button = ttk.Button(root, text="modern button")
    entry = ttk.Entry(root)
    entry.pack()
    button.pack()
    root.mainloop()

with open("quiz.txt", "r") as f:
    file = f.readlines()
    
    container = []

    for line in file:
        container.append(line.replace("\n", ""))
    
    print(container)

if __name__ == "__main__":
    main()
        

    

    

