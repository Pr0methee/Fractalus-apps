from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import askyesno,showerror
from PersonalWidgets import PopingToplevel
from PIL import Image as PILImage, ImageTk
import os

class Vignette:
    """image dans la barre des taches"""
    def __init__(self,nom:str,can:Canvas,image,i):
        self.can=can
        self.i=i

        self.r=self.can.create_rectangle(30+45*i,self.can.winfo_height()-22.5,70+45*i,self.can.winfo_height(),fill='#80bfff',outline='#0080ff',tags=nom.replace(' ','_'))
        self.im=self.can.create_image(50+45*i,self.can.winfo_height()-11.25,image=image,anchor='center',tags=nom.replace(' ','_'))

    def destroy(self):
        self.can.delete(self.r,self.im)
    
    def redraw(self,i):
        self.i=i

        self.can.coords(self.r,30+45*i,self.can.winfo_height()-22.5,70+45*i,self.can.winfo_height())
        self.can.coords(self.im,50+45*i,self.can.winfo_height()-11.25)

class GestionApps(PopingToplevel):
    def __init__(self,master):
        """master doit avoir un attribut CANVAS !"""
        try:
            master.CANVAS
        except AttributeError:
            raise AttributeError("You're not using a good master.")
        
        self.d={}#app visibles
        self.h = {}#apps non visibles (horloge+baterie)
        self.images = {}
        self.started =False

        self.opened = False
        self.asking=False
        
        self.master = master
        self.instances:dict[(type,list)] = {}
        self.vignettelist:dict[(str,list[int,Vignette])]={}

        self.openwith = {}#dictionnaire -> k: nom app, v: ch. de car. qui dit quels types de fichier elle peut ouvrir
        self.icons = []
    
    def add(self,nom,proc,img=''):
        """ajoute une app"""
        assert nom not in self.d
        self.d[nom]=proc
        self.instances[nom]=[]
        self.images[nom]=img
    
    def add_hide(self,nom,proc,img=None,x=None,y=None):
        """ajoute une app cachée (horloge/batterie)"""
        assert nom not in self.h
        self.h[nom]=proc
        self.instances[nom]=[]
        if img != None:
            assert (x,y)!=(None,None)
            self.master.CANVAS.create_image(x,y,image=img,tag=nom,anchor='nw')
            if nom=='SELF':
                self.master.CANVAS.tag_bind(nom,'<Button-1>',lambda *args:self.show())
            else:
                self.master.CANVAS.tag_bind(nom,'<Button-1>',lambda *args:self.open(nom))
        else: assert (x,y)==(None,None)
    
    def open(self,proc_name):
        """Ouvre une app. On ne peut ouvrir qu'une fenetre de chaque app """
        assert proc_name in self.d.keys() or proc_name in self.h.keys()
        if proc_name in self.d:
            if self.instances[proc_name] == []:
                self.draw_vignette(len([proc for proc in self.d if self.instances[proc]!=[]])+1,proc_name)
                self.master.update()
                self.instances[proc_name].append(self.d[proc_name](self.master))                
                
            else:#si l'app est déjà ouverte, on propulse la fenetre au 1er plan
                self.instances[proc_name][0].poping()
        else:
            if self.instances[proc_name] == []:
                self.instances[proc_name].append(self.h[proc_name](self.master))
            else:#si l'app est déjà ouverte, on propulse la fenetre au 1er plan
                self.instances[proc_name][0].poping()
      
    def start(self):
        """dessine la barre des taches"""
        self.started=True
        self.bdt=self.master.CANVAS.create_rectangle(0,self.master.CANVAS.winfo_height(),self.master.CANVAS.winfo_width(),self.master.CANVAS.winfo_height()-25,fill='#7d7d7d',outline='#7d7d7d')
    
    def draw_vignette(self,i,which):
        """dessine une vignette dans la barre des taches"""
        can:Canvas=self.master.CANVAS
        self.vignettelist[which]=[i,Vignette(which,can,self.images[which]('Vignette'),i)] 

    def update(self):
        """Mise a jour"""
        if not self.started:return
        self.master.winfo_exists()#arrête la maj si c'est fini

        for proc in self.instances:#effacer les instances terminées
            if self.instances[proc]!=[] and not self.instances[proc][0].winfo_exists():
                self.instances[proc]=[]
            
            if proc in self.vignettelist and self.instances[proc]==[]:
                self.vignettelist[proc][1].destroy()#enlever la vignette
                del self.vignettelist[proc]

        #redessiner les vignettes
        s= {self.vignettelist[proc][0] for proc in self.vignettelist}#liste des places des vignettes
        if len(s)==0:return#on arrête si il n'y a aucune vignette 
        S={i+1 for i in range(max(s))}
        if S==s:return#si il n'y a aucun trou dans la barre des taches
        k=[k for k in self.vignettelist]
        for proc in self.vignettelist:
            self.vignettelist[proc][1].redraw(k.index(proc)+1)
    
    def draw_icone(self,which:str,i:int):
        """dessine une icone sur le burreau"""
        can:Canvas=self.master.CANVAS
        self.icons.append(can.create_image(25+100*(i//8),25+100*(i%8),image=self.images[which]('icone'),anchor='nw',tag=which.replace(' ','_')))
        can.tag_bind(which.replace(' ','_'),'<Button-1>',lambda *args:self.open(which))
    
    def draw(self):
        """dessine toutes les icones"""
        for i,proc in enumerate(self.d):
            self.draw_icone(proc,i)

    def show(self):
        """ouverture du gestionnaire d'app"""
        if self.opened:
            return
        super().__init__(self.master)
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW",self.reset)
        self.transient(self.master)
        self.title("Logiciels")
        self.iconphoto(False,ImageTk.PhotoImage(PILImage.open(r"H\Apps\desktools\koch.png")))

        self.opened=True

        self.list=ttk.Treeview(self,show='tree')#,width=25,selectmode=SINGLE
        self.list.pack()

        for x in self.d:
            self.list.insert('',END,text=x,image=self.images[x]('list'))

        self.geometry("200x200+20+"+str(self.master.CANVAS.winfo_height()-258))
        self.bind("<Configure>",lambda *args:self.geometry("200x200+20+"+str(self.master.CANVAS.winfo_height()-258)))
        self.bind("<Leave>",self.reset)
        
        self.bind('<<TreeviewSelect>>',self.open_)        

    def add_infos(self,app,files:str):
        """dire avec quelle app s'ouvrent les fichiers .files"""
        if files.count(' ')==1:
            files.replace(' ','')
            self.openwith[files]=app
        elif files.count(' ')==0:
            self.openwith[files]=app
        else:
            for elt in files.split(' '):
                self.openwith[elt]=app
    
    def open_file(self,link):
        """Ouvrir {link} avec l'app dédiée"""
        ext=os.path.splitext(link)[1]
        app = self.openwith.get(ext,False)
        
        if app == False:
            self.master.bell()
            showerror("Impossible d'ouvrir le fichier","Oups...\nIl n'y a aucune application disponible pour ouvrir les fichiers '"+ext+"'")
            return

        if self.instances[app]==[]:
            self.instances[app].append(self.d[app](self.master,link))
            self.draw_vignette(len([proc for proc in self.d if self.instances[proc]!=[]]),app)
        else:
            self.instances[app][0].open(link)

    def reset(self,*args):
        """effacer la fenetre"""
        self.opened=False
        self.destroy()
    
    def open_(self,*args):
        """ouvrir une app"""
        if self.asking:return
        proc = self.list.item(self.list.focus())['text']
        self.asking=True
        if askyesno("Ouvrir ?","Voulez-vous ouvrir l'application "+proc+" ?",master=self):
            self.open(proc)
        self.asking=False

    def end(self):
        """tout effacer"""
        self.started=False
        for i in self.icons+[self.bdt]:
            self.master.CANVAS.delete(i)
        for item in self.vignettelist.values():
            self.master.CANVAS.delete(item[1].im,item[1].r)
        for proc in self.instances.values():
            if proc != []:
                proc[0].destroy()