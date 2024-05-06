from __future__ import annotations

import threading,subprocess,sys
from tkinter import *
import H.Apps.word.form as form,H.Apps.word.resize as resize
import tkinter.ttk as ttk
import csv,os,shutil, pdf2image

def ask_csv(master):
    """formulaire de demande des infos concernant la structure du csv (présence d'en-tête ou non + délimiteur)"""
    f=form.Formulaire(master,"Remplissez les informations suivantes :")
    f.add_champ("Délimiteur : ",lambda master : Entry(master),lambda p:True,'',pre=';')
    f.add_champ("Présence d'en-tête ? ",lambda master: form.RadioChooser(master,[('Oui',1),('Non',0)],0),lambda p:True,'')
    f.add_submit()
    return f.run()

class ShowCSV(Toplevel):
    def __init__(self, master,csvfile:str, delimiter:str, first=True):
        """Fenetre d'affichage d'un CSV"""
        super().__init__(master)
        self.transient(master)

        self.title(csvfile)

        with open(csvfile,'r') as f:
            csvreader = csv.reader(f,delimiter=delimiter)
            print(csvreader)
            i=0
            for row in csvreader:
                if i==0:
                    if first :
                        self.tree = ttk.Treeview(self,columns=tuple(row),show='headings')
                        for col in row:
                            self.tree.heading(col, text=col.capitalize())
                    else:
                        self.tree = ttk.Treeview(self,columns=tuple([None for i in range(len(row))]),show='')
                    self.tree.pack(expand=True,fill=BOTH)

                if (i==0 and not first) or i!=0:
                    self.tree.insert('',END,values=row)
                i+=1
        
class LatexExecutor(threading.Thread):
    def __init__(self,name:str,parent:Tk,callback:function) -> None:
        """Génère un pdf d'un fichier .tex"""
        
        super().__init__()

        os.system("pdflatex -interaction nonstopmode "+name+'.tex')

        for ext in ['.aux','.log','.pdf','.thm']:
            shutil.move(name.split('\\')[-1]+ext,os.getcwd()+'\\'+name+ext)

        pages = pdf2image.convert_from_path(name+'.pdf')
        try:
            os.mkdir('H\\cache\\bin')
        except:
            pass

        for i in range(len(pages)):#crée dans le fichier bin une image de chaque page du pdf pour les afficher dans un Canvas
            pages[i].save(r'H\cache\bin\page'+ str(i) +'.png', 'PNG')
            resize.resize(750,1,r'H\cache\bin\page'+ str(i) +'.png',r'H\cache\bin\page'+ str(i) +'.png')

        callback()                    
        RapportWindowTex(parent,len(pages))

class RapportWindowTex(Toplevel):
    def __init__(self,parent:Tk,l:int):
        """Affiche le pdf"""
        super().__init__(parent)
        self.transient(parent)

        self.title("Rapport d'exécution-LaTeX")

        self.can=Canvas(self)
        self.can.pack(side=LEFT)        
        self.can['height']=750
        self.can['width']=530

        self.img=[PhotoImage(file=fr"H\cache\bin\page{i}.png",master=self) for i in range(l)]
        for i in range(l):
            self.can.create_image(530//2,750//2+765*i,image=self.img[i])

        self.scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.can.yview)
        self.can.configure(yscrollcommand=self.scrollbar.set)
        self.can.config(scrollregion=self.can.bbox("all"))
        self.scrollbar.pack(expand=True,fill='y',side='right')

        self.resizable(0,0)
        shutil.rmtree('H\cache\\bin')
        self.update()
        self.update_idletasks()
