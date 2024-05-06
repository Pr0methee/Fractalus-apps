# coding: utf-8

"""
Projet d'éditeur de texte/code
11/11/2022-Valentin Novo

Cet éditeur est censé pouvoir ouvrir et écrire dans des fichiers, (cf. constante FILES pour savoir lesquels sont ouvrables)

https://stackabuse.com/reading-and-writing-ms-word-files-in-python-via-python-docx-module/
https://www.geeksforgeeks.org/reading-excel-file-using-python/
https://jaetheme.com/balises-html5/
"""
import H.Apps.word.instaler#Crée le dossier cache si necessaire

from tkinter import * 
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
import tkinter.colorchooser as colorchooser
import os,io,time
from contextlib import redirect_stdout
from H.Apps.word.executors import ask_csv,ShowCSV,LatexExecutor
import H.Apps.word.Text_edit as Text_edit, H.Apps.word.insertion as insertion, H.Apps.word.mef_window as mef_window#af
import H.Apps.word.apply as apply
from PersonalWidgets import PopingToplevel
import tkinter.filedialog as filedialog

def initialize(session):
    with open('H/cache/word/Built-In Python.txt',"w") as f:
        f.write(session.pref[2])
    with open('H/cache/word/Erreurs Python.txt',"w") as f:
        f.write(session.pref[5])
    with open('H/cache/word/Fonctions Python.txt',"w") as f:
        f.write(session.pref[6])
    with open('H/cache/word/Math Mode 2 LaTeX.txt',"w") as f:
        f.write(session.pref[7])
    with open('H/cache/word/Math Mode LaTeX.txt',"w") as f:
        f.write(session.pref[8])
    with open('H/cache/word/Modules Python.txt',"w") as f:
        f.write(session.pref[9])
    with open('H/cache/word/Mots-Clés Python.txt',"w") as f:
        f.write(session.pref[11])
    with open('H/cache/word/Mots-Clés LaTeX.txt',"w") as f:
        f.write(session.pref[10])
    with open('H/cache/word/Mots-Clés SQL.txt',"w") as f:
        f.write(session.pref[12])
    with open('H/cache/word/String Python.txt',"w") as f:
        f.write(session.pref[13])
    with open('H/cache/word/Commentaires Python.txt',"w") as f:
        f.write(session.pref[4])
    with open('H/cache/word/Commentaires LaTeX.txt',"w") as f:
        f.write(session.pref[3])

def save_pref():
    d={}
    with open('H/cache/word/Built-In Python.txt',"r") as f:
        d['builtinpy']=f.read()
    with open('H/cache/word/Erreurs Python.txt',"r") as f:
        d['errpy']=f.read()
    with open('H/cache/word/Fonctions Python.txt',"r") as f:
        d['fctpy']=f.read()
    with open('H/cache/word/Math Mode 2 LaTeX.txt',"r") as f:
        d['mm2latex']=f.read()
    with open('H/cache/word/Math Mode LaTeX.txt',"r") as f:
        d['mmlatex']=f.read()
    with open('H/cache/word/Modules Python.txt',"r") as f:
        d['modpy']=f.read()
    with open('H/cache/word/Mots-Clés Python.txt',"r") as f:
        d['mcpy']=f.read()
    with open('H/cache/word/Mots-Clés LaTeX.txt',"r") as f:
        d['mclatex']=f.read()
    with open('H/cache/word/Mots-Clés SQL.txt',"r") as f:
        d['mcsql']=f.read()
    with open('H/cache/word/String Python.txt',"r") as f:
        d['strpy']=f.read()
    with open('H/cache/word/Commentaires Python.txt',"r") as f:
        d['compy']=f.read()
    with open('H/cache/word/Commentaires LaTeX.txt',"r") as f:
        d['comlatex']=f.read()
    return d


FILES = [
    ("All",'.txt .py .pyw .csv .html .css .js .php .sql .tex .sty .aux .log .thm'),
    ("Text files",'.txt'),#
    ("CSV",".csv"),#
    ("Python files",'.py .pyw'),#
    ("HTML files",".html"),#
    ("CSS",".css"),
    ("Javascript",'.js'),
    ("PHP",'.php'),
    ("SQL",'.sql'),
    ("LaTeX",'.tex .sty'),#
    ("LaTeX output",'.aux .log .thm')
    ]


