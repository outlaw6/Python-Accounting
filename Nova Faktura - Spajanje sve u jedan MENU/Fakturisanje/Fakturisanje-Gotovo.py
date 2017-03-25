import HTML
from Tkinter import *
from listview import MultiListbox
from datetime import datetime
import MySQLdb

#
#GLOBALNE VARIJABLE
#
redni_broj = 1
cijene_sa_pdv = []
cijene_bez_pdv = []
suma_samo_pdv = []
ZBIR_FAKTURE = [ cijene_sa_pdv, cijene_bez_pdv, suma_samo_pdv]
LISTA_ZA_UNOS_U_BAZU = []
LISTA_ZA_PRINTING = []
Flag = None
datum = datetime.now()


def ocitavanje_rednog_broja_fakture():
    """Otvara MySQL bazu, cita redni broj i vrace ga u promjenljivu redni broj fakture"""

    global redni_broj_fakture, datum_variable

    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI")
    cursor = db.cursor()

    sql = """SELECT redni_broj from invoice"""
    cursor.execute(sql)

    redni_broj_fakture = cursor.fetchone()
    
    #db.commit()
    print redni_broj_fakture[0]
    fak = Label(root, text="Redni broj fakture : " + str(datum.year)+"-"+str(redni_broj_fakture[0]), fg="red").place(x = 550, y = 155)
    return fak 

    db.close()

def unos_u_bazu():
    """Otvara konekciju sa bazom, unosi LISTA ZA UNOS U BAZU, povecavam ZALIHE"""

    global LISTA_ZA_UNOS_U_BAZU
    print LISTA_ZA_UNOS_U_BAZU

    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI" )
    cursor = db.cursor()

    for artikal in LISTA_ZA_UNOS_U_BAZU:
        sql = """UPDATE zaliha SET kolicina = kolicina - '{0}' WHERE barcode = '{1}'""".format(artikal[1], artikal[0])
        cursor.execute(sql)
        db.commit()
    db.close()
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



def write_funkcija(redni_broj,sifra_artikla,naziv_artikla,j_mjere,komada,cijena,cijena_bez_pdv, pdv,rabat, cijena_sa_pdv, ukupno):

    """Ova funkcija upisuje elemente listboxa za printanje"""

    global LISTA_ZA_PRINTING

    lokalna_lista = []
    lokalna_lista.append(redni_broj)
    lokalna_lista.append(sifra_artikla)
    lokalna_lista.append(naziv_artikla)
    lokalna_lista.append(j_mjere)
    lokalna_lista.append(komada)
    lokalna_lista.append(cijena)
    lokalna_lista.append(cijena_bez_pdv)
    lokalna_lista.append(pdv)
    lokalna_lista.append(rabat)
    lokalna_lista.append(cijena_sa_pdv)
    lokalna_lista.append(ukupno)

    LISTA_ZA_PRINTING.append(lokalna_lista)

    print LISTA_ZA_PRINTING


