from Tkinter import *
from ttk import *


def label_entry(frmlblent,txtlbl,txtlbl2=None):
    label=Label(frmlblent,text=txtlbl)
    label.pack(side=LEFT)
    frmlblent._entry=Entry(frmlblent)
    frmlblent._entry.pack(side=LEFT)
    if txtlbl2:
        label2=Label(frmlblent,text=txtlbl2)
        label2.pack(side=LEFT)
        frmlblent._entry2=Entry(frmlblent)
        frmlblent._entry2.pack(side=LEFT)
    
class FormMenu:
    
    def __init__(self,master):
        self.master=master
        self.frm_invoices=None
        self.frm_calendar=None

    def _init_widgets(self):
        #initiate toolbar
        self.toolbar = Frame(self.master)
        lbl0=Label(self.toolbar,text='Name of you Company').pack(side=LEFT)
        butcalc=Button(self.toolbar,text='Calc',command=self.calc_click).pack(side=LEFT)
        butcalendar=Button(self.toolbar,text='Calander',command=self.calendar_click).pack(side=LEFT)
        self.toolbar.pack(side='top',fill='x')
        
        style = Style()
        style.configure("BW.TLabel", foreground="white", background="black")


        #buttons frame
        #--------------------------------------------
        self.buttons = Frame(self.master, style="BW.TLabel")
        #button Fakturisanje
        self.btnproducts = Button(self.buttons,command=self.products_click)
        self.imgprdt=PhotoImage(file="img/products.gif")
        self.btnproducts['image']=self.imgprdt
        self.btnproducts.pack(side='top')
        lbl1=Label(self.buttons,text="Fakturisanje", style="BW.TLabel").pack()
        #button ino Dobavljac
        self.btninvoices = Button(self.buttons, text='Invoices...', command=self.invoices_click)
        self.imginv=PhotoImage(file="img/invoices.gif")
        self.btninvoices['image']=self.imginv
        self.btninvoices.pack(side='top')
        lbl2=Label(self.buttons,text="Unos - ino Dobavljac", style="BW.TLabel").pack()
        #button domaci Dobavljac
        self.btncustomers = Button(self.buttons, text='Customers...', command=self.customers_click)
        self.imgcust=PhotoImage(file="img/customers.gif")
        self.btncustomers['image']=self.imgcust
        self.btncustomers.pack(side='top')
        lbl3=Label(self.buttons,text="Unos - domaci Dobavljac.", style="BW.TLabel").pack()
        self.buttons.pack(side='left',padx=10)

         #button domaci Nivelacija
        self.btnnivelacija = Button(self.buttons, text='Nivelacija...', command=self.nivelacija_click)
        self.imgnivelacija=PhotoImage(file="img/nivel2.gif")
        self.btnnivelacija['image']=self.imgnivelacija
        self.btnnivelacija.pack(side='top')
        lbl4=Label(self.buttons,text="Nivelacija.", style="BW.TLabel").pack()
        self.buttons.pack(side='left',padx=10)


       
        #background label
        #-------------------------------------------
        self.imgback=PhotoImage(file="img/background.gif")
        self.lblbackground= Label(self.master, style="BW.TLabel",borderwidth=0)
        self.lblbackground.pack(side='top')
        self.lblbackground['image'] = self.imgback

    def calc_click(self):
        import os
        os.system(' python /home/pandemonium/Documents/Nova\ Faktura\ -\ Spajanje\ sve\ u\ jedan\ MENU/Fakturisanje/Fakturisanje-Gotovo.py')

    #calendar-------    
    def calendar_click(self):
        if self.frm_calendar==None:
            self.frm_calendar=ttkCalendar(master=self.master)
        elif self.frm_calendar.flag: #frm_products currently opened
            print ('already a window exists')
            return 0
        else:
            self.frm_calendar=ttkCalendar(master=self.master)
            
        print ('called wait window')
        self.master.wait_window(self.frm_calendar.top)
        print ('exited from wait window')
        print (self.frm_calendar.datepicked)
        
    def products_click(self):
        import os
        os.system(' python /home/pandemonium/Documents/Nova\ Faktura\ -\ Spajanje\ sve\ u\ jedan\ MENU/Fakturisanje/Fakturisanje-Gotovo.py')

        

    def invoices_click(self):
        import os
        os.system('python /home/pandemonium/Documents/Nova\ Faktura\ -\ Spajanje\ sve\ u\ jedan\ MENU/Kalkulacija\ -\ ino\ Dobavljac/kalkulacija-final.py')
        
        
    def customers_click(self):
        import os
        os.system('python /home/pandemonium/Documents/Nova\ Faktura\ -\ Spajanje\ sve\ u\ jedan\ MENU/Kalkulacija\ -\ domaci\ Dobavljac/kalkulacija-domaci.py')

    def nivelacija_click(self):
        import os
        os.system('python /home/pandemonium/Documents/Nova\ Faktura\ -\ Spajanje\ sve\ u\ jedan\ MENU/Nivelacija/nivelacija.py')
        
