import HTML
from Tkinter import *
from listview import MultiListbox
import MySQLdb
from datetime import datetime


#GLOBALNE VARIJABLE

redni_broj = 1
dobavljaceva_vrijednost = []
pdv_ulazni_suma = []
prodajna_vrijednost_suma = []
razlika_u_cijeni_suma = []
prodajna_bez_pdv_suma = []
pdv_izlazni = []
ZBIR_FAKTURE = [ dobavljaceva_vrijednost, pdv_ulazni_suma, prodajna_vrijednost_suma, prodajna_bez_pdv_suma , razlika_u_cijeni_suma, pdv_izlazni ]
nabavna_vrijednost_suma = []
LISTA_ZA_PRINTING = []
LISTA_ZA_UNOS_U_BAZU = []

datum = datetime.now()
datum_variable = str(datum.day)+"-"+str(datum.month)+"-"+str(datum.year)


def zavisni_troskovi_nabavke(ztn, suma):

    """Racuna procentualno ucesce troskova nabavke u sumi fakture da bi se dodalo na dobavljacevu vrijednost"""

    return  round(1 + (ztn/suma),4)

    




def ocitavanje_rednog_broja_fakture():
    """Otvara MySQL bazu, cita redni broj i vrace ga u promjenljivu redni broj fakture"""

    global redni_broj_fakture, datum_variable

    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI")
    cursor = db.cursor()

    sql = """SELECT redni_broj from faktura"""
    cursor.execute(sql)

    redni_broj_fakture = cursor.fetchone()
    
    #db.commit()
    print redni_broj_fakture[0]
    fak = Label(root, text="Redni broj prijemnice : " + str(datum.year)+"-"+str(redni_broj_fakture[0]), fg="red").place(x = 500, y = 250)
    return fak 

    db.close()