def unos(*args):

    """Unosi u Listboxe dodate artikle. Glavna Funkcija. Setuje vrijednosti LABEL-a. Kontrolise da li je unos s Rabatom ili bez"""

    global redni_broj, suma, bez_pdv, pdv_iznos, cijene_sa_pdv, cijene_bez_pdv, suma_samo_pdv, LISTA_ZA_PRINTING, Flag

    JM = "KOM"
    sifra2 = int(sifra.get())
    naziv2 = naziv.get()
    cijena2 = float(cijena.get())
    komada2 = int(komada.get())
    rabat2 = int(rabat.get())
    pdv = 1.19
   
    print rabat2
    

    #
    # Dio funkcije ako faktua ima rabat
    #

    if rabat2 != 0:


        faktor_popusta = float((100 - rabat2) / 100.0)
        
        print faktor_popusta

        cijena_s_popustom = cijena2 * faktor_popusta

        cijena_bez_pdv = round(cijena2 * 0.84033, 2)

        samo_pdv = (cijena2 - cijena_bez_pdv) * komada2

        cijena_s_rabatom = round((cijena_bez_pdv * faktor_popusta) * pdv,2)

        ukupno = round(komada2 * cijena_s_rabatom,2)
        

        print cijena2

        rabat_entry.delete(0, END)
        rabat_entry.insert(0,0)


        mlb.insert(END, ('%d' % redni_broj, '%d' % sifra2, '%s' % naziv2, '%s' % JM,  '%d' % komada2,  str(cijena2), str(cijena_bez_pdv),  str(samo_pdv),  '%d' % rabat2, str(cijena_s_rabatom),  str(ukupno)))
        write_funkcija(redni_broj, sifra2, naziv2, JM,  komada2, cijena2, cijena_bez_pdv, samo_pdv, rabat2, cijena_s_rabatom,  ukupno)

        
        cijene_sa_pdv.append(ukupno)
        suma_samo_pdv.append(samo_pdv)
        cijene_bez_pdv.append(cijena_bez_pdv * komada2)


        suma.set(round(sum(cijene_sa_pdv),2))
        bez_pdv.set(round(sum(cijene_bez_pdv), 2))
        #pdv_iznos.set(round(sum(suma_samo_pdv),2) )
        pdv_iznos.set( round((round(sum(cijene_sa_pdv),2) - (round(sum(cijene_sa_pdv),2) - ((round(sum(suma_samo_pdv),2) * 0.84033)))),2))

        #
        #
        # Kreira LABEL za iskazivanje popusta
        #
        popust_label = Label(root, text="Popust: ", fg="red")
        popust_label.place(x = 700, y = 430)
        
        popust_iznos = StringVar()
        popust_iznos.set(round( sum(cijene_bez_pdv) - (sum(cijene_sa_pdv) * 0.84033), 2))
        popust_label2 = Label(root, textvariable=popust_iznos, fg="red")
        popust_label2.place(x = 770, y = 430)
        
        Flag = True
        print Flag


    #
    # Dio Funkcije ako je bez RABATA faktura
    #
    else:

        samo_pdv = round( cijena2 - (cijena2 * 0.84033), 2)
        suma_samo_pdv.append(round(((cijena2 * komada2) * 0.15967), 2))

        cijene_sa_pdv.append(cijena2 * komada2)

        ukupno = komada2 * cijena2

        

        cijena_bez_pdv = round(cijena2 * 0.84033, 2)

        cijene_bez_pdv.append( cijena_bez_pdv  * komada2 )

               


        mlb.insert(END, ('%d' % redni_broj, '%d' % sifra2, '%s' % naziv2, '%s' % JM,  '%d' % komada2,  str(cijena2), str(cijena_bez_pdv),  str(samo_pdv),  '%d' % rabat2, str(cijena2),  str(ukupno)))
        

        write_funkcija(redni_broj, sifra2, naziv2, JM,  komada2, cijena2, cijena_bez_pdv, samo_pdv, rabat2, cijena2,  ukupno)
        suma.set(round(sum(cijene_sa_pdv),2))

        bez_pdv.set( round(  sum(cijene_bez_pdv), 2))
        pdv_iznos.set( round(   sum(cijene_sa_pdv) * 0.15967 ,2)   )

    




    lokalna_lista = []
    lokalna_lista.append(sifra2)
    lokalna_lista.append(komada2)
    

    LISTA_ZA_UNOS_U_BAZU.append(lokalna_lista)
    
    print LISTA_ZA_UNOS_U_BAZU
    #
    # Izbirisi ENTRY pozicije
    #
    sifra_entry.delete(0, END)
    naziv_entry.delete(0,END)
    cijena_entry.delete(0, END)
    komada_entry.delete(0, END)
    sifra_entry.focus()
    redni_broj += 1

    root.update_idletasks()


#
# root window
#
root  = Tk()
root.title("Fakturisanje")
root.geometry("1200x500")
frame = Frame(root)
#
# Varijable
#
sifra = StringVar()
naziv = StringVar()
cijena = StringVar()
komada = StringVar()
rabat = StringVar()
kupac = StringVar()
kupac_pib = StringVar()
kupac_pdv = StringVar()
kupac_adresa = StringVar()
pdv = 1.19

#
# LABELS
#
Label(root, text="Datum : " + str(datum.day) + "-" + str(datum.month) + "-" + str(datum.year)).place(x = 100, y = 25)

Label(root, text="Sifra artikla").place(x = 100, y = 50)
sifra_entry = Entry(root, width = 12, textvariable=sifra)
sifra_entry.place(x = 200 , y = 50)

Label(root, text="Naziv artikla").place(x = 100, y = 75)
naziv_entry = Entry(root, width = 20, textvariable=naziv)
naziv_entry.place(x = 200, y = 75)

Label(root, text="Cijena artikla").place(x = 100, y = 100)
cijena_entry = Entry(root, width = 7, textvariable=cijena)
cijena_entry.place(x = 200, y = 100)

