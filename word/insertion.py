from __future__ import annotations

from tkinter.scrolledtext import ScrolledText
from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import showerror,askyesno
from sympy import *
from sympy.parsing.latex import parse_latex
init_printing()
from H.Apps.word.init_sympy import *
import io, H.Apps.word.verif_text as verif_text
from contextlib import redirect_stdout
from PersonalWidgets import PopingToplevel

carcteristics ={
    'latin' : [
        [range(65,91), range(97,123), range(192,214), range(216,247), range(248,383)],#range dans laquelle tous les caractères sont latins
        []#ceux à esquiver
    ],
    'grec' : 
    [
        [range(902,975)],#carctères grecs
        [903,907,909,930]#à part ceux-la
    ],
    'symbols' : [#etc.
        [range(33,65),range(91,97),range(123,127),range(161,192),range(215,217),range(247,248),range(448,452),range(697,880)],
        list(range(48,58)) + [37,43,60,61,62,247] + list(range(177,180)) + list(range(188,191)) + list(range(215,217))
    ],
    'math':[
        [range(37,38),range(43,44),range(177,180),range(188,191),range(215,217),range(247,248),range(8528,8543),range(8501,8502),range(8704,8841)],
        []
    ],
    'flèche':[
        [range(8592,8704)],
        []
    ],
    'romain':[
        [range(8544,8576)],
        []
    ]
}

get = {#k:ce qui est affiché, v:ce que comprends caracteristics
    "Caractères latins":'latin',
    "Grec":'grec',
    "Symboles":'symbols',
    "Caractères mathématiques":'math',
    "Flèches" : 'flèche',
    "Numération Romaine":'romain'
}


