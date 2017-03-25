

def idi_dolje(x):
    if (x.focus_displayof() == sifra_entry):
        naziv_entry.focus()
    elif (x.focus_displayof() == naziv_entry):
        cijena_entry.focus()
    elif (x.focus_displayof() == cijena_entry):
        komada_entry.focus()    
    elif (x.focus_displayof() == entry4):
        naziv_entry.focus()
        

def idi_gore(y):

    if (y.focus_displayof() == sifra_entry):
        naziv_entry.focus()
    elif (y.focus_displayof() == naziv_entry):
        komada_entry.focus()
    elif (y.focus_displayof() == komada_entry):
        naziv_entry.focus()
    elif (y.focus_displayof() == naziv_entry):
        sifra_entry.focus()    




if __name__ == '__main__':

    entry1 = Entry(root)
    entry2 = Entry(root)
    entry3 = Entry(root)
    entry4 = Entry(root)
    button = Button(text='go', command=test)
    entry1.pack()
    entry2.pack()
    entry3.pack()
    entry4.pack()
    button.pack()
    root.bind('<Down>', idi_dolje)
    root.bind('<Up>', idi_gore)
    entry1.focus()
    root.mainloop()