from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import showerror,showinfo
import H.Apps.Turing.form as form,time,pickle
from H.Apps.Turing.drawings import Head,Bandeau,Ecriture
from tkinter.filedialog import askopenfilename,asksaveasfilename
from PersonalWidgets import PopingToplevel

FILES = [
    ('Turing files','.tur')
]

class App(PopingToplevel):
    def __init__(self,master,link='',ask = [
        lambda files,master:askopenfilename(filetypes=files,parent=master),
        lambda files,master:asksaveasfilename(filetypes=files,defaultextension='.tur',parent=master)
    ]):
        super().__init__(master)
        self.transient(master)
        Grid.columnconfigure(self,0,weight=1)        
        Grid.rowconfigure(self,1,weight=1)

        self.ask_protocol = ask

        self.table_transition = {}# {'etat':{'lit1':['e1','d1','s1']}}
        self.initial_state = ''

        if link != '':
            with open(link,'rb') as f:
                data = pickle.load(f)
            self.initial_state = data[0]
            self.table_transition = data[1]

        self.table=None

        self.title("Machine de Turing")

        self.f1=Frame(self)
        self.f1.grid(row=0,column=0,sticky=NSEW)

        self.file = Menubutton(self.f1,text="File",relief=RIDGE)
        self.file.pack(side=LEFT)

        self.menu = Menu(self.file)
        self.menu.add_command(label='Ouvrir',command=self.open)
        self.menu.add_command(label='Enregistrer',command=self.save)

        self.file.config(menu=self.menu)

        self.creer = Button(self.f1,text='Créer',command=self.pop)
        self.creer.pack(side=LEFT)

        self.add = Button(self.f1,text="Texte de départ",command=self.add_text)
        self.add.pack(side=LEFT)

        self.run = Button(self.f1,text='Exécuter',command=self.run_table)
        self.run.pack(side=LEFT)

        self.f2 = Frame(self,bg='grey')
        self.f2.grid(row=1,column=0,sticky=NSEW)

        self.can=Canvas(self.f2,bg='white')
        self.can.pack(pady=5,padx=5,fill=BOTH,expand=True)
        self.can.update()

        self.b = Bandeau(self.can,'c')
        self.h = Head(self.can)
        self.w = Ecriture(self.can,'')

        self.can.bind('<Configure>',self.config)
        
    def add_text(self):
        print('add_text')
        f=form.Formulaire(self)
        f.add_champ('Texte de départ : ',lambda master:Entry(master),lambda p: all(car in ('0',' ','1')for car in p),'Ce doit être une suite de 0, 1 et d\'espaces')
        f.add_submit('Ajouter')
        rep = f.run()
        if not type(rep)==bool:
            self.w.create(rep[0])


    def config(self,evt):
        self.b.config()
        self.h.config()
        self.w.config()

    def pop(self):
        try:
            assert self.table.winfo_exists()
            self.table.destroy()
        except Exception as err:
            self.table=PopUpWindow(self)
    
    def completed(self):
        err=False
        if self.initial_state =='' or self.initial_state not in self.table_transition:
            err=True
            showerror("Etat initial invalide","L'état initial est invalide, soit vous ne l'avez pas renseigné, soit il ne s'agit pas d'un état de la table.")
        if not all(x in self.table_transition.keys() or x=='f' for x in [self.table_transition[k][k_][2] for k in self.table_transition.keys() for k_ in self.table_transition[k].keys()]):
            err=True
            showerror("Etats invalides","Un ou plusieurs états qui peuvent être atteints pendant l'éxecution ne sont pas définis.")
        if not any(x=='f' for x in [self.table_transition[k][k_][2] for k in self.table_transition.keys() for k_ in self.table_transition[k].keys()]):
            err=True
            showerror("Programme sans fin","L'état final n'est jamais atteints lors de l'éxecution du programme.")
        
        return not err
    
    def run_table(self):
        if not self.completed():return

        etat = self.initial_state
        self.w.initial_pos()
        self.add_halt()
        self.halt=False
        self.update()
        time.sleep(0.5)

        while etat != 'f':
            if self.halt:
                self.halt=False
                showinfo("HALT","Vous avez arrété l'exécution")
                break
            l = self.w.get()
            self.w.write(self.table_transition[etat][l][0])
            self.w.deplacer(self.table_transition[etat][l][1])
            etat = self.table_transition[etat][l][2]
            self.update()
            time.sleep(0.5)

        self.destroy_halt()

    
    def add_halt(self):
        self.halt_btn= Button(self.f1,text="Arrêter",command=self.halt_command)
        self.halt_btn.pack(side=LEFT)
    
    def halt_command(self):
        self.halt=True
    
    def destroy_halt(self):
        self.halt_btn.destroy()
    
    def save(self):
        r=self.ask_protocol[1](FILES,self)
        data = [self.initial_state,self.table_transition]

        with open(r,'wb') as f:
            pickle.dump(data,f)
        
    def open(self):
        r = self.ask_protocol[0](FILES,self)
        with open(r,'rb') as f:
            data = pickle.load(f)
        self.initial_state = data[0]
        self.table_transition = data[1]

