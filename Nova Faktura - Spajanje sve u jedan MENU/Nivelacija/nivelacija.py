import HTML
from Tkinter import *
from listview import MultiListbox
import MySQLdb
import HTML
from datetime import datetime

#GLOBALNE VARIJABLE

redni_broj = 1
cijene_sa_pdv = []
cijene_bez_pdv = []
suma_samo_pdv = []

ZBIR_FAKTURE = [ cijene_sa_pdv, cijene_bez_pdv, suma_samo_pdv]

LISTA_ZA_PRINTING = []

datum = datetime.now()
datum_variable = str(datum.day)+"-"+str(datum.month)+"-"+str(datum.year)

def write_funkcija(a,b,c,d,e,f,g):

    """Ova funkcija upisuje elemente listboxa za printanje"""

    global LISTA_ZA_PRINTING

    lokalna_lista = []
    lokalna_lista.append(a)
    lokalna_lista.append(b)
    lokalna_lista.append(c)
    lokalna_lista.append(d)
    lokalna_lista.append(e)
    lokalna_lista.append(f)
    lokalna_lista.append(g)

    LISTA_ZA_PRINTING.append(lokalna_lista)

    print LISTA_ZA_PRINTING

def ocitavanje_vrijednosti_iz_baze(x):
    """Otvara MySQL bazu, cita redni broj i vrace ga u promjenljivu redni broj fakture"""

    global stanje_iz_baze, datum_variable

    sifra2 = int(sifra.get())

    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI")
    cursor = db.cursor()

    sql = """SELECT naziv, kolicina, pvrijednost from zaliha where barcode = {0}""".format(sifra2)
    cursor.execute(sql)

    stanje_iz_baze = cursor.fetchone()
    
    
    print stanje_iz_baze
    naziv_entry.insert(END, stanje_iz_baze[0])
    cijena_entry.insert(END, stanje_iz_baze[2])
    komada_entry.insert(0, stanje_iz_baze[1])
    
    root.unbind('<KP_Enter>')
    root.bind('<KP_Enter>', unos)

    
    db.close()

def unos_u_bazu():
    """Ova funkcija zamijenjuje staru cijenu novom cijenom"""

    
    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI" )
    cursor = db.cursor()

    sql = """UPDATE zaliha SET pvrijednost = '{0}' WHERE barcode = '{1}'""".format(nova_cijena2, sifra.get())
    cursor.execute(sql)
    db.commit()
    db.close()

    sifra_entry.delete(0, END)
    naziv_entry.delete(0,END)
    cijena_entry.delete(0, END)
    komada_entry.delete(0, END)
    nova_cijena_entry.delete(0, END)
    pass


def test_funkcija(x):

    sifra2 = int(sifra.get())

    """Funkcija koja uspostavlja konekciju s bazom i ispisuje vrijednosti u entry polja"""

    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI" )
    cursor = db.cursor()
    sql = """SELECT pvrijednost, naziv from zaliha where barcode = {0}""".format(sifra2) 
    cursor.execute(sql)

    data = list(cursor.fetchone())

    
    print  data[0] 

    cijena_entry.insert(END, float(data[0]))
    naziv_entry.insert(END, data[1])
    komada_entry.focus()
    db.close()


def unos(*args):

    """Unosi u Listboxe dodate artikle"""

    global redni_broj, LISTA_ZA_PRINTING, nova_cijena2, staro_stanje, novo_stanje, razlika

    sifra2 = int(sifra.get())
    naziv2 = naziv.get()
    cijena2 = float(cijena.get())
    komada2 = int(komada.get())

    nova_cijena2 = float(nova_cijena.get())

            
    sifra_entry.focus()
    redni_broj += 1

    staro_stanje = round(komada2 * cijena2,2)
    novo_stanje = round(komada2 * nova_cijena2,2)
    razlika = round(staro_stanje - novo_stanje, 2)

    staro_stanje_ukupno.set(staro_stanje)
    novo_stanje_ukupno.set(novo_stanje)
    razlika_iznos.set(razlika)
    


    mlb.insert(END, ('%d' % redni_broj, '%d' % sifra2, '%s' % naziv2, '%d' % komada2, str(cijena2), str(nova_cijena2), str(cijena2 - nova_cijena2)))
    write_funkcija(redni_broj, sifra2, naziv2, komada2, cijena2, nova_cijena2, cijena2 - nova_cijena2)

    root.update_idletasks()

#
# root window
#
root  = Tk()
root.title("Nivelacija")
root.geometry("900x500")
#
# Varijable
#
sifra = StringVar()
naziv = StringVar()
cijena = StringVar()
komada = StringVar()
nova_cijena = StringVar()


#
# LABELS
#
Label(root, text="Sifra artikla").place(x = 100, y = 50)
sifra_entry = Entry(root, width = 7, textvariable=sifra)
sifra_entry.place(x = 200 , y = 50)

Label(root, text="Naziv artikla").place(x = 100, y = 75)
naziv_entry = Entry(root, width = 20, textvariable=naziv)
naziv_entry.place(x = 200, y = 75)