Label(root, text="Rabat").place(x = 300, y = 101)
Label(root, text="%").place(x = 395, y = 101)
rabat_entry = Entry(root, width = 5, textvariable=rabat )
rabat_entry.insert(0, 0)
rabat_entry.place(x = 350, y = 100)


Label(root, text="Komada").place(x = 100, y = 125)
komada_entry = Entry(root, width = 7, textvariable=komada)
komada_entry.place(x = 200, y = 125)

Label(root, text="Kupac :").place(x = 550, y=50)
kupac_entry = Entry(root, width = 18, textvariable=kupac)
kupac_entry.place(x = 610, y = 50)

Label(root, text = "Kupac PIB :").place(x = 550, y = 75)
kupac_pib_entry = Entry(root, width = 9, textvariable=kupac_pib)
kupac_pib_entry.place(x = 625, y = 75)

Label(root, text = "Kupac PDV :").place(x = 550, y = 100)
kupac_pdv_entry = Entry(root, width = 9, textvariable = kupac_pdv)
kupac_pdv_entry.place(x = 635, y = 100)

Label(root, text = "Adresa :").place(x = 550, y = 125)
kupac_adresa_entry = Entry(root, width = 18, textvariable = kupac_adresa)
kupac_adresa_entry.place( x = 635, y = 125)


#
# BUTTON
#

Button(root, text="UNESI", command=unos, background="grey").place(x = 100, y = 150)



ukupno_bez_pdv = Label(root, text = "Bez PDV: ", fg= "red")
ukupno_bez_pdv.place(x= 600, y = 400)
bez_pdv = StringVar()
bez_pdv2 = Label(root, textvariable=bez_pdv, fg="red")
bez_pdv2.place(x = 660, y = 400)


ukupno_pdv = Label(root, text="PDV : ", fg="red")
ukupno_pdv.place(x = 600, y = 430)
pdv_iznos = StringVar()
pdv_iznos2 = Label(root, textvariable=pdv_iznos, fg="red")
pdv_iznos2.place(x = 630, y = 430)


Ukupno_iznos = Label(root, text="Ukupno : ", fg = "red")
Ukupno_iznos.place(x = 600, y = 460)
suma = StringVar()
suma2 = Label(root, textvariable=suma, fg="red")
suma2.place(x = 660, y = 460)


#
# Napravi MultiListBox
#

mlb = MultiListbox(root, (('R. Broj', 4), ('Sifra artikla', 8), ('Naziv artikla', 36), ('JM', 4), ('Komada', 1), ('Cijena', 5), ('C. bez PDV', 1) ,('PDV', 4), ('Rabat', 4) ,('Cijena s Rabatom', 1), ('Ukupno', 9)))
mlb.place(x= 100, y=  200)


#
# Pozovi DELETE, izbrisi selektovani element
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
# Write Funkcija za stvaranje HTML fakture
#

def ispisi():

    """ Ova funkcija ispisuje u file, kreira HTML Fakturu. Ne preuzima nikakve argumente """

   

    f2 = open("/home/pandemonium/Documents/Latica-Faktura" + str(datum.year) +"-"+ str(datum.month) +"-"+ str(datum.day) + ".html", "w")

    f2.write("<body>")
    f2.write("<style> p.date {text-align:right;} \n")
    f2.write(".right { position:absolute;  right:0px; width:245px;}  .left { position: relative; left: 0px; width: 300px; border: 1px solid black; margin-bottom: 50px;} \
            .top-right { position: fixed; top: 20px; right: 30px; width: 300px; height: 200px; } .top { position: relative; top: 50px; left: auto; right: auto; margin-bottom: 60px;} img { float: left; }</style>")
    f2.write('<div class="left"> <img src="/home/pandemonium/Documents/rsz_1latica.jpg"> <p> Latica DOO </p> <p> PIB: 1257-45/2  </p> <p>   PDV: 2247-44-826</p> <p> Tel: 00/ 223 444</div> </center>')
    f2.write('<div class="top-right"><p> Kupac : ' + str(kupac.get()) + ' </p> <p> Kupac PIB : ' + str(kupac_pib.get()) + '</p><p>'+ 'Kupac PDV : ' + str(kupac_pdv.get()) + '</p><p>Adresa : ' + str(kupac_adresa.get()) +  '</p></div>')
    f2.write('<center><strong><p> Faktura br: ' + str(datum.year)+ "-" +str(redni_broj_fakture[0]) + '  </center> </strong> </p>')
    




    htmlcode = HTML.table(LISTA_ZA_PRINTING, header_row = ['R. Broj',   'Sifra',   'Naziv artikla','JM',  'Komada', 'Cijena','Cijena bez PDV', 'PDV','Rabat %', 'Cijena s rabatom',  'Ukupno'],
                                             col_width=['5%', '7%', '20%', '7%', '7%',  '7%', '7%', '7%', '7%', '7%', '7%'] ,
                                             col_align=['center', 'center', 'center', 'center','center',  'center' ,'center',' center', 'center', 'center', 'center'], 
                                             col_styles=['font-size: 12px', 'font-size:12px','font-size: 12px','font-size: 12px', 'font-size: 12px','font-size: 12px', \
                                             'font-size: 12px','font-size: 12px', 'font-size: 12px', 'font-size: 12px', 'font-size: 14px'])

    
    f2.write('<center><div class="top"> ' + htmlcode + '<p>\n'+ '</center></div>\n')


    #
    #Pravi posebnu LISTU, zbir zbirova na kraju fakture 
    #
    #
    # Provjerava FLAG za popust, nema druge

    if Flag == True:
        suma_bez_pdv = []
        x = "Bez PDV: "
        suma_bez_pdv.append(x)
        suma_bez_pdv.append(round( sum(cijene_bez_pdv), 2  ))

        suma_popust = []
        p = "Popust: "
        suma_popust.append(p)
        suma_popust.append(round( sum(cijene_bez_pdv) - (sum(cijene_sa_pdv) * 0.84033), 2))

        suma_pdv = []
        y = "PDV :"
        suma_pdv.append(y)
        suma_pdv.append(str(sum(suma_samo_pdv)))

        zbir_sa_pdv = []
        z = "UKUPNO: "
        zbir_sa_pdv.append(z)
        zbir_sa_pdv.append(str(sum(cijene_sa_pdv)))

        ZBIR2 = []

        ZBIR2.append(suma_bez_pdv)
        ZBIR2.append(suma_pdv)
        ZBIR2.append(zbir_sa_pdv)
        ZBIR2.append(suma_popust)
        print ZBIR2

    else:
        suma_bez_pdv = []
        x = "Bez PDV: "
        suma_bez_pdv.append(x)
        suma_bez_pdv.append(round( sum(cijene_bez_pdv), 2  ))

        suma_pdv = []
        y = "PDV :"
        suma_pdv.append(y)
        suma_pdv.append(str(sum(suma_samo_pdv)))

        zbir_sa_pdv = []
        z = "UKUPNO: "
        zbir_sa_pdv.append(z)
        zbir_sa_pdv.append(str(sum(cijene_sa_pdv)))

        ZBIR2 = []

        ZBIR2.append(suma_bez_pdv)
        ZBIR2.append(suma_pdv)
        ZBIR2.append(zbir_sa_pdv)
        print ZBIR2
    
    zbir2 = HTML.table(ZBIR2, col_width=['40%', '40%'], col_align = ['', 'center'] , col_styles = ['', 'background-color:grey'])
    f2.write('<center>'  + '<div class="right">' + zbir2 + '</div>' + '</center>')

    f2.write("</body>")
    ###############################################
    

    
    pass



Button(root, text="ISPISI", command=ispisi, background="grey").place(x = 250, y = 150)
Button(root, text="Proknjizi", command=unos_u_bazu, background="grey").place(x = 325, y = 150)



def idi_dolje(x):

    if (root.focus_displayof() == sifra_entry):
        naziv_entry.focus()
    elif (root.focus_displayof() == naziv_entry):
        cijena_entry.focus()
    elif (root.focus_displayof() == cijena_entry):
        komada_entry.focus()    
    elif (root.focus_displayof() == komada_entry):
        sifra_entry.focus()
        

def idi_gore(y):

    if (root.focus_displayof() == sifra_entry):
        komada_entry.focus()
    elif (root.focus_displayof() == komada_entry):
        cijena_entry.focus()
    elif (root.focus_displayof() == cijena_entry):
        naziv_entry.focus()
    elif (root.focus_displayof() == naziv_entry):
        sifra_entry.focus()    



sifra_entry.focus()
root.bind('<KP_Enter>', test_funkcija)
root.bind('<Delete>', test_funkcija)
root.bind('<Return>', unos)
root.bind('<Down>', idi_dolje)
root.bind('<Up>', idi_gore)
root.update_idletasks()
ocitavanje_rednog_broja_fakture()

root.mainloop()