def unos_u_bazu():
    """Otvara konekciju sa bazom, unosi LISTA ZA UNOS U BAZU, povecavam ZALIHE"""

    global LISTA_ZA_UNOS_U_BAZU
    print LISTA_ZA_UNOS_U_BAZU

    db = MySQLdb.connect("localhost","unos","123456","ARTIKLI" )
    cursor = db.cursor()

    for artikal in LISTA_ZA_UNOS_U_BAZU:
        sql = """INSERT INTO zaliha VALUES (id, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(artikal[0], artikal[1], artikal[2], artikal[3], artikal[4], artikal[5])
        cursor.execute(sql)
        db.commit()
    db.close()
    pass


def write_funkcija(lista):

    """Ova funkcija upisuje elemente listboxa za printanje i kreira
       LISTU ZA UNOS U BAZU """

    global LISTA_ZA_PRINTING

    lokalna_lista = []

    for x in lista:
        lokalna_lista.append(x)
    

    LISTA_ZA_PRINTING.append(lokalna_lista)
    print LISTA_ZA_PRINTING


def unos(*args):

    """Unosi u Listboxe dodate artikle"""

    global redni_broj, suma, dobavljaceva_vrijednost, pdv_ulazni_suma, prodajna_vrijednost_suma, prodajna_bez_pdv_suma, LISTA_ZA_PRINTING, pdv_izlazni,\
            nabavna_vrijednost_suma, LISTA_ZA_UNOS_U_BAZU
    pdv = 1.19
    JM = "KOM"
    sifra2 = int(sifra.get())
    naziv2 = naziv.get()
    cijena2 = float(cijena.get())
    komada2 = int(komada.get())
    transport2 = float(transport.get())
    carina2 = float(carina.get())
    ukupna_vrijednost_fakure2 = float(ukupna_vrijednost_fakure.get())



    maloprodajna_cijena2 = float(maloprodajna_cijena.get())

    prodajna_cijena_bez_pdv = round(maloprodajna_cijena2 * 0.84033,2)

    

    

    PDV = round(maloprodajna_cijena2 * 0.1597,2)

    ZTN = round(zavisni_troskovi_nabavke((transport2 + carina2), ukupna_vrijednost_fakure2),4) 

    nabavna_vrijednost = round(cijena2 * ZTN,2)

    zavisni_troskovi_transport = round((zavisni_troskovi_nabavke(transport2, ukupna_vrijednost_fakure2) - 1) * 100,2)
    zavisni_troskovi_carina = round((zavisni_troskovi_nabavke(carina2, ukupna_vrijednost_fakure2)  - 1) * 100, 2)
    pdv_ulazni = round( (((cijena2 * komada2) * pdv) * 0.15967),2)
    razlika_u_cijeni = round(prodajna_cijena_bez_pdv - nabavna_vrijednost,2)


    mlb.insert(END, ('%d' % redni_broj, '%d' % sifra2, '%s' % naziv2, '%d' % komada2, JM, str(cijena2), str(zavisni_troskovi_transport),\
                     str(zavisni_troskovi_carina),  str(nabavna_vrijednost), str(pdv_ulazni), str(razlika_u_cijeni), str(prodajna_cijena_bez_pdv), PDV, str(maloprodajna_cijena2)))
    
    mlb.insert(END, )
    #
    # Prosledjujuje HTML-u kreatoru da stvori file za printing
    #


    lista_za_ispis = [redni_broj, sifra2, naziv2, komada2, JM, cijena2, zavisni_troskovi_transport, zavisni_troskovi_carina, nabavna_vrijednost, \
                      pdv_ulazni, razlika_u_cijeni, prodajna_cijena_bez_pdv, PDV, maloprodajna_cijena2]
    write_funkcija(lista_za_ispis)

    
    #
    # Dodaje artikle za unos u bazu
    #
    lokalna_lista = []
    lokalna_lista.append(sifra2)
    lokalna_lista.append(naziv2)
    lokalna_lista.append(JM)
    lokalna_lista.append(komada2)
    lokalna_lista.append(cijena2)
    lokalna_lista.append(maloprodajna_cijena2)

    LISTA_ZA_UNOS_U_BAZU.append(lokalna_lista)
    print LISTA_ZA_UNOS_U_BAZU

    ###


    sifra_entry.delete(0, END)
    naziv_entry.delete(0,END)
    cijena_entry.delete(0, END)
    komada_entry.delete(0, END)
    maloprodajna_entry.delete(0, END)

    sifra_entry.focus()
    redni_broj += 1

    dobavljaceva_vrijednost.append(cijena2 * komada2)
    suma_dob_vrijednosti.set(round(sum(dobavljaceva_vrijednost), 2))

    nabavna_vrijednost_suma.append(nabavna_vrijednost * komada2)

    pdv_ulazni_suma.append(pdv_ulazni)
    pdv_iznos.set(round(sum(pdv_ulazni_suma),2))

    prodajna_vrijednost_suma.append(maloprodajna_cijena2 * komada2)
    suma.set(round(sum(prodajna_vrijednost_suma),2))

    razlika_u_cijeni_suma.append(razlika_u_cijeni * komada2)
    raz_u_cijeni.set(round(sum(razlika_u_cijeni_suma),2))

    prodajna_bez_pdv_suma.append(maloprodajna_cijena2 * 0.84033* komada2)
    suma_bez_pdv.set(round(sum(prodajna_bez_pdv_suma),2))

    pdv_izlazni.append(PDV * komada2)
    pdv_izlazni_suma.set(round(sum(pdv_izlazni),2))
    print prodajna_vrijednost_suma

    
    
    root.update_idletasks()
    pass




#
# root window
#
root  = Tk()
root.title("UNOS ARTIKALA")
root.geometry("1400x800")

#Button(root, text="test", command=transport, background="grey").place(x = 250, y = 10)
#
# Varijable
#
sifra = StringVar()
naziv = StringVar()
cijena = StringVar()
komada = StringVar()
maloprodajna_cijena = StringVar()
pdv = 1.19
dobavljac = StringVar()
dobavljac_pdv = StringVar()
dobavljac_pib = StringVar()
dobavljac_adresa = StringVar()
dobavljac_telefon = StringVar()
transport = StringVar()
carina = StringVar()
ukupna_vrijednost_fakure = StringVar()
broj_racuna = StringVar()


#
# LABELS
#


Label(root, text="Datum: ").place(x = 100, y = 25)
Label(root, text=str(datum.day)+"-"+str(datum.month)+"-"+str(datum.year)).place(x = 150, y = 25)

Label(root, text="Unos artikala & Kalkulacija maloprodajne cijene", fg="red", font = "Helvetica 16 ").place( x = 400, y = 5 )


Label(root, text="Dobavljac :").place(x = 500, y = 50)
dobavljac_entry = Entry(root, width = 15, textvariable=dobavljac)
dobavljac_entry.place(x = 600, y = 50)

Label(root, text="PDV :").place(x = 500, y = 75)
dobavljac_pdv_entry = Entry(root, width = 15, textvariable=dobavljac_pdv)
dobavljac_pdv_entry.place(x = 600, y = 75)

Label(root, text="PIB :").place(x = 500, y = 100)
dobavljac_pib_entry = Entry(root, width = 15, textvariable=dobavljac_pib)
dobavljac_pib_entry.place(x = 600, y = 100)

Label(root, text="Dobavljac adresa :").place(x = 500, y = 125)
dobavljac_adresa_entry = Entry(root, width = 22, textvariable=dobavljac_adresa)
dobavljac_adresa_entry.place(x = 630, y = 125)

Label(root, text="Telefon :").place(x = 500, y = 150)
dobavljac_telefon_entry = Entry(root, width = 15, textvariable=dobavljac_telefon)
dobavljac_telefon_entry.place(x = 600, y = 150)

Label(root, text="Br. Fakture :").place(x = 500, y = 175)
broj_racuna_entry = Entry(root, width = 7, textvariable=broj_racuna)
broj_racuna_entry.place( x = 600, y = 175)

Label(root, text="Barcode artikla").place(x = 100, y = 50)
sifra_entry = Entry(root, width = 15, textvariable=sifra)
sifra_entry.place(x = 200 , y = 50)

Label(root, text="Naziv artikla").place(x = 100, y = 75)
naziv_entry = Entry(root, width = 25, textvariable=naziv)
naziv_entry.place(x = 200, y = 75)

Label(root, text="Komada").place(x = 100, y = 100)
komada_entry = Entry(root, width = 7, textvariable=komada)
komada_entry.place(x = 200, y = 100)

Label(root, text="Nabavna Cijena artikla").place(x = 100, y = 125)
cijena_entry = Entry(root, width = 7, textvariable=cijena)
cijena_entry.place(x = 200, y = 125)

Label(root, text="Maloprodajna cijena").place(x = 100, y = 155)
maloprodajna_entry = Entry(root, width = 7, textvariable = maloprodajna_cijena)
maloprodajna_entry.place(x= 230, y = 155)

Label(root, text="Transport").place( x = 100, y = 180)
transport_entry = Entry(root, width = 7, textvariable = transport)
transport_entry.place(x = 195, y =180)

Label(root, text="Carina").place(x = 100, y = 210)
carina_entry = Entry(root, width = 7, textvariable=carina)
carina_entry.place( x = 195, y = 210)

Label(root, text="Ukupna vrijednost fakture :").place(x = 300, y = 210)
ukupna_vrijednost_fakure_entry = Entry(root, width = 10, textvariable=ukupna_vrijednost_fakure)
ukupna_vrijednost_fakure_entry.place(x = 480, y = 210)



#
# BUTTON
#

Button(root, text="UNESI", command=unos, background="grey").place(x = 100, y = 250)



ukupno_bez_pdv = Label(root, text = "Dobavljaceva vrijednost: ", fg= "red")
ukupno_bez_pdv.place(x= 600, y = 500)
suma_dob_vrijednosti = StringVar()
suma_dobavljac = Label(root, textvariable=suma_dob_vrijednosti, fg="red")
suma_dobavljac.place(x = 770, y = 500)


ukupno_pdv = Label(root, text="PDV : ", fg="red")
ukupno_pdv.place(x = 600, y = 530)
pdv_iznos = StringVar()
pdv_iznos2 = Label(root, textvariable=pdv_iznos, fg="red")
pdv_iznos2.place(x = 640, y = 530)


Ukupno_iznos = Label(root, text="Prodajna vrijednost s PDV : ", fg = "red")
Ukupno_iznos.place(x = 600, y = 560)
suma = StringVar()
suma2 = Label(root, textvariable=suma, fg="red")
suma2.place(x = 790, y = 560)


prod_bez_pdv = Label(root, text="Prodajna vrijednost bez PDV : ", fg = "red")
prod_bez_pdv.place(x = 600, y = 590)
suma_bez_pdv = StringVar()
suma_bez_pdv2 = Label(root, textvariable=suma_bez_pdv, fg="red")
suma_bez_pdv2.place(x = 790, y = 590)




Razlika_u_cijeni = Label(root, text="Razlika u cijeni :", fg="red")
Razlika_u_cijeni.place(x = 600, y = 620)
raz_u_cijeni = StringVar()
raz_u_cijeni2 = Label(root, textvariable=raz_u_cijeni, fg="red")
raz_u_cijeni2.place(x = 700, y =620)

pdv_izlazni_label = Label(root, text="PDV :", fg="red")
pdv_izlazni_label.place(x = 600, y = 650)
pdv_izlazni_suma = StringVar()
pdv_izlazni2 = Label(root, textvariable=pdv_izlazni_suma, fg="red")
pdv_izlazni2.place(x = 640, y =650)


mlb = MultiListbox(root, (('R. Broj', 2), ('Sifra artikla', 8), ('Naziv artikla', 26),('Komada', 7) ,('JM', 4), ('Dob. Cijena', 7),('Transport', 7),('Carina',7),('Nab. Vrijednost', 7), ('PDV-ulazni', 7),  ('Razlika u cijeni', 12), 
                            ('Prod. Cijena bez PDV', 8), ('PDV', 4), ('Prod. Cijena s PDV', 4)))
mlb.place(x= 100, y=  300)


#
# Pozovi DELETE
#

def pozovi_delete():

    global redni_broj, LISTA_ZA_PRINTING, razlika_u_cijeni_suma, pdv_izlazni


    index = mlb.item_selected[0]
    print index
    mlb.btn_del_click()
    print ZBIR_FAKTURE

    
    for y in ZBIR_FAKTURE:

        del y[index]
        suma_dob_vrijednosti.set(round(sum(dobavljaceva_vrijednost), 2))

        pdv_iznos.set(round(sum(pdv_ulazni_suma),2))

        suma.set(round(sum(prodajna_vrijednost_suma),2))

        raz_u_cijeni.set(round(sum(razlika_u_cijeni_suma),2))

        suma_bez_pdv.set(round(sum(prodajna_bez_pdv_suma),2))

        pdv_izlazni_suma.set(round(sum(pdv_izlazni),2))

    
    del LISTA_ZA_PRINTING[index]
    print LISTA_ZA_PRINTING
    redni_broj -= 1


Button(root, text="DELETE", command=pozovi_delete, background="grey").place(x = 180, y = 250)


#
# Write Funkcija
#

def ispisi():
    """ Ova funkcija ispisuje u file """

    global LISTA_ZA_PRINTING


    f2 = open("/home/pandemonium/Documents/Latica-Prijemnica"+ str(datum_variable) +"-"+ str(datum.hour) +":" +str(datum.minute)+".html", "w")

    f2.write("<body>")
    f2.write("<style> p.date {text-align:right;} \n")
    f2.write(".right { position: absolute;  right:0px; width:245px;}  .left { position: relative; left: 0px; width: 300px; border: 1px solid black; margin-bottom: 25px; font-size: 12px;}  .top { position: relative; top: 50px; left: auto; right: auto; margin-bottom: 30px;} img { float: left; }\
             .top-right { position: fixed; top: 20px; right: 30px; width: 300px; height: 200px; } </style>\n")
    
    f2.write('<div class="left"> <strong>Dobavljac:  </strong><p> '+ str(dobavljac.get()) + '  </p> <p> PDV: '+ str(dobavljac_pdv.get()) +'</p> <p> PIB: '+ str(dobavljac_pib.get()) +'</p> <p> Tel: '+ str(dobavljac_telefon.get()) + '</p><p> Adresa: '+ str(dobavljac_adresa.get()) + '</p> <p> Br.Fakture: ' + str(broj_racuna.get()) +' </p> </div> </center>\n')
    f2.write('<center><strong><p> Kalkulacija maloprodajne cijene </center> </strong> </p>')
    f2.write('<div class="top-right"><p> Datum : ' + str(datum_variable) + ' </p> <p> Redni broj prijemnice : ' + str(datum.year)+'-'+str(redni_broj_fakture[0])+' </p></div>')


    zadnji_red = ['<strong>', '', '<strong>UKUPNO</strong>', '' ,'', '<strong>' + str(round(sum(dobavljaceva_vrijednost), 2)),
                                                                     '<strong>' + str(transport.get()) , 
                                                                     '<strong>' + str(carina.get()), 
                                                                     '<strong>' + str(round(sum(nabavna_vrijednost_suma), 2)), 
                                                                     '<strong>' + str(round(sum(pdv_ulazni_suma),2)),
                                                                     '<strong>' + str(round(sum(razlika_u_cijeni_suma),2)),
                                                                     '<strong>' + str(round(sum(prodajna_bez_pdv_suma),2)),
                                                                     '<strong>' + str(round(sum(pdv_izlazni),2)),
                                                                     '<strong>' + str(round(sum(prodajna_vrijednost_suma),2)) ]
                            
    LISTA_ZA_PRINTING.append(zadnji_red)


    htmlcode = HTML.table(LISTA_ZA_PRINTING, header_row = ['R.Broj',   'Sifra',   'Naziv artikla', 'Kolicina','JM',  'Dob. Cijena', 'Transport', 'Carina', 'Nab. cijena', 'PDV-ulazni', 'Raz. u cijeni', 'Prod. Cijena bez PDV', 'PDV', 'Prd. Cijena s PDV'],
                                             col_width=['10%', '10%', '25%', '10%', '10%','10%','10%', '10%', '10%', '10%', '10%', '10%', '10%', '10%',] ,
                                             col_align=['center', 'center', 'center', 'center', 'center', 'center', 'center', 'center','center', 'center', 'center', 'center', 'center', 'center'], 
                                             col_styles=['font-size: 10px', 'font-size: 10px','font-size: 10px', 'font-size: 10px','font-size: 10px','font-size: 10px','font-size: 10px','font-size: 10px',
                                             'font-size: 10px','font-size: 10px',  'font-size: 10px', 'font-size: 10px', 'font-size: 10px', 'font-size: 10px'])

    
    
    f2.write('<center><div class="top"> ' + htmlcode + '<p>\n'+ '</center></div>\n')
    f2.close()
    pass



Button(root, text="ISPISI", command=ispisi, background="grey").place(x = 270, y = 250)
Button(root, text="Proknjizi", command=unos_u_bazu, background="grey").place(x = 350, y = 250)

print zavisni_troskovi_nabavke(165.36,4892.39)

sifra_entry.focus()

root.bind('<Delete>', pozovi_delete)
root.bind('<Return>', unos)
root.update_idletasks()

ocitavanje_rednog_broja_fakture()

root.mainloop()