Label(root, text="Cijena artikla").place(x = 100, y = 100)
cijena_entry = Entry(root, width = 7, textvariable=cijena)
cijena_entry.place(x = 200, y = 100)

Label(root, text="Komada").place(x = 100, y = 125)
komada_entry = Entry(root, width = 7, textvariable=komada)
komada_entry.place(x = 200, y = 125)

Label(root, text="Nova CIJENA").place(x = 270, y = 125)
nova_cijena_entry = Entry(root, width = 7, textvariable = nova_cijena)
nova_cijena_entry.place(x = 350, y = 125)

Label(root, text="Datum: ").place(x = 100, y = 25)
Label(root, text=str(datum.day)+"-"+str(datum.month)+"-"+str(datum.year)).place(x = 150, y = 25)


#
# BUTTON
#

Button(root, text="UNESI", command=unos, background="grey").place(x = 100, y = 150)
Button(root, text="PROKNJIZI", command=unos_u_bazu, background="grey").place(x = 320, y = 150)



staro_stanje = Label(root, text = "Ukupno staro stanje : ", fg= "red")
staro_stanje.place(x= 600, y = 400)
staro_stanje_ukupno = StringVar()
staro_stanje2 = Label(root, textvariable=staro_stanje_ukupno, fg="red")
staro_stanje2.place(x = 760, y = 400)


razlika = Label(root, text="Razlika : ", fg="red")
razlika.place(x = 600, y = 460)
razlika_iznos = StringVar()
razlika_iznos2 = Label(root, textvariable=razlika_iznos, fg="red")
razlika_iznos2.place(x = 730, y = 460)


novo_stanje = Label(root, text="Ukupno novo stanje : ", fg = "red")
novo_stanje.place(x = 600, y = 430)
novo_stanje_ukupno = StringVar()
suma2 = Label(root, textvariable=novo_stanje_ukupno, fg="red")
suma2.place(x = 760, y = 430)


mlb = MultiListbox(root, (('R. Broj', 4), ('Sifra artikla', 8), ('Naziv artikla', 36), ('Kolicina', 8), ('Stara Cijena', 8), ('Nova cijena', 8), ('Razlika', 12)))
mlb.place(x= 100, y=  200)


#
# Pozovi DELETE
#

def pozovi_delete():

    global redni_broj, LISTA_ZA_PRINTING
    index = mlb.item_selected[0]
    print index
    mlb.btn_del_click()
    print ZBIR_FAKTURE

    
    for y in ZBIR_FAKTURE:
        del y[index]
        suma.set(sum(cijene_sa_pdv))
        bez_pdv.set(sum(cijene_bez_pdv))
        pdv_iznos.set(round(sum(suma_samo_pdv),2))

    del LISTA_ZA_PRINTING[index]
    print LISTA_ZA_PRINTING
    redni_broj -= 1


Button(root, text="DELETE", command=pozovi_delete, background="grey").place(x = 170, y = 150)


#
# Write Funkcija
#

def ispisi():
    """ Ova funkcija ispisuje u file """

    f2 = open("/home/pandemonium/Documents/Latica-Fakutra.html", "w")

    f2.write("<body>")
    f2.write("<style> p.date {text-align:right;} \n")
    f2.write(".right { position:absolute;  right:0px; width:245px;}  .left { position: relative; left: 0px; width: 300px; border: 1px solid black; margin-bottom: 50px;}  .top { position: relative; top: 50px; left: auto; right: auto; margin-bottom: 60px;} img { float: left; }</style>")
    f2.write('<div class="left"> <img src="/home/pandemonium/Documents/rsz_1latica.jpg"> <p> Latica DOO </p> <p> PIB: 1257-45/2  </p> <p>   PDV: 2247-44-826</p> <p> Tel: 00/ 223 444</div> </center>')
    f2.write('<center><strong style="font-size: bog"> Promjena cijene  '+ str(datum_variable) + '</center></storng>')
    

    zadnj_red = [ '', '<strong>', 'UKUPNO', '',
                                            '<strong>' + str(staro_stanje),
                                            '<strong>' + str(novo_stanje),
                                            '<strong>' + str(razlika * (-1))]

    LISTA_ZA_PRINTING.append(zadnj_red)
                                    


    htmlcode = HTML.table(LISTA_ZA_PRINTING, header_row = ['R. Broj',   'Sifra',   'Naziv artikla', 'Komada', 'Stara cijena', 'Nova Cijena', 'Razlika'],
                                             col_width=['10%', '10%', '30%', '10%', '10%', '10%', '10%'] ,
                                             col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center'], 
                                             col_styles=['font-size: small', 'font-size: small','font-size: small','font-size: small','font-size: small','font-size: small', 'background-color:grey'])

    f2.write('<center><div class="top"> ' + htmlcode + '<p>\n'+ '</center></div>\n')


    f2.close()
        
    pass

#
# PRINT, Write to file
#


Button(root, text="ISPISI", command=ispisi, background="grey").place(x = 250, y = 150)

   

sifra_entry.focus()
root.bind('<Delete>', pozovi_delete)
root.bind('<Return>', unos)
root.bind('<KP_Enter>', ocitavanje_vrijednosti_iz_baze)
root.update_idletasks()


root.mainloop()