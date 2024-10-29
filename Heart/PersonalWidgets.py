__doc__="""
Module qui définit certaines fenêtres graphiques
"""

from tkinter import Frame,Toplevel,Label
import tkinter.colorchooser as colorchooser
from tkinter.ttk import Progressbar

class ColorChooserButton(Frame):
    def __init__(self,master,default):
        """Bouton permetant de selectionner une couleur et de l'afficher"""
        super().__init__(master, width=15,height=15,relief='solid',borderwidth=2,bg=default)#il s'agit en fait d'une Frame de 15x15
        self.bind("<Button-1>",self.clic)#si on clique sur ce bouton, l'utilisateur veut choisir une autre couleur
    
    def clic(self,*args):
        """Permet à l'utilisateur de choisir une couleur"""
        responce= colorchooser.askcolor(self.get(),parent=self)
        if responce != (None,None):#si l'utilisateur n'a pas fermé la boite de dialogue...
            self['bg']=responce[1]#on change la couleur de fond

    def get(self):
        """Renvoie la couleur qui a été choisie"""
        return self['bg']
    
    def set(self,colour):
        """Change la couleur"""
        self['bg']=colour

class ProgressWindow(Toplevel):
    def __init__(self,master):
        """Fenêtre toplevel qui permet d'afficher une barre de chargement qui indique à l'utilisateur de patienter"""
        super().__init__(master)
        self.title('Please Wait')
        self.p = Progressbar(self,length=250,mode='indeterminate')
        self.p.pack()
    
    def start(self):
        """Lancer le défilement"""
        self.p.start()
    
    def end(self):
        """Arrêter"""
        self.destroy()

class LabeledWidget(Frame):
    def __init__(self,master,text,widget,labside='left',lpady=1,widside='right',wpady=1):
        """
        Widget avec un Label.
        L'argument widget doit être une fonction lambda avec pour paramètre la fenetre mère dudit widget.
        Par exemple : lambda master: Entry(master)
        """
        super().__init__(master)
        Label(self,text=text).pack(side=labside,pady=lpady)#on place le label
        self.wid = widget(self)
        self.wid.pack(side=widside,pady=wpady)#puis le widget
    
    def get(self):
        """Renvoie la valeur du widget"""
        return self.wid.get()
    
    def set(self,arg):
        """Change la valeur du widget"""
        self.wid.set(arg)

class PopingToplevel(Toplevel):
    def poping(self):
        #self.deiconify()
        self.wm_attributes('-topmost',1)
        self.wm_attributes('-topmost',0)