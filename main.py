from ttkthemes import ThemedTk
from tkinter import ttk

def rgb(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def main():
    root = ThemedTk(theme="Adapta")
    root.config(bg=rgb(200,200,200))
    button = ttk.Button(root, text="modern button")
    entry = ttk.Entry(root)
    entry.pack()
    button.pack()
    root.mainloop()

if __name__ == "__main__":
    main()