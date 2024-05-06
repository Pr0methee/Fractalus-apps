from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
import socket,time,shutil,os
from PersonalWidgets import PopingToplevel

def print_dict(d:dict):
    """Renvoie un str contenant le contenu d'un dictionnaire"""
    r=''
    for x in d:
        r+=str(x)+' : '+str(d[x])+'\n'
    return r[:-1]

class CMD(PopingToplevel):
    COMMANDS_DESC ={#description des commandes
    'ayudame':"Renvoie la liste des commandes valides avec une description",
    'borar':'Efface la console',
    'cc':"Se décaler au répertoire ...",
    'cc..':'Aller au répertoire précédent',
    'creardir':"Créer le répertoire",
    'damecam':"Renvoie le chemin",
    'eliminar':'Retire un fichier/dossier ',
    'enum':'Renvoie la liste des fichiers du dossier',
    'fecha':"Renvoie la date du jour",
    'hora':"Renvoie l'heure du système",
    "ipconfig":"Renvoie l'adresse IP du poste",
    "mover":"Déplace un fichier/dossier vers un autre emplacement",
    "renom":"Renomme un fichier/dossier",
    "vacio":"Crée un fichier vide d'un certain type"
    }
    NAME = "Fractus System [version 1.0]"
    CREDITS =chr(169)+" Valentin Novo. Tous droits réservés.\n\nEntrez {ayudame} pour plus d'informations.\n"

    def __init__(self,master,LAST:str='H\\',CWD:str='H\\'):
        super().__init__(master)
        self.VALID_COMMANDS ={#nom des commandes : fct à appeler
        'ayudame':lambda:"Liste des commandes valides : \n"+print_dict(self.COMMANDS_DESC),
        'cc':lambda arg:self.cc(arg),
        'cc..':lambda: self.prec_dir(),
        'creardir':lambda arg:self.crear_directory(arg),
        'damecam':lambda:self.CWD,
        'eliminar':lambda arg:self.eliminar(arg),
        'enum':lambda:self.enum(),
        'fecha':lambda:time.asctime(),
        'hora':lambda:str(time.time()),
        'ipconfig':lambda:socket.gethostbyname(socket.gethostname()),
        'mover':lambda a,n:self.mover(a,n),
        'renom':lambda f,n:self.renombrar(f,n),
        'vacio':lambda typ:self.vacio(typ)
        }
        self.CWD = CWD 
        self.LAST = LAST
        self.I=0#revoir les commandes précédentes
        self.COMMANDS_USED =[]

        self.transient(master)
        self.title("Invité de commande")
        self.geometry("700x500")
        self['bg']='black'
        self.protocol("WM_DELETE_WINDOW",self.eol)

        #affichage des commandes et de leurs effets
        self.txt = ScrolledText(self,bg='black',fg='#00ff00',font=Font(family="Arial",size=12),bd=0)
        self.txt.pack(expand=True,fill=BOTH)
        self.txt.configure(state='disabled')

        #champ de saisie des commandes
        Label(self,text=">>>",bg='black',fg="#00ff00").pack(side=LEFT)
        self.en=Entry(self,width=680,bg='black',fg="#00ff00",insertbackground="#00ff00")
        self.en.pack(side=RIGHT)
        self.en.bind("<Return>",self.execute)
        self.en.bind("<Up>",self.up)
        self.en.bind("<Down>",self.down)
        self.en.bind("<FocusIn>",self.re)

        self.cleanning()
    
    def cleanning(self):
        """Tout effacer"""
        self.txt.configure(state='normal')
        self.txt.delete(0.0,END)
        self.insert_text(CMD.NAME)
        self.insert_text(CMD.CREDITS)
        self.txt.configure(state='disabled')

    def re(self,*args):
        """On revient sur le champ de saisie"""
        self.I=0

    def up(self,*args):
        """commande précédente"""
        self.I+=1
        if self.I> len(self.COMMANDS_USED):
            self.I-=1
            return
        
        if len(self.COMMANDS_USED)!=0:
            self.en.delete(0,END)
            self.en.insert(0,self.COMMANDS_USED[-self.I])

    def down(self,*args):
        """Commande suivante"""
        self.I-=1
        if self.I<=0:
            self.I=0
            self.en.delete(0,END)
            self.en.insert(0,'')
            return 
        if len(self.COMMANDS_USED)!=0:
            self.en.delete(0,END)
            self.en.insert(0,self.COMMANDS_USED[-self.I])


    def insert_text(self,text):
        """Rajouter qqch dans le widget text"""
        self.txt.configure(state='normal')
        self.txt.insert(END,str(text)+'\n')
        self.txt.configure(state='disabled')
    
    def execute(self,*args):
        """Execute la commande entrée"""
        self.COMMANDS_USED.append(self.en.get())
        command=self.en.get().split(' ')[0]
        if command=='borar':
            self.cleanning()
        else:
            self.insert_text('>>> '+self.en.get())
            try:
                self.insert_text(self.VALID_COMMANDS.get(command,lambda *args:"Error, Invalid Command")(*self.en.get().split(' ')[1:])+'\n')
            except TypeError as err:
                self.insert_text("Error, Invalid Syntax")
        self.en.delete(0,END)
        self.txt.yview_moveto('1.0')
    
    def eol(self):
        self.destroy()
    
    #Commandes du cmd
    def cc(self,dir):
        """Change de répertoire"""
        if not os.path.exists(self.CWD+'\\'+dir) or type(dir)!=str:
            return f"Erreur, impossible de se placer dans le répertoire {dir}."
        self.CWD += '\\'+dir
        return ''

    def prec_dir(self):
        """Se décaller au répertoire précédent"""
        if self.CWD == self.LAST:
            return "Erreur, impossible de revenir au répertoire précédent."
        self.CWD = '\\'.join(self.CWD.split('\\')[:-1])
        return ''

    def crear_directory(self,dir):
        """Créer le répertoire"""
        if os.path.exists(self.CWD+'\\'+dir) or type(dir)!=str:
            return "Erreur, impossible de créer ce répertoire"
        try:
            os.mkdir(self.CWD+'\\'+dir)
            return 'Répertoire créé avec succès'
        except:
            return "Erreur, impossible de créer ce répertoire"

    def eliminar(self,d):
        """Retire le fichier/dossier {d}"""
        if os.path.exists(d):
            try:
                os.remove(d)
            except:
                os.rmdir(d)
        elif os.path.exists(self.CWD+'\\'+d):
            try:
                os.remove(self.CWD+'\\'+d)
            except:
                os.rmdir(self.CWD+'\\'+d)
        else:
            return f"Erreur, le fichier {d} n'existe pas"
        return d+" supprimé avec succès"

    def enum(self):
        """Liste le contenu du répertoire actuel"""
        if os.listdir(self.CWD)!=[]:
            return 'Contenu de :'+self.CWD+'\n-'+'\n-'.join(os.listdir(self.CWD))
        return self.CWD+' est vide.'

    def mover(self,act,new):
        """Déplacer un fichier/dossier ailleurs"""
        try:
            shutil.move(self.CWD+'\\'+act,self.CWD+'\\'+new)
        except FileNotFoundError as err:
            return f"Erreur, imossible de déplacer {act}, il n'existe pas"
        except shutil.Error as err:
            return "Erreur, opération impossible"

        return ''

    def renombrar(self,file,new):
        """Renommer un fichier/dossier"""
        if os.path.exists(self.CWD+'\\'+file):
            os.rename(self.CWD+'\\'+file,self.CWD+'\\'+new)
            return "Renommé avec succès"
        return f'Impossible de renommer, {file} n\'existe pas' 

    def vacio(self,typ):
        """Créer un fichier vide de type {typ}"""
        i =0
        while os.path.exists(self.CWD+'\\NouveauDocument'+str(i)+'.'+typ):
            i+=1
        try:
            with open(self.CWD+'\\NouveauDocument'+str(i)+'.'+typ,'w') as f:
                f.write('')
            with open(self.CWD+'\\NouveauDocument'+str(i)+'.'+typ,'r') as f:
                f.read()
            return ''
        except:
            return f"Erreur, Impossible de créer un fichier vide de format .{typ}"

if __name__=='__main__':
    fen=Tk()
    CMD(fen)
    fen.mainloop()