class InsertWindow(PopingToplevel):
    def __init__(self, master,text:Text|ScrolledText):
        """Insertion de caractères spéciaux"""
        super().__init__(master)
        self.transient(master)

        self.title("Insérer des caractères")
        self.geometry("500x375")

        self.text=text
        self.id = None

        
        self.ls = ttk.Combobox(self, values=list(get.keys()))#choix possibles
        self.ls.pack(padx=10,pady=10)
        self.ls.insert(0,'Choisissez la catégorie')
        self.ls.configure(state='readonly')

        self.frame1=Frame(self)
        self.frame1.pack()

        #on peux aussi directement donner un numéro si on le connais
        Label(self.frame1,text='Ou entrez le numéro du caractère : ').pack(side=LEFT)
        self.ent = Entry(self.frame1)
        self.ent.pack(pady=5,side=RIGHT)

        self.ent.bind("<Return>",self.check)

        ttk.Separator(master=self,orient=HORIZONTAL).pack(fill=X)

        self.ls.bind('<<ComboboxSelected>>',self.select)
        self.F =Frame(self)
        self.F.pack()
        
        #là ou on met tous les boutons
        self.c=Canvas(self.F)
        self.c.grid(row=0,column=0,sticky="news")
        self.vsb = Scrollbar(self.F, orient=VERTICAL)
        self.vsb.grid(row=0,column=1,sticky=NS)

        self.vsb.config(command=self.c.yview)

        self.c.bind_all("<MouseWheel>", self._on_mousewheel)

        self.fr=None

        self.lab = Label(self,text = 'Caractère choisi : ')
        self.lab.pack(side=LEFT)

        self.btn = Button(self,text='Insérer',command=self.insert)
        self.btn.pack(side=RIGHT)

    def check(self,*args):
        """Vérifier ce qui a été mis dans l'Entry"""
        if self.ent.get().isdigit():
            self.change(chr(int(self.ent.get())),int(self.ent.get()))
        else:
            showerror('Bad Index',"Vous devez entrer un nombre",parent=self)

    def select(self,*args):
        """Dessiner tous les boutons"""
        self.clear()
        self.create(carcteristics[get[self.ls.get()]][0],carcteristics[get[self.ls.get()]][1])
    
    def create(self,ranges,excepted):
        """Créer des boutons dont le texte est chr(i) pour tout i dans ranges si i n'est pas dans excepted"""
        self.fr=Frame(self.F)
        x=0
        for rang in ranges:
            for i in rang:
                if i in excepted: continue
                Button(self.fr,text=chr(i),width=4,command = lambda j=i:self.change(chr(j),j)).grid(row=x//10,column=x%10)
                x+=1
        self.c.create_window(0, 0,  window=self.fr)
        self.fr.update_idletasks()

        self.c.config(scrollregion=self.c.bbox("all"))
        self.c['yscrollcommand'] = self.vsb.set
        self.c.yview_moveto(0)

    def _on_mousewheel(self, event):
        try:
            self.c.yview_scroll(-1*(event.delta//120), "units")
        except:#eviter les erreurs après la fermeture de la fenêtre
            pass
    
    def change(self,car,num):
        """Montrer le caractère selectionné"""
        self.lab['text'] = 'Caractère choisi : ' + car + ' ; identifiant : '+str(num)
        self.id =num

    def clear(self):
        """Tout effacer"""
        children = self.children.copy()
        for child in children.values():
            if type(child) in (ttk.Separator,ttk.Combobox):
                continue
            if child in (self.F, self.c, self.vsb, self.lab, self.btn,self.frame1):
                continue 
            
            child.destroy()
        
        if self.fr != None:
            self.fr.destroy()
            self.fr=None
            self.c.config(scrollregion=self.c.bbox("all"))
            self.c['yscrollcommand'] = self.vsb.set
            self.c.yview_moveto(0)

    def insert(self):
        """Inserer dans le widget text"""
        if self.id == None:
            showerror("Aucun caractère choisi","Vous ne pouvez pas insérer un caractère que vous n'avez pas choisi",parent=self)
        else:
            self.text.insert(END,chr(self.id))


def insret_proc(master,text):
    """Appel rapide"""
    InsertWindow(master,text)

class FunctionWindow(PopingToplevel):
    def __init__(self, master,text):
        """insertion de fonctions mathématiques"""
        super().__init__(master)
        self.transient(master)
        self.resizable(0,0)
        self.title('Fonction')

        f=Frame(self)
        f.pack()
        #il faut les écrire comme dans le shell python
        Label(f,text='Entrée : ').pack(side=LEFT)
        frame1=Frame(self)
        frame1.pack()
        
        self.entry = Text(frame1,height=10,width=50)
        self.entry.pack(side=BOTTOM)

        frame2 = Frame(self)
        frame2.pack()
        Label(frame2,text='Sortie : ').grid(row=0,column=0)
        self.Latex = Button(frame2,text='En Latex',command=self.use_latex)
        self.Latex.grid(row=0,column=1)
        self.Unicode = Button(frame2,text='En Unicode',command=self.use_unicode)
        self.Unicode.grid(row=0,column=2)
        
        self.text = text
        self.update()
    
    def update(self):
        super().update()

        txt = self.entry.get(0.0,END)
        if not verif_text.well_parent(txt):#vérifier si il ya le bon nombre de ()
            self.Latex['state']='disabled'
            self.Unicode['state']='disabled'
        else:
            if self.Latex['state']=='disabled' and self.Unicode['state']=='disabled':
                self.Latex['state']='normal'
                self.Unicode['state']='normal'

        
        super().update()
        self.after(500,self.update)
    
    def use_latex(self):
        """Transformer en LaTeX"""
        try :
            f = io.StringIO()
            with redirect_stdout(f):
                exec("l = "+self.entry.get('0.0','end')+"\nprint_latex(l)")
            s=f.getvalue()
            if askyesno('Visualisation','Voici le résultat. Cela vous convient-il ?\n'+s,parent=self):
                self.text.insert('end',s)
                self.destroy()
        except Exception as err:
            showerror('Opérateur inconnu',f"Nous ne parvenons pas à créer l'opérateur '{self.entry.get('0.0','end')}', {err}",parent=self)

    def use_unicode(self):
        """Transformer en Unicode"""
        try :
            f = io.StringIO()
            with redirect_stdout(f):
                exec("l = "+self.entry.get('0.0','end')+"\nprinting.pprint(l)")
            s=f.getvalue()
            if askyesno('Visualisation','Voici le résultat. Cela vous convient-il ?\n'+s,parent=self):
                self.text.insert('end',s)
                self.destroy()
        except Exception as err:
            showerror('Opérateur inconnu',f"Nous ne parvenons pas à créer l'opérateur '{self.entry.get('0.0','end')}', {err}",parent=self)

def func_proc(master,text):
    FunctionWindow(master,text)


class EquaWindow(PopingToplevel):
    def __init__(self,master,text):
        """Permet de convertir du LaTeX en Unicode"""
        super().__init__(master)
        self.transient(master)
        self.resizable(0,0)
        self.title('Equation')

        f=Frame(self)
        f.pack()
        Label(f,text='Entrée (LaTeX): ').pack(side=LEFT)
        frame1=Frame(self)
        frame1.pack()
        
        self.entry = Text(frame1,height=10,width=50)
        self.entry.pack(side=BOTTOM)

        frame2 = Frame(self)
        frame2.pack()
        self.transform = Button(frame2,text="Convertir",command=self.parse)
        self.transform.pack()
    
        self.sortie =Text(self,height=10,width=50,state='disabled')
        self.sortie.pack()

        self.btn = Button(self,text='Exporter',command=self.export)
        self.btn.pack()

        
        self.text = text
        self.update()
    
    def parse(self):
        try:
            f = io.StringIO()
            with redirect_stdout(f):
                pprint(parse_latex(self.entry.get('0.0','end')))
            s=f.getvalue()
            self.sortie.delete('0.0','end')
            self.sortie.configure(state='normal')
            self.sortie.insert('0.0',s)
            self.sortie.configure(state='disabled')
        except Exception as err:
            showerror("Erreur",err,parent=self)
    
    def export(self):
        self.text.insert('end',self.sortie.get('0.0','end'))
        self.destroy()

def equa_proc(master,text):
    EquaWindow(master,text)

if __name__ == '__main__':
    tk=Tk()
    FunctionWindow(tk,None)
    tk.mainloop()