class App(Text_edit.TextEdit):
    def __init__(self,master,link:str='',ask=[
        lambda files,master:filedialog.askopenfilename(filetypes=files,parent=master),
        lambda files,master:filedialog.asksaveasfile(filetypes=files,defaultextension='.txt',parent=master)
        ]):

        """
        Classe de l'application.
        """
        
        #Définition générale
        super().__init__(master,"Text/Code Editor",FILES,ask)
        self.transient(master)

        if link != '':
            self.current=link
            self.open_file()


        #self.actual_ex:PythonExecutor = None
        self.applier = apply.Applier(self.txt)#appliquer les styles

        #Bandeau actions
        #Action fichier
        self.fichiers = self.add_menubutton("Fichiers")
        self.fichiers.pack(side=LEFT)

        self.fichier_menu = Menu(self.fichiers)
        for desc in [("Ouvrir",self.askopen,'Ctrl+o'),("Enregistrer",self.save,'Ctrl+s'),("Enregistrer Sous",self.saveas,''),("Nouveau",self.new_file,'Ctrl+n'),("Exécuter",self.run_file,'Ctrl+F5')]:
            self.fichier_menu.add_command(label = desc[0],command=desc[1],accelerator=desc[2])#ajoute toutes les options. accelerator permet de notifier à l'utilisateur un racourci

        self.fichier_menu.add_separator()
        self.fichier_menu.add_command(label="Quitter",command=self.destroy)

        self.fichiers.configure(menu=self.fichier_menu)

        #Action Editer 
        self.edit = self.add_menubutton("Editer")
        self.edit.pack(side=LEFT)

        self.edit_menu = Menu(self.edit)
        for each1 in [[("Défaire",self.undo,'Ctrl+Z'),("Refaire",self.redo,'Ctrl+Y')],[("Chercher",self.search,'Ctrl+F'),("Remplacer",self.replace,'Ctrl+H')]]:
            for each2 in each1:
                self.edit_menu.add_command(label=each2[0],command=each2[1],accelerator=each2[2])
            self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Atteindre la définition",command=self.reach,accelerator='Ctrl+R')

        self.edit.configure(menu=self.edit_menu)

        #Action insérer
        self.insert = self.add_menubutton('Insérer')
        self.insert.pack(side=LEFT)

        self.insertmenu = Menu(self.insert)
        self.insertmenu.add_command(label = "Caractère",command=lambda : insertion.insret_proc(self,self.txt),accelerator="Ctrl+i")
        self.mathmenu=Menu(self.insertmenu)
        self.mathmenu.add_command(label='Equations',command=lambda : insertion.equa_proc(self,self.txt),accelerator="Ctrl+=")#insérer une equation, math en ligne
        self.mathmenu.add_command(label='Fonctions',command=lambda : insertion.func_proc(self,self.txt),accelerator="Alt+=")#insérer une fonction
        self.insertmenu.add_cascade(label="Maths",menu=self.mathmenu)
        self.insert.configure(menu=self.insertmenu)

        #Action mise en forme
        self.mef = self.add_menubutton("Mise en Forme")
        self.mef.pack(side=LEFT)

        self.mefmenu = Menu(self.mef)
        
        #modifier la couleur d'arrière plan
        self.meffondmenu = Menu(self.mefmenu)
        self.th = IntVar()
        self.meffondmenu.add_radiobutton(label="Thème clair-Par défaut",variable=self.th,value=0,command=self.changebg)
        self.meffondmenu.add_radiobutton(label="Thème sombre-Par défaut",variable=self.th,value=1,command=self.changebg)
        self.meffondmenu.add_radiobutton(label="Théme personalisé",variable=self.th,value=2,command=self.changebg)
        self.mefmenu.add_cascade(label ='Fond',menu=self.meffondmenu)

        #...celle d'avant plan
        self.meffgmenu = Menu(self.mefmenu)
        self.fg =IntVar()
        self.meffgmenu.add_radiobutton(label="Noir",variable=self.fg,value=0,command=self.changefg)
        self.meffgmenu.add_radiobutton(label="Blanc",variable=self.fg,value=1,command=self.changefg)
        self.meffgmenu.add_radiobutton(label="Couleur personalisée",variable=self.fg,value=2,command=self.changefg)
        self.mefmenu.add_cascade(label ='Curseur',menu=self.meffgmenu)

        #modifier les couleurs polices... des styles par défaut
        self.mefmenu.add_command(label="Styles par défaut",command=lambda : mef_window.MEFWindow(self,self.applier.styles))
        self.mef.configure(menu=self.mefmenu)

        self.run()
         
    def changebg(self):
        """Change la couleur d'arrière plan de l'app."""
        if self.th.get()==0:#si le fond est blanc alors les écritures doivent être noire
            self.txt['bg']='SystemWindow'
            self.change_bg('SystemButtonFace')
            self.change_fg('SystemWindowText')
            self.txt.configure(foreground='black',insertbackground='black')
            self.fg.set(0)
        elif self.th.get()==1:#et inversement
            self.txt['bg']='#2d2d2d'
            self.txt.configure(foreground='white',insertbackground='white')
            self.change_bg('#2d2d2d')
            self.change_fg('white')
            self.fg.set(1)
        else:#si on choisit de mettre une couleur personalisée
            color = colorchooser.askcolor(parent=self)
            if color == (None,None):#si l'utilisateur n'a rien choisit on remet tout comme au départ
                if self.txt['bg'] == 'SystemWindow':
                    self.th.set(0)
                elif self.txt['bg'] == '#2d2d2d':
                    self.th.set(1)
            else:
                self.txt['bg']=color[1]
                self.change_bg(color[1])
    
    def changefg(self):
        """change la couleur d'avant plan de l'app"""
        #3 possibilités : noir,blanc ou couleur personalisée
        if self.fg.get()==0:
            self.change_fg('SystemWindowText')
            self.txt.configure(foreground='black',insertbackground='black')
        elif self.fg.get()==1:
            self.txt.configure(foreground='white',insertbackground='white')
            self.change_fg('white')
        else:
            color = colorchooser.askcolor(parent=self)
            if color == (None,None):#si l'utilisateur n'a rien choisit...
                if self.txt['fg'] == 'black':
                    self.fg.set(0)
                elif self.txt['fg'] == 'white':
                    self.fg.set(1)
            else:
                self.txt.configure(foreground=color[1],insertbackground=color[1],)
                self.change_fg(color[1])

    def run(self):
        """Boucle principale"""
        #gestion des touches
        self.bind('<Control-r>',self.reach)#atteindre la définition
        self.bind('<Control-F5>',self.run_file)#executer le fichier
        self.bind('<Control-i>',lambda arg: insertion.insret_proc(self,self.txt))#insertion
        self.bind('<Alt =>',lambda arg: insertion.func_proc(self,self.txt))#fonctions maths
        self.bind('<Control =>',lambda arg: insertion.equa_proc(self,self.txt))#équation

        self.apply()#lancer l'application des styles

        super().run()

    def apply(self):
        """applique les styles sur tout le document"""
        self.applier.update(self.current)
        self.after(250,self.apply)#on recommence

    def reach(self,*args):
        """Atteindre la définition"""
        if self.selected:
            try:
                f = io.StringIO()
                with redirect_stdout(f):
                    exec(f"help({self.selected_text()})")
                s=f.getvalue()
                
                self.disable_all()
                HelpWindow(self,self.selected_text(),s)
                
                self.able_all()
            except (SyntaxError,NameError):
                self.disable_all()
                HelpWindow(self,self.selected_text(),"Erreur, Impossible d'obtenir de l'aide sur la selection.")
                self.able_all()
    
    def run_file(self,*args):
        """Executer un fichier"""
        if messagebox.askyesno("Run","Voulez-vous executer le fichier ?",parent=self):
            self.save()#les fichiers doivent être enregistrés pour être executés

            if os.path.splitext(self.current)[1] in ('.tex',):#execution latex= générer PDF
                exe = ExecWindow(self,"Génération du pdf... Si certaines extensions ne sont pas présentes sur votre ordinateur, des boites de dialogues peuvent s'ouvrir.")
                LatexExecutor(os.path.splitext(self.current)[0],self,exe.end)#generation+affichage
            
            elif os.path.splitext(self.current)[1] in ('.csv',):
                rep = ask_csv(self)
                if rep !=None:
                    ShowCSV(self,self.current,rep[0],rep[1])
               
            else:#Si le fichier n'est pas dans un type executable -> erreur
                messagebox.showwarning("RunError","Le fichier que vous tentez d'executer n'est pas executable.",parent=self)

class WaitUntil:
    def __init__(self,var,val) -> None:
        self.var=var
        self.val=val
    
    def wait(self):
        while self.var != self.val:
            time.sleep(1e-10)
            print('waitting')


class HelpWindow(PopingToplevel):
    def __init__(self,parent, expr,result):
        """Petite fenêtre qui affiche l'aide sur une commande (ne marche qu'en python)"""
        super().__init__(parent)
        self.transient(parent)
        self.title(f"Résultat de : help({expr})")
        self.text=scrolledtext.ScrolledText(self)
        self.text.pack()
        self.text.insert('0.0',result)
        self.resizable(0,0)
        self.text.configure(state='disabled')     

class ExecWindow(Toplevel):
    def __init__(self, master:Tk,text:str):
        """Petite fenêtre qui affiche un message sur l'execution python ou latex"""
        super().__init__(master)
        self.wm_attributes('-topmost',1)
        lab = Label(self,text=text)
        lab.pack()
        self.protocol("WM_DELETE_WINDOW",lambda:None)#vérouille la croix de fermeture
        self.update()
    
    def end(self):
        """End Of Life"""
        self.destroy()

if __name__ == '__main__':
    #boucle principale de test
    tk=Tk()
    app=App(tk)
    app.run()