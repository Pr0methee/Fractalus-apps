from __future__ import annotations
from tkinter import *
import tkinter.ttk as ttk
import os,time
import tkinter.messagebox as messagebox
from PIL import ImageTk
from PersonalWidgets import PopingToplevel
import resize

class ALL:
    """Tout"""
    pass

class DialogFileWindow(PopingToplevel):
    """Classe de Base pour toutes les apps necessitant de visualiser l'arborescence"""
    def __init__(self,master,path,last,authorised:list[tuple]|ALL,alias:dict={},commands={'Open':lambda:None,'Browse':lambda:None}):
        super().__init__(master=master)
        self.transient(master)

        self.geometry('500x250')
        self.resizable(0,0)
        self.CWD=path#Curent working directory
        self.LAST=last#on ne peut pas revenir avant
        self.alias=alias#changer le nom
        self.authorised=authorised#type qu'on peut montrer
        self.chose=None#choisit
        self.commands=commands#commandes à utiliser si le bouton est 'Browse' ou 'Open'

        f1=Frame(self)
        f1.pack(side='left',expand=True,fill='y')

        self.tree = ttk.Treeview(f1)#Treeview: montrer l'arborescence
        self.tree.heading('#0', text=path)

        self.scrollbar = ttk.Scrollbar(f1, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(expand=True,fill='y',side='left')

        self.tree.pack(fill=Y,expand=True,side='right')

        self.folder = PhotoImage(file =r'H\Apps\explorateur\dos4.png')
        self.page = PhotoImage(file =r'H\Apps\explorateur\page2.png')

        self.f2=Frame(self)
        self.f2.pack(side=LEFT)

        self.txt = Text(self.f2,height=14,width=50,state='disabled')#info sur les fichiers/dossier
        self.txt.pack(side=TOP)
        
        self.btn=Button(self.f2,text='')
        self.btn.pack(side=LEFT)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.poping()
    
    def clearall(self):
        """effacer le contenu du treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def openfolder(self,ext,cc=True):
        """changer le CWD.
        cc:est-ce qu'on montre le '..'"""
        if ext==None or self.chose=='':
            return 
        if ext!='..':
            self.CWD += ext+'\\'  
        else:
            if self.CWD == self.LAST or self.CWD == self.LAST+'\\':
                self.bell()
            else:
                self.CWD = '\\'.join(self.CWD.split('\\')[:-2])+'\\'
            self.chose=None
        self.actualise(cc)
    
    def actualise(self,cc,*args):
        """Afficher le CWD dans le treeview"""
        head =self.CWD
        for elt in self.alias:
            head=head.replace(elt,self.alias[elt])#on affiche le CWD sans les infos indésirables (remonter trop loin dans l'arborescence)
        self.tree.heading("#0",text=head)

        self.clearall()
        if cc:
            self.tree.insert('',END,text='..',image=self.folder)

        try:
            for link in os.listdir(self.CWD):
                photo= self.page
                typ = os.path.splitext(link)[1]
                if typ=='':
                    photo=self.folder
                elif self.authorised != ALL and typ not in self.authorised:
                    continue
                    
                self.tree.insert('',END, text=link,image=photo)

        except Exception as err:
            print(err)
        
    def on_select(self,event):
        """action a executer quand un item est selectionné"""
        self.chose =self.tree.item(self.tree.focus())['text']
        if self.chose=='':return
        self.txt.configure(state='normal')
        
        self.txt.delete('0.0','end')
        if self.chose!='..':
            self.txt.insert('end','Nom : '+self.chose+'\n')#nom du dossier/fichier
        
        if os.path.splitext(self.chose)[1]=='':#si c'est un dossier
            if self.chose!='..':
                self.txt.insert('end',str(len(os.listdir(self.CWD+'\\'+self.chose)))+' éléments')#on affiche le nombre d'élément
            self.btn['text']='Browse'
            self.btn['command']=self.commands['Browse']
        else:#sinon la taille
            self.txt.insert('end',str(os.path.getsize(self.CWD+'\\'+self.chose))+' o')
            self.btn['text']='Open'
            self.btn['command']=self.commands['Open']
        self.txt.configure(state='disabled')
    
    def add_inf2(self,obj):
        """permet d'ajoute qqch à coté du bouton"""
        return obj(self.f2)

    def set_authorised(self,new):
        """Changer la liste des types qu'on peut afficher"""
        self.authorised=new

class Explorateur(DialogFileWindow):
    def __init__(self, master, path, last, alias: dict = {},opencom=None):
        super().__init__(master, path, last, ALL, alias,{'Open':lambda:opencom(self.CWD+self.chose),'Browse':lambda :self.openfolder(self.chose)})
        self.title("Explorateur")
        icon = ImageTk.PhotoImage(file=r"H\Apps\explorateur\explorateur.gif")
        self.iconphoto(False,icon)
        self.openfolder('')
        self.nd = self.add_inf2(lambda master:Button(master,text="Nouveau Dossier",command=self.new))#créer un nv dossier
        self.nd.pack(side=RIGHT)

        self.tree.bind("<Delete>",self.suppr)#commande supprimer qqch

    def new(self):
        """lance l'attente de saisie de nom de dossier"""
        self.btn.configure(state='disabled')
        self.nd.configure(text='X',command=self.close)
        self.txt.configure(state='disabled')

        self.en=self.add_inf2(lambda master:Entry(master))
        self.en.pack()
        self.en.bind("<Return>",self.add)
    
    def close(self):
        """arrêter l'attente du nom de dossier"""
        self.en.destroy()
        self.btn.configure(state='normal')
        self.nd.configure(text='Nouveau Dossier',command=self.new)
        self.txt.configure(state='normal')
    
    def add(self,*evt):
        """Tente de créer le dossier"""
        if self.en.get()=='':#si l'entrée est vide -> fin
            self.en.destroy()
            self.btn.configure(state='normal')
            self.nd.configure(text='Nouveau Dossier',command=self.new)
            self.txt.configure(state='normal')
        elif os.path.exists(self.CWD+'\\'+self.en.get()):# si déjà existant -> erreur
            messagebox.showerror('Dossier existant',"Impossible de recréer le dossier")
        else:#sinon on essaie de le crée
            try:
                os.mkdir(self.CWD+'\\'+self.en.get())
                self.en.destroy()
                self.btn.configure(state='normal')
                self.nd.configure(text='Nouveau Dossier',command=self.new)
                self.txt.configure(state='normal')

                self.actualise(True)
            except Exception as err:#mauvais nom de dossier
                messagebox.showerror('Oups...',"Il y a un soucis dans le nom de votre dossier...")
                self.bell()

    def suppr(self,*evt):
        if self.tree.item(self.tree.focus())['text'] != '' and self.tree.item(self.tree.focus())['text']!='..':#faire attention à ce qui est selectionné
            if messagebox.askyesno("Attention !","Voulez-vous supprimer le fichier/dossier ? Cette action est irréversible."):#avertissement
                try:
                    os.remove(self.CWD+'\\'+self.chose)
                except:
                    os.rmdir(self.CWD+'\\'+self.chose)
        self.actualise(True)

class Opener(DialogFileWindow):
    def __init__(self, master,path,last,authorised:list[tuple],alias:dict={}):
        """Permettre d'ouvrir un fichier"""
        super().__init__(master,path,last,authorised,alias,{'Open':self.open,'Browse':lambda :self.openfolder(self.chose)})
        self.title("Ouvrir")

        self.opened=None

        #faire defiler les types possibles
        self.combo = self.add_inf2(lambda master :ttk.Combobox(master,values=tuple(k[0]+' '+k[1] for k in authorised),state='readonly'))
        self.combo.pack(side=RIGHT)
        self.combo.set(authorised[0][0]+' '+authorised[0][1])
        self.combo.bind('<<ComboboxSelected>>',self.actualise)

        self.openfolder('')
          
    def actualise(self,*args):
        """changer les extensions autorisées"""
        self.set_authorised(self.combo.get().split(' ')[1:])
        super().actualise(True)
    
    def open(self):
        """choisir le fichier"""
        self.opened = self.CWD+self.chose
    
    def run(self):
        """Boucle principale : on attend qu'un fichier soit choisit puis on le retourne"""
        while self.opened==None:
            self.update()
            time.sleep(1e-9)
        self.destroy()
        return self.opened

class Saver(DialogFileWindow):
    def __init__(self, master,path,last,authorised:list[tuple],alias:dict={},prename:str=''):
        """Enregistrer un fichier"""
        super().__init__(master,path,last,[],alias,{'Open':lambda:None,'Browse':lambda :self.openfolder(self.chose)})
        self.title("Enregistrer sous")
        icon = ImageTk.PhotoImage(file=r"H\Apps\explorateur\disquette.png")
        self.iconphoto(False,icon)
        self.saved=None

        #nom du fichier
        self.entry=self.add_inf2(lambda master:Entry(master))
        self.entry.insert(0,prename)
        self.entry.pack(side=LEFT)
        self.entry.bind("<Return>",self.save)

        #type
        self.combo = self.add_inf2(lambda master :ttk.Combobox(master,values=tuple(k[0]+' '+k[1] for k in authorised),state='readonly'))
        self.combo.pack(side=RIGHT)
        self.combo.set(authorised[0][0]+' '+authorised[0][1])
        self.combo.bind('<<ComboboxSelected>>',self.actualise)

        self.savebtn = self.add_inf2(lambda master:Button(master,text='Enregistrer',command=self.save))
        self.savebtn.pack()

        self.btn['text']='Browse'
        self.geometry('600x250')

        self.openfolder('')
    
    def save(self,*args):
        #enregistrer
        if self.entry.get()=='':
            self.bell()
            return
        name = self.entry.get()
        if os.path.splitext(name)[1]=='':#si on n'a pas mis d'extension -> la rajouter
            if self.combo.get().split(' ')[1].count(' ')==0:
                name+=self.combo.get().split(' ')[1]
            else:
                name+=self.combo.get().split(' ')[1].split(' ')[1]
        if os.path.exists(self.CWD+name) and not messagebox.askyesno('File already exists',f"Attention, le fichier existe déjà. Voulez-vous le supprimer ?"):
            return
        self.saved = self.CWD+name
    
    def run(self):
        """Boucle: attendre une sauvegarde"""
        while self.saved==None:
            try:
                self.update()
                time.sleep(1e-9)
            except:
                break
        self.destroy()
        return self.saved

class BackgroundsOpener(DialogFileWindow):
    def __init__(self, master,background):
        """Choisir un fond d'ecran"""
        self.bg=background
        super().__init__(master, 'H\Wallpapers', 'H\Wallpapers', [('Images JPEG','.jpg')], {'H\Wallpapers':''}, {'Open':lambda:self.open,'Browse':lambda :None})

        self.txt.destroy()
        self.can=self.add_inf2(lambda master: Canvas(master,height=225,width=600,highlightthickness=0))
        self.can.pack(side=TOP)

        self.btn.destroy()

        self.btn = self.add_inf2(lambda master: Button(master,text='',command=self.open))
        self.btn.pack(side=LEFT)

        self.title("Selectionner un fond d'écran")

        self.page =PhotoImage(file =r'H\Apps\explorateur\photo.png')

        self.opened=None

        self.combo = self.add_inf2(lambda master :ttk.Combobox(master,values=tuple(k[0]+' '+k[1] for k in [('Images JPEG','.jpg')]),state='readonly'))
        self.combo.pack(side=RIGHT)
        self.combo.set('Images JPEG .jpg')

        self.btn['text']='Open'
        self.set_authorised('.jpg')

        self.openfolder('',False)
        self.tree.heading("#0",text='')
        
    
    def open(self):
        self.opened = self.CWD+self.chose
        self.bg.change(self.opened)
        self.destroy()
    
    def on_select(self, event):
        self.can.delete('ALL')
        self.chose =self.tree.item(self.tree.focus())['text']
        if self.chose=='':return
        self.image=image = ImageTk.PhotoImage(resize.cached_resize(self.can.winfo_width(),0,r'H\Wallpapers\\'+self.chose))
        self.can.create_image(self.can.winfo_width()/2,self.can.winfo_height()/2,image=image,anchor='center')

def openfile(master,types:list[tuple],first:str):
    """Routine : ouvrir un fichier"""
    return Opener(master,first,first,types,{first:""}).run()

def savefile(master,types:list[tuple],first:str): 
    """Routine : sauvegarder un fichier"""
    return Saver(master,first,first,types,{first:""}).run()


if __name__=='__main__':
    root=Tk()
    print(openfile(root,[('TEXT','.txt'),('Python','.py')],r"H\Users\admin"))