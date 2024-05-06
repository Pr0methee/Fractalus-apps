from __future__ import annotations

from tkinter import *
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.scrolledtext as scrolledtext
from tktooltip import ToolTip
import H.Apps.word.form as form
from PersonalWidgets import PopingToplevel

class TextEdit(PopingToplevel):
    def __init__(self,master,title : str|None, files:list[tuple[str]]=[],ask=[
        lambda files,master:filedialog.askopenfilename(filetypes=files,parent=master),
        lambda files,master:filedialog.asksaveasfile(filetypes=files,defaultextension='.txt',parent=master)
        ]) -> None:
        """Classe de base pour les éditeurs de texte"""
        
        super().__init__(master)

        Grid.columnconfigure(self,0,weight=1)        
        Grid.rowconfigure(self,1,weight=1)

        if title == None:
            self.title("Text Editor")
        else:
            self.title(title)

        self.current = ''#fichier ouvert
        self.selected = False

        self.FILES = files
        self.asking_proc=ask#quelles fonction doit-on appeler pour demander l'ouverture/enregistrement

        #Création des frames
        self.top_frame = Frame(self)
        self.top_frame.grid(row=0,column=0,sticky=NSEW)#bandeau action

        self.bottom_frame = Frame(self)
        self.bottom_frame.grid(row=1,column=0,sticky = NSEW)#bandeau text

        #zone de texte
        self.txt = scrolledtext.ScrolledText(self.bottom_frame,undo=True)
        self.txt.pack(fill=BOTH,expand=True)
    
    def add_menubutton(self,label:str)-> Menubutton:
        return Menubutton(self.top_frame,text=label)
    
    def add_button(self,label:str, command:function) -> Button:
        return Button(self.top_frame,text=label,command=command)
    
    def disable_all(self) -> None:
        """Met state =disabled à tous les enfants/petits-enfants de self"""
        for child in self.children.values():
            if type(child)==Frame:
                disable_frame(child)
            elif type(child) in (Text, Menubutton):
                child.configure(state="disabled")

    def able_all(self) -> None:
        """Met state =normal à tous les enfants/petits-enfants de self"""
        for child in self.children.values():
            if type(child)==Frame:
                able_frame(child)
            elif type(child) in (Text, Menubutton):
                child.configure(state="normal")

    def truesearch(self,pattern:str)-> list:
        """Montre toutes les occurence de pattern"""
        r='0.0'
        l=[]
        while self.txt.index('end') != r:
            r = self.txt.search(pattern,r,'end')
            if r == '':break
            l.append(r)
            r+='+1c'

        return l
    
    def search(self,*args) -> None:
        """Lance la recherche"""
        self.end_all()

        if not self.selected:
            f=form.Formulaire(self,"Recherche")
            f.add_champ("Texte à rechercher",lambda master:Entry(master),lambda p:p!='','Veuillez saisir quelque chose')
            f.add_submit()
            result = f.run()
        else:
            result=[self.selected_text()]

        if result == False:pass
        
        else:
            indexes =self.truesearch(result[0])
            if indexes != []:
                self.indexes = indexes
                self.i =0
                self.l = len(result[0])

                self.btn =Button(self.top_frame,text='X',fg='red',bg='white',relief=SUNKEN,command=self.end_search)
                self.btn.pack(side=RIGHT)

                #bal = 
                b=ToolTip(self.btn,msg="Masquer le résultat de la recherche",delay=0)
                b.wm_attributes('-topmost',1)
                #bal.bind_widget(self.btn,msg="Masquer le résultat de la recherche")

                self.btn_next =Button(self.top_frame,text='v',fg='black',bg='white',relief=SUNKEN,command=self.next_occ)
                self.btn_next.pack(side=RIGHT)

                #baln = 
                b2=ToolTip(self.btn_next,msg="Occurence suivante",delay=0)
                b2.wm_attributes('-topmost',1)
                #baln.bind_widget(self.btn_next,msg="Occurence suivante")

                self.btn_prec =Button(self.top_frame,text='^',fg='black',bg='white',relief=SUNKEN,command=self.prec_occ)
                self.btn_prec.pack(side=RIGHT)

                #balp = 
                b3=ToolTip(self.btn_prec,msg="Occurence précédente",delay=0)
                b3.wm_attributes('-topmost',1)
                #balp.bind_widget(self.btn_prec,msg="Occurence précédente")

                for i in indexes:
                    self.txt.tag_add("research",i,i+f'+{len(result[0])}c')

                self.txt.tag_configure("research",foreground='white',background='black')

                self.txt.tag_add('act',indexes[self.i],indexes[self.i]+f'+{self.l}c')
                self.txt.tag_configure('act',background='yellow',foreground='black')

                messagebox.showinfo("Résultat de recherche",f"L'élément '{result[0]}' a été trouvé {len(indexes)} fois dans le document",parent=self)
            else:
                messagebox.showinfo("Résultat de recherche",f"L'élément '{result[0]}' n'a pas été trouvé dans le document",parent=self)

    def end_search(self) -> None:
        """Mettre fin à la recherche"""
        self.btn.destroy()
        self.btn_prec.destroy()
        self.btn_next.destroy()
        self.txt.tag_delete("research")
        self.txt.tag_delete('act')

    def replace(self,*args):
        """Lance le remplacement"""
        self.end_all()

        if self.selected:
            pattern = self.selected_text()
        else:
            f = form.Formulaire("Remplacer")
            f.add_champ("Texte à remplacer",lambda master:Entry(master),lambda p:p!='',"Veuillez saisir quelque chose")
            f.add_submit()
            pattern=f.run()
        
        if pattern != False:
            if type(pattern) == list:pattern = pattern[0]

            indexes=self.truesearch(pattern)
            if indexes == []:
                messagebox.showerror("Remplacer",f"Impossible de remplacer l'expression '{pattern}', car elle n'a pas été trouvée dans le document.",parent=self)
            else:
                #mettre en évidence les termes à remplacer
                for i in indexes:
                    self.txt.tag_add("replace",i,i+f'+{len(pattern)}c')

                self.txt.tag_configure("replace",foreground='white',background='navy')

                #demander ce par quoi remplacer
                f = form.Formulaire(self,None)
                f.add_champ("Remplacer par :",lambda master:Entry(master),lambda p:True,'')
                f.add_submit()
                replace = f.run()

                if replace != False:
                    replace = replace[0]

                    if messagebox.askyesno("Remplacer tout",f"Voulez vous remplacer toutes les occurences de '{pattern}' par '{replace}' ?",parent=self):
                        text = self.txt.get('0.0','end')
                        text = text.replace(pattern,replace)
                        self.txt.delete('0.0','end')
                        self.txt.insert('0.0',text)
                    else:
                        self.indexes = indexes
                        self.i=0
                        self.l=len(pattern)
                        self.rep = replace
                        self.pattern = pattern

                        self.btn_end_rep =Button(self.top_frame,text='X',fg='red',bg='white',relief=SUNKEN,command=self.end_replace)
                        self.btn_end_rep.pack(side=RIGHT)

                        #b = ToolTip(self.btn_end_rep,msg="Masquer le résultat de la recherche de remplacement",delay=0)
                        #b.wm_attributes('-topmost',1)

                        self.btn_next =Button(self.top_frame,text='v',fg='black',bg='white',relief=SUNKEN,command=self.next_occ)
                        self.btn_next.pack(side=RIGHT)

                        #b2 = ToolTip(self.btn_next,msg="Occurence suivante",delay=0)
                        #b2.wm_attributes('-topmost',1)

                        self.btn_prec =Button(self.top_frame,text='^',fg='black',bg='white',relief=SUNKEN,command=self.prec_occ)
                        self.btn_prec.pack(side=RIGHT)

                        #b3 = ToolTip(self.btn_prec,msg="Occurence précédente",delay=0)
                        #b3.wm_attributes('-topmost',1)

                        self.btn_ok =Button(self.top_frame,text='✓',fg='black',bg='white',relief=SUNKEN,command=self.rep_occ)
                        self.btn_ok.pack(side=RIGHT)

                        b4 = ToolTip(self.btn_ok,msg="Remplacer cette occurence",delay=0)
                        b4.wm_attributes('-topmost',1)

                        self.txt.tag_add('act',indexes[self.i],indexes[self.i]+f'+{self.l}c')
                        self.txt.tag_configure('act',background='yellow',foreground='black')

    def next_occ(self):
        """Voir l'occurence suivante du pattern considéré"""
        self.i+=1
        if self.i >= len(self.indexes):
            self.i=0

        self.txt.tag_delete('act')
        self.txt.tag_add('act',self.indexes[self.i],self.indexes[self.i]+f'+{self.l}c')
        self.txt.tag_configure('act',background='yellow',foreground='black')

        y = int(self.indexes[self.i].split('.')[0])
        yend = int(self.txt.index('end').split('.')[0])
        self.txt.yview_moveto(y/yend-0.1)

    def prec_occ(self):
        """Voir l'occurence précédente du pattern considéré"""
        self.i-=1
        if self.i < 0:
            self.i=len(self.indexes)-1
        
        self.txt.tag_delete('act')
        self.txt.tag_add('act',self.indexes[self.i],self.indexes[self.i]+f'+{self.l}c')
        self.txt.tag_configure('act',background='yellow',foreground='black')
        
        y = int(self.indexes[self.i].split('.')[0])
        yend = int(self.txt.index('end').split('.')[0])
        self.txt.yview_moveto(y/yend-0.1)

    def rep_occ(self):
        """Remplacer l'occurence actuelle du pattern considéré"""
        self.txt.replace(self.indexes[self.i],self.indexes[self.i]+f'+{self.l}c',self.rep)

        self.indexes = self.truesearch(self.pattern)
        
        if self.indexes == []:
            messagebox.showinfo("Remplacement terminé","Toutes les occurences ont été remplacées.",parent=self)
            self.end_replace()
        else:
            if self.i>= len(self.indexes):
                self.i=0

            self.txt.tag_delete('act')
            self.txt.tag_add('act',self.indexes[self.i],self.indexes[self.i]+f'+{self.l}c')
            self.txt.tag_configure('act',background='yellow',foreground='black')

    def end_replace(self):
        """Arrêter la routine de remplacement"""
        self.btn_end_rep.destroy()
        self.btn_prec.destroy()
        self.btn_next.destroy()
        self.btn_ok.destroy()
        self.txt.tag_delete("replace")
        self.txt.tag_delete('act')

    def end_all(self):
        """Arrêter toute routine"""
        try:self.end_replace()
        except:pass

        try:self.end_search()
        except:pass

    def is_select(self):
        """Verifie si du texte est selectionné"""
        if not self.selected and self.selected_text() != None:
            self.selected=True
        if self.selected and self.selected_text()==None:
            self.selected = False
        self.after(500,self.is_select)

    def undo(self):
        """Ctrl+Z"""
        try:self.txt.edit_undo() 
        except:self.bell()
    
    def redo(self):
        """Ctrl+Y"""
        try:self.txt.edit_redo() 
        except:self.bell()

    def ask_confirm(self):
        """Quitter"""
        if messagebox.askyesno("Attention","Êtes-vous sûr de vouloir quitter l'éditeur de texte ?\nToutes modifications non-sauvegardées sera perdue.",parent=self):
            self.destroy()

    def selected_text(self):
        """Renvoie le texte selectionné par l'utilisateur si il existe, None sinon"""
        try:
            return self.txt.get(self.txt.index('sel.first'),self.txt.index('sel.last'))
        except: 
            return None
    
    def askopen(self,*args):
        """Demander pour ouvrir un fichier"""
        if messagebox.askyesno("Ouvrir","Si vous continuez, le fichier actuel sera perdu.\nVoulez-vous continuer ?",parent=self):
            f = self.asking_proc[0](self.FILES,self)
            if f != '':
                self.current = f
                self.open_file()

    def open_file(self):
        """Ouvrir un fichier"""
        with open(self.current,'r',encoding='utf8') as file:
            self.txt.delete(0.0,'end')
            self.end_all()
            self.txt.insert(0.0,file.read())
    
    def save(self,*args):
        """Enregister"""
        if self.current == '': self.saveas()
        else:
            with open(self.current,'w',encoding='utf-8') as f:
                f.write(self.txt.get(0.0,'end'))
    
    def saveas(self):
        """Enregister sous"""
        f = self.asking_proc[1](self.FILES,self)
        if type(f)==str:
            self.current=f
        elif f!=None:
            self.current=f.name
        self.save()
        try:self.applier.change()
        except:pass
 
    def new_file(self,*args):
        """Demander à créer un nouveau fichier"""
        if messagebox.askyesno("Nouveau fichier","Si vous continuez, le fichier actuel sera perdu.\nVoulez-vous continuer ?",parent=self):
            self.current = ''
            self.txt.delete(0.0,"end")

    def change_bg(self,col):
        """Changer de couleur de fond"""
        self.top_frame.configure(bg=col)
        for child in self.top_frame.children.values():
            child.configure(bg=col)
    
    def change_fg(self,col):
        """changer de couleur d'avant plan"""
        for child in self.top_frame.children.values():
            child.configure(fg=col)

    def run(self):
        """Lancer"""
        self.protocol("WM_DELETE_WINDOW", self.ask_confirm)

        self.bind('<Control-s>',self.save)
        self.bind('<Control-n>',self.new_file)
        self.bind('<Control-o>',self.askopen)
        self.bind('<Control-f>',self.search)
        self.bind('<Control-h>',self.replace)

        self.is_select()

        #self.mainloop()

    def open(self,link):
        """Ouvrir un chemin"""
        if messagebox.askyesno("Ouvrir ?","Vous êtes sur le point d'ouvrir un nouveau fichier.\nVoulez-vous sauvegarder celui-ci d'abord ?",parent=self):
            self.save()
        self.current=link
        self.open_file()


def disable_frame(frame:Frame):
    """Met state=disabled à tous les descendants de frame"""
    for child in frame.children.values():
        if type(child)==Frame:
                disable_frame(child)
        elif type(child) in (Text, Menubutton):
            child.configure(state="disabled")

def able_frame(frame:Frame):
    """Met state=normal à tous les descendants de frame"""
    for child in frame.children.values():
        if type(child)==Frame:
                able_frame(child)
        elif type(child) in (Text, Menubutton):
            child.configure(state="normal")