from __future__ import annotations

from tkinter import *
from tkinter.font import Font

class Style:
    def __init__(self,fg,bg,font:Font,text:Text=None):
        """Définit un style. Un style est caractérisé par une police, une couleur d'avant plan et une d'arriere plan."""
        self.desc = {
            'foreground':fg,
            'background':bg,
            'font':font
        }

        self.text = text#text sert pour créer le tag qui permettra d'appliquer le style
    
    def tag_create(self):
        """Créer le tag"""
        self.text.tag_configure(str(self),foreground=self.desc['foreground'],background=self.desc['background'],font=self.desc['font'])

    def tag_add(self,i1,i2='end'):
        """Ajouter le tag entre i1 et i2"""
        self.text.tag_add(str(self),i1,self.text.index(i2))
    
    def tag_remove(self):
        """Enlever le tag"""
        self.text.tag_remove(str(self),'0.0','end')
    
    def tag_update(self):
        """Modifier le tag"""
        self.text.tag_configure(str(self),foreground=self.desc['foreground'],background=self.desc['background'],font=self.desc['font'])
    
    def __call__(self,name=None,**kwds):
        """
        Si name=None et kwds vide -> renvoie la description du style
        Si name != None et kwds vide -> renvoie l'attribut name du descripteur
        Si name=None et kwds contient entre 1 et 3 args, modifie les attributs du descripteur chosit dans kwds
        Sinon renvoie une erreur
        """
        if len(kwds)>3 or (name !=None and len(kwds) !=0) :
            raise SyntaxError("Too many arguments have been passed.")
        if name !=None:
            return self.desc[name]
        elif len(kwds)>=1:
            for k in kwds.keys():
                self.desc[k] = kwds[k]
        else:
            return self.desc
    
    def save(self,f):
        """Enregistre le style dans un fichier."""
        with open(f+'.txt',"w") as file:
            file.write(self.__str__())

    def str_font(self):
        if self.desc['font'] =='TkFixedFont':return '"'+self.desc['font']+'"'
        return 'Font(family ="'+self.desc['font']['family']+'",size='+str(self.desc['font']['size'])+',slant="'+self.desc['font']['slant']+'",weight="'+self.desc['font']['weight']+'",underline='+str(self.desc['font']['underline'])+',overstrike='+str(self.desc['font']['overstrike'])+')'

    @classmethod
    def from_txt(self,l)->Style:
        with open(l,'r') as f:
            return eval(f.read())
    
    def __str__(self) -> str:
        return 'Style("'+str(self.desc['foreground'])+'","'+str(self.desc['background'])+'",'+self.str_font()+')'

class StyleGestion:
    def __init__(self):
        """Gestionnaire de style. Dict avec comme clé un nom de style et comme valeur le style"""
        self.styles = {}
    
    def add(self,name,desc:Style):#ajoute le style
        if name in self.styles:
            raise ValueError("Style already exists")
        assert type(desc) ==Style 

        self.styles[name]=desc
    
    def get(self,style=None)->Style:#renvoie un ou tous les styles
        if style == None:return self.styles
        assert style in self.styles
        return self.styles[style]