from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.colorchooser as colorchooser
import tkinter.font as font
from PersonalWidgets import PopingToplevel

class MEFWindow(PopingToplevel):
    def __init__(self, master,gestionaire):
        """Gestionnaire de mise en forme"""
        super().__init__(master)

        self.gestion =gestionaire
        self.transient(master)
        self.title("Styles par défaut")

        self.liste = ttk.Combobox(self,state='readonly',values=list(gestionaire.get().keys()))
        self.liste.pack()
        self.liste.bind("<<ComboboxSelected>>",self.styleselected)
        ttk.Separator(self).pack(fill=X)

        self.labtitle = Label(self,text="Style : ")
        self.labtitle.pack(pady=10)

        topframe=Frame(self,height=25)
        topframe.pack(pady=5)

        Label(topframe,text='Couleur de Police : ').pack(side=LEFT)
        self.btnfgcol=Frame(topframe,height=15,width=15,bg='SystemButtonFace',relief=SOLID,borderwidth=2)
        self.btnfgcol.pack(side=RIGHT)
        self.fglocked = False
        self.btnfgcol.bind("<Button-1>",lambda arg :self.changecol("fg"))
    
        secondframe=Frame(self,height=25)
        secondframe.pack(pady=1)

        Label(secondframe,text="Couleur d'Arrière-Plan : ").pack(side=LEFT)
        self.btnbgcol=Frame(secondframe,height=15,width=15,bg='SystemButtonFace',relief=SOLID,borderwidth=2)
        self.btnbgcol.pack(side=RIGHT)
        self.bglocked=False
        self.btnbgcol.bind("<Button-1>",lambda arg :self.changecol("bg"))

        thirdframe=Frame(self)
        thirdframe.pack(pady=1)

        Label(thirdframe,text='Taille de Police : ').pack(side=LEFT)
        self.s =ttk.Spinbox(thirdframe,from_=1,to=100)
        self.s.pack(side=RIGHT)
        
        fourthframe=Frame(self)
        fourthframe.pack(pady=1)

        Label(fourthframe,text='Nom de la Police : ').pack(side=LEFT)
        self.fonts = ttk.Combobox(fourthframe,state='readonly',values=list(font.families())+['TkFixedFont'])
        self.fonts.pack(side=RIGHT)
        self.fonts.bind("<<ComboboxSelected>>",self.changepol)
                
        fifthframe=Frame(self)
        fifthframe.pack(pady=1)

        Label(fifthframe,text='Effet du texte : ').pack()
        
        self.itvar = BooleanVar()
        Checkbutton(fifthframe,text='Italique',variable=self.itvar,onvalue=1, font=font.Font(family="TkFixedFont",slant='italic',size=10)).pack(side=LEFT)

        self.boldvar = BooleanVar()
        Checkbutton(fifthframe,text='Gras',variable=self.boldvar,onvalue=1,font=font.Font(family="TkFixedFont",weight='bold',size=10)).pack(side=RIGHT)

        self.undvar = BooleanVar()
        Checkbutton(fifthframe,text='Souligné',variable=self.undvar,onvalue=1,font=font.Font(family="TkFixedFont",underline=1,size=10)).pack(side=RIGHT)

        self.overvar = BooleanVar()
        Checkbutton(fifthframe,text='Barré',variable=self.overvar,onvalue=1,font=font.Font(family="TkFixedFont",overstrike=1,size=10)).pack(side=RIGHT)

        Button(self,text="Enregistrer",command=self.save).pack(side=BOTTOM)

        self.disabled_all()

    def changecol(self,where):
        if where == 'fg' and not self.fglocked:
            responce = colorchooser.askcolor(self.btnfgcol['bg'],parent=self)
            if responce != (None,None):
                self.btnfgcol['bg']=responce[1]
                for child in self.children.values():
                    if type(child)==Label:
                        child['fg']=responce[1]
        elif where == 'bg' and not self.bglocked:
            responce = colorchooser.askcolor(self.btnbgcol['bg'],parent=self)
            if responce != (None,None):
                self.btnbgcol['bg']=responce[1]
                for child in self.children.values():
                    if type(child)==Label:
                        child['bg']=responce[1]

    def disabled_all(self):
        for child in self.children.values():
            if type(child)==Frame:
                for child_ in child.children.values():
                    if type(child_) in (ttk.Spinbox,ttk.Combobox,Checkbutton):
                        child_['state']='disabled'
            elif type(child)==Button:
                child['state']='disabled'

        self.fglocked = True
        self.bglocked = True

    def able_all(self):
        for child in self.children.values():
            if type(child)==Frame:
                for child_ in child.children.values():
                    if type(child_) in (ttk.Spinbox,ttk.Combobox,Checkbutton):
                        child_['state']='normal'
            elif type(child)==Button:
                child['state']='normal'
        
        self.fglocked = False
        self.bglocked = False
    
    def styleselected(self,*args):
        self.labtitle['text']="Style : "+self.liste.get()
        self.btnbgcol['bg']=self.gestion.get(self.liste.get())()['background']
        self.btnfgcol['bg']=self.gestion.get(self.liste.get())()['foreground']
        
        if self.gestion.get(self.liste.get())()['font'] == 'TkFixedFont':
            self.defaultview()
        else:
            self.able_all()
            if self.gestion.get(self.liste.get())()['font']['size'] !=0:
                self.s.set(self.gestion.get(self.liste.get())()['font']['size'])
            else:
                self.s.set(10)

            self.itvar.set(self.gestion.get(self.liste.get())()['font']['slant']=='italic')
            self.boldvar.set(self.gestion.get(self.liste.get())()['font']['weight']=='bold')
            self.undvar.set(self.gestion.get(self.liste.get())()['font']['underline']==1)
            self.overvar.set(self.gestion.get(self.liste.get())()['font']['overstrike']==1)
            self.fonts.set(self.gestion.get(self.liste.get())()['font']['family'])
    
    def changepol(self,*args):
        if self.fonts.get() == 'TkFixedFont':
            self.defaultview()
        else:
            self.able_all()

    def defaultview(self):
        """Visualisation si la police est 'TkFixedFont'."""
        self.disabled_all()
        self.s.configure(state="disabled")
        self.fglocked = False
        self.bglocked = False
        self.fonts.configure(state='normal')
        self.fonts.set("TkFixedFont")
        self.s.set('')
        self.itvar.set(False)
        self.boldvar.set(False)
        self.undvar.set(False)
        self.overvar.set(False)
        for child in self.children.values():
            if type(child)==Button:
                child.configure(state="normal")
    
    def save(self):
        style =self.liste.get()
        if self.fonts.get()=="TkFixedFont":
            fnt = self.fonts.get()
        else:
            it = {True:'italic',False:'roman'}.get(self.itvar.get())
            bold = {True:'bold',False:'normal'}.get(self.boldvar.get())
            under = int(self.undvar.get())
            over = int(self.overvar.get())
            if self.s.get()=='':self.s.set(0)
            fnt = font.Font(family=self.fonts.get(),size=int(self.s.get()),slant=it,weight=bold,underline=under,overstrike=over)

        self.gestion.get()[style](font=fnt,foreground=self.btnfgcol['bg'],background=self.btnbgcol['bg'])
        self.gestion.get()[style].tag_update()
        self.gestion.get()[style].save("H\\cache\\word\\"+style)
        self.destroy()
        
if __name__ == '__main__':
    tk=Tk()
    MEFWindow(tk)
    tk.mainloop()