class PopUpWindow(PopingToplevel):
    def __init__(self, master:App):
        super().__init__(master)
        self.title('Table de transitions')
        self.transient(master)

        self.master:App=master

        self.f1=Frame(self)
        self.f1.grid(row=0,column=0,sticky=NSEW)

        self.new=Button(self.f1,text='Ajouter une ligne',command=self.add)
        self.suppr=Button(self.f1,text='Supprimer un état',command=self.delete)
        self.suppr_line=Button(self.f1,text='Supprimer une ligne',command=self.delete_line)
        self.new.pack(side=LEFT)
        self.suppr.pack(side=LEFT)
        self.suppr_line.pack(side=LEFT)

        self.f2=Frame(self)
        self.f2.grid(row=1,column=0,sticky=NSEW)

        self.s1_f2 = Frame(self.f2)
        self.s1_f2.pack(side=TOP)

        Label(self.s1_f2,text='Etat Initial : ').pack(side=LEFT)
        self.ent = Entry(self.s1_f2)
        self.ent.pack(side=LEFT)
        self.ent.insert(0,self.master.initial_state)

        Label(self.s1_f2,text='.    Etat final : f').pack(side=RIGHT)#,padx=5)

        cols = ["Etat","Lit","Ecrit","Déplacer","Etat suivant"]
        self.table = ttk.Treeview(self.f2,columns=cols,show='headings')
        self.table.pack(side=BOTTOM)

        for obj in cols:
            self.table.heading(obj,text=obj)
        
        for elt in self.master.table_transition.keys():
            for l in self.master.table_transition[elt].keys():
                self.table.insert('','end',values = (elt,l,*self.master.table_transition[elt][l]))
        
        self.ent.bind('<FocusOut>',self.initial)

    def initial(self,evt):
        self.master.initial_state = self.ent.get()
        
    def add(self):
        f=form.Formulaire(self,'Ajouter une ligne')
        f.add_champ("Nom de l'etat",lambda master:Entry(master),lambda p:p!='','','')
        f.add_champ("Lit : ",lambda master:ttk.Combobox(master,state='readonly',values=(' ','1','0')),lambda p:True,'','')
        f.add_champ("Ecrit : ",lambda master:ttk.Combobox(master,state='readonly',values=(' ','1','0')),lambda p:True,'','')
        f.add_champ("Se déplace vers : ",lambda master:ttk.Combobox(master,state='readonly',values=('D','G','')),lambda p:p in ('D','G',''),'','D')
        f.add_champ("Nom de l'état suivant",lambda master:Entry(master),lambda p:p!='','Il doit y avoir un état suivant','')
        f.add_submit('Ajouter')
        rep=f.run()
        if type(rep)==bool:return
        if not rep[0] in self.master.table_transition:
            self.master.table_transition[rep[0]]={}
        
        if rep[1] in self.master.table_transition[rep[0]]:
            showerror('Invalid Input',"Cette ligne existe déjà",parent=self)
            return

        self.master.table_transition[rep[0]][rep[1]]= rep[2:]
        self.table.insert('','end',values=rep)
        print(self.master.table_transition)
    
    def delete(self):
        f=form.Formulaire(self,'Supprimer un état')
        f.add_champ("Nom de l'état :",lambda master:Entry(master),lambda p: p in self.master.table_transition,'Vous devez saisir un état créé','')
        f.add_submit('Supprimer',True)
        rep=f.run()
        if type(rep)==bool:return
        self.table.delete([elt for elt in self.table.get_children() if self.table.item(elt)['values'][0]==rep[0]])
        del self.master.table_transition[rep[0]]
    
    def delete_line(self):
        f=form.Formulaire(self,'Supprimer une ligne')
        f.add_champ("Nom de l'état :",lambda master:Entry(master),lambda p: p in self.master.table_transition,'Vous devez saisir un état créé','')
        f.add_champ("Lit :",lambda master:ttk.Combobox(master,state='readonly',values=(' ','1','0')),lambda p: True,'','')
        f.add_submit('Supprimer',True)
        rep=f.run()
        if type(rep)==bool:return
        if rep[1] not in self.master.table_transition[rep[0]]:
            showerror("Invalid Input","Une ligne telle que vous l'avez décrite n'existe pas !",parent=self)
            self.delete_line()
            return
        self.table.delete([elt for elt in self.table.get_children() if self.table.item(elt)['values'][0]==rep[0] and self.table.item(elt)['values'][1]==int(rep[1])])
        del self.master.table_transition[rep[0]][rep[1]]
        


if __name__=='__main__':
    tk=Tk()
    app=App(tk)
    app.mainloop()
