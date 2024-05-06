"""Calculatrice booléenne"""

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from sympy import *
from PersonalWidgets import PopingToplevel

#les symboles
x=Symbol('x')
y=Symbol('y')

#transformer 0 et 1 en symbole pour permettre le calcul
zero=Symbol("Z")
un=Symbol("U")

class BoolExec:
    """Permet de faire certains calculs grace aux propriétés de De Morgann inconnue de sympy"""
    def __init__(self,p):

        if str(x&~x) in p:
            p=p.replace(str(x&~x),'0')
        if str(y&~y) in p:
            p=p.replace(str(y&~y),'0')
        if str(x|~x) in p:
            p=p.replace(str(x|~x),'1')
        if str(y|~y) in p:
            p=p.replace(str(y|~y),'1')
        self.v=p
    
    def get(self):
        return self.v

class Calculator(PopingToplevel):
    def __init__(self,master):
        """Création"""
        super().__init__(master)
        self.transient(master)
        self.title("Boole Calculator")
        self.iconphoto(False,PhotoImage(file=r"H\Apps\BooleCalc\BooleCalculator.png"))

        self.cadre = Frame(self,borderwidth=2,width=250,height=50,relief=SOLID)
        self.cadre.pack(padx=5,pady=5)
        self.cadre.pack_propagate(False)

        self.label=Label(self.cadre,text='')
        self.label.pack(side=RIGHT)

        self.execs = []

        f1 = Frame(self)
        f1.pack()

        ttk.Button(f1,text="x",width=9,command=lambda:self.write("x","x")).pack(side=LEFT)
        ttk.Button(f1,text="y",width=9,command=lambda:self.write("y","y")).pack(side=LEFT)
        ttk.Button(f1,text="(",width=9,command=lambda:self.write("(","(")).pack(side=LEFT)
        ttk.Button(f1,text=")",width=9,command=lambda:self.write(")",")")).pack(side=LEFT)

        f2 = Frame(self)
        f2.pack()

        ttk.Button(f2,text="¬",width=9,command=lambda:self.write("¬","~")).pack(side=LEFT)#non
        ttk.Button(f2,text="∧",width=9,command=lambda:self.write("∧","&")).pack(side=LEFT)#et
        ttk.Button(f2,text="∨",width=9,command=lambda:self.write("∨","|")).pack(side=LEFT)#ou
        ttk.Button(f2,text="⊕",width=9,command=lambda:self.write("⊕","^")).pack(side=LEFT)#ou exclusif
    
        f3 = Frame(self)
        f3.pack()

        ttk.Button(f3,text="0",width=9,command=lambda:self.write("0","zero")).pack(side=LEFT)
        ttk.Button(f3,text="1",width=9,command=lambda:self.write("1","un")).pack(side=LEFT)
        ttk.Button(f3,text="⌫",width=9,command=self.delete).pack(side=LEFT)#effacer
        ttk.Button(f3,text="exe",width=9,command=self.exec).pack(side=LEFT)
    
    def write(self,car,e):
        """Ecrire un caractère"""
        self.label['text']=self.label['text']+car#sur l'affichage
        self.execs.append(e)#dans la liste à executer
    
    def delete(self):
        """Supprimer le dernier élément"""
        if self.label['text']!='':
            self.label['text']=self.label['text'][:-1]
            self.execs.pop()
    
    def exec(self):
        """Faire le calcul"""
        try:
            f=''.join(self.execs)
            f=eval(f)
            f=str(f.replace(zero,False).replace(un,True))
            expr=f.replace('False','0').replace('True','1')
            expr=BoolExec(expr).get()
            expr=str(eval(expr.replace('0','zero').replace('1','un')).replace(zero,False).replace(un,True)).replace('False','0').replace('True','1')
            self.execs=replace(replace(list(expr),'0','zero'),'1','un')
            
            self.label['text']=expr.replace("~","¬").replace("&","∧").replace("|","∨").replace("^","⊕")
        except Exception as err:
            messagebox.showerror("Syntax error","Invalid Syntax"+str(err))
    
    def run(self):
        self.mainloop()

def replace(l:list,old,new):
    """Remplace tous les old de l par des new"""
    r=[]
    for it in l :
        if it == old:
            r.append(new)
        else:
            r.append(it)
    return r

if __name__ == '__main__':
    root=Tk()
    c=Calculator(root)
    c.run()