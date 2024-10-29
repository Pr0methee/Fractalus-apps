import time
from tkinter import *
import tkinter.messagebox as messagebox
from win32api import GetSystemMetrics#permet d'avoir les dimensions de l'écran
from PersonalWidgets import PopingToplevel

SYMBOLS = list("""&~"#'{([-|`_\\^@°)]+=}¨^$£¤%µ*§!:/;.,?<>²""")
DIGITS = list("1234567890")

class RadioChooser(Frame):
    def __init__(self,master:Tk,buttons:list,setvalue:int=0):
        """Crée une Frame avec plusieurs radioboutons dans la fenetre master"""
        #buttons est une liste de tuple ou chaque tuple est sous la forme (label,onvalue)
        super().__init__(master)
        self.var = IntVar()
        n=0
        
        for but in buttons:
            assert type(but) == tuple
            assert len(but)==2
            btn=Radiobutton(self,text=but[0],variable=self.var,value=but[1])
            btn.pack(side=LEFT)
            if n== setvalue:
                btn.select()
            n+=1


        master.update()
        master.update_idletasks()

    def get(self):
        """Renvoie le bouton choisit"""
        return self.var.get()

class Formulaire(PopingToplevel):

    def __init__(self,master,title:str=''):
        """
        Classe d'un formulaire graphique avec tkinter.\n
        L'instanciation crée une fenêtre de saisie provisoirement vide avec uniquement le titre du formulaire.\n
        Utilisez ensuite la méthode add_champ pour ajouter une ligne à votre formulaire.\n
        Vous pouvez utiliser cette méthode autant de fois que vous voulez.\n
        Créez ensuite le bouton "submit" (add_submit). Le formulaire est désormais vérouillée, vous ne pouvez alors plus ajouter de champ.\
            Vous pouvez désormais lancer le formulaire avec la méthode run
        """
        
        super().__init__(master)
        self.transient(master)
        #master.protocol("WM_DELETE_WINDOW",self.destroy())
        self.resizable(0,0)

        if title=='':
            title='Formulaire'
        Label(self,text=title).pack()
        
        xmax = GetSystemMetrics(0)
        ymax = GetSystemMetrics(1)
        x0 = self.x0 = xmax/2 - self.winfo_width()/2
        y0 = self.y0 = ymax/2 - self.winfo_height()/2
        self.geometry("+%d+%d" % (x0, y0))#centrer la fenetre

        self.entries=[]
        self.help_text=[]
        self.help_lab=[]
        self.verifications = []
        
        self.locked =False#état : vérouillé ou non
        self.values= False
        self.ask_conf = False

    def add_champ(self,lab:str,champ,verif,help:str,pre:str=''):
        """
        lab est un str qui correspond au label pour demander une information

        champ doit être une fonction lambda du type :
        lambda master: Entry(master)...

        verif doit être une fonction lambda du type:
        lambda selec : selec != '' ...
        
        help est un str qui donne une aide à l'utilisateur si il y a une erreur dans sa saisie

        Impossible d'utiliser cette fonction après que le formulaire soit totalement créé
        """

        if self.locked:
            raise RuntimeError("Can't add a row, this app has been locked !")

        f=Frame(self)
        f.pack(side=TOP,pady=7)
        Label(f,text=lab).grid(row=0,column=0)
        self.entries.append(champ(f))
        if pre != '':
            self.entries[-1].insert(0,pre)
        if lab[-1]=='\n':
            self.entries[-1].grid(row=1,column=0)
        else:
            self.entries[-1].grid(row=0,column=1)
        self.help_lab.append(Label(f,text='',foreground='red'))
        self.help_lab[-1].grid(row=0,column=2)
        self.help_text.append(help)
        self.verifications.append(verif)
    
    def add_submit(self,text:str='Soumettre',conf:bool=False):
        """
        Ajoute le boutton de soumission.
        Bloque la modification de l'app
        """
        assert self.locked == False, "Can't create submit button: you have already done it."
        self.btn = Button(self,text=text,command=self.verificate)
        self.btn.pack()
        self.locked =True
        self.ask_conf = conf

    def verificate(self):
        l=[]
        for i in range(len(self.entries)):
            if self.verifications[i] != None:
                a = self.verifications[i](self.entries[i].get())
                if not a:
                    self.help_lab[i]['text'] = self.help_text[i]
                else:
                    self.help_lab[i]['text'] = ''
                l.append(a)
        
        if all(l):
            if self.ask_conf:
                if messagebox.askyesno("Confirmer","Confirmez-vous les informations saisies ?",parent=self):
                    self.values = [e.get() for e in self.entries]
                    self.destroy()
            else:
                self.values = [e.get() for e in self.entries]
                self.destroy()

    def run(self):
        """Lance le formulaire. Ne peut se faire que si il est vérouillé"""
        assert self.locked, "Can't run. '%s' is not locked"%(self)
        
        while self.values == False:
            try:
                assert self.winfo_exists()
                self.update()
                time.sleep(1e-5)
            except :#erreur : le client à cliqué sur la croix pour fermer la fenêtre
                return False
        return self.values
    
    def end(self):
        self.values=None

def no_symbols(ch:str)->bool:
    """Renvoie True si ch ne contient aucun symbole"""
    for car in ch:
        if car in SYMBOLS:
            return False
    return True

def no_digits(ch:str)->bool:
    """Renvoie True si ch ne contient aucun chiffre"""
    for car in ch:
        if car in DIGITS:
            return False
    return True    

def is_int(ch:str):
    """Renvoie True si ch est un nombre"""
    try:
        int(ch)
        return True
    except:
        return False

def is_ip(ch:str):
    """Renvoie True si ch est une adresse IP"""
    if ch.count('.')!=3:
        return False
    
    l=ch.split('.')
    return all(is_int(n) for n in l)