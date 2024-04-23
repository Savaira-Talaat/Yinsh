from tkinter import *
from PIL import Image, ImageTk

def on_enter(e, btn):
    btn['background'] = 'lightgrey'

def on_leave(e, btn):
    btn['background'] = 'slate grey'

fenetre = Tk()
fenetre.geometry("900x600")
fenetre.title("Menu du jeu")
fenetre['bg'] = 'black'
fenetre.resizable(height=False, width=False)

image = Image.open("yinsh.jpg")
photo = ImageTk.PhotoImage(image)
canvas = Canvas(fenetre, width=900, height=600)
canvas.pack()

canvas.create_image(0, 0, anchor=NW, image=photo)
label_menu = Label(canvas, text='Welcome to the YINSH game', font=("Bungee Spice", 20, "bold"), bg='black', fg='white')
label_menu.place(relx=0.5, rely=0.1, anchor=CENTER)

button_normal = Button(canvas, text="Mode Normal", font=("Bungee Spice", 20, "bold"), bg='slate grey', bd=4, relief=RAISED)
button_normal.place(relx=0.3, rely=0.5, anchor=CENTER)
button_normal.bind("<Enter>", lambda e, btn=button_normal: on_enter(e, btn))
button_normal.bind("<Leave>", lambda e, btn=button_normal: on_leave(e, btn))

button_blitz = Button(canvas, text="Mode Blitz", font=("Bungee Spice", 20, "bold"), bg='slate grey', bd=4, relief=RAISED)
button_blitz.place(relx=0.7, rely=0.5, anchor=CENTER)
button_blitz.bind("<Enter>", lambda e, btn=button_blitz: on_enter(e, btn))
button_blitz.bind("<Leave>", lambda e, btn=button_blitz: on_leave(e, btn))






fenetre.mainloop()
