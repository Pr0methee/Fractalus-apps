from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import connect,H.Apps.admintools.form as form
from PersonalWidgets import PopingToplevel

class AdminInterface(PopingToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.title('Utilisateurs')
        self.geometry("400x200")
        self.transient(master)

        #Liste des utilisateurs dans le widget treeview
        self.tree =ttk.Treeview(self,columns=('Identifiant','Mot de Passe'),show='headings')#ligne d'en-tête
        for col in ('Identifiant','Mot de Passe'):
            self.tree.heading(col, text=col)
        self.tree.pack()

        self.add_all()
       
        self.tree.bind('<<TreeviewSelect>>',self.act)
    
    def add_all(self):
        """Ajoute tous le monde"""
        for pers in connect.get_profils():
            if pers[0] != 'admin':
                self.tree.insert('',END,values=(pers[0],'•'*len(pers[1])))#permet de cacher le mot de passe
        self.tree.insert('',END,values=('+',''))#bouton pour ajouter quelqu'un

    def act(self,*args):
        """Action à effectuer quand on selectionne un utilisateur"""
        for selected_item in self.tree.selection():#Prend la personne selectionnée (il ne peut y en avoir qu'une)
            item = self.tree.item(selected_item)
            record = item['values']#obtenir uniquement nom et mdp
            
            if record[0]=='+':#dijonction de cas : ajouter qqun 
                self.f=form.Formulaire(self,"Ajouter un profil")
                self.f.add_champ("Mot de passe Administrateur : ",lambda master:Entry(master,show='•'),lambda p:p!='','Attention, ce champ est vide')
                self.f.add_champ("Nom d'utilisateur",lambda master:Entry(master),lambda p:p!='','Attention, ce champ est vide')
                self.f.add_champ("Mot de passe de l'utilisateur",lambda master:Entry(master,show='•'),lambda p:p!='','Attention, ce champ est vide')
                self.f.add_submit("Continuer",True)
                l= self.f.run()
                if l not in (False,None):
                    r=connect.create_profil(l[1],l[2])
                    if r!='OK':
                        messagebox.showerror('Erreur',r)
                    self.update_table()
            else:#si on doit modifier/voir qqch
                #le mot de passe admin sert à verifier l'identité de l'utilisateur
                self.f=form.Formulaire(self,"Modifier le profil : "+record[0])
                self.f.add_champ("Mot de passe Administrateur : ",lambda master:Entry(master,show='•'),lambda p:p!='','Attention, ce champ est vide')
                self.f.add_champ("Que voulez-vous faire ?\n",lambda master:form.RadioChooser(master,[("Voir le mot de passe",0),("Supprimer le profil",1),("Changer le mot de passe",2)]),lambda p:True,'')
                self.f.add_submit("Continuer",True)
                l= self.f.run()
                if l not in (False,None):
                    if connect.good_admin_psw(l[0]):
                        if l[1]==0:
                            messagebox.showinfo(f"Mot de passe de : {record[0]}",connect.get_psw(record[0])[0])
                        elif l[1]==1:
                            if messagebox.askyesno("Supprimer le profil ?",f"Êtes-vous certain de vouloir supprimer le profil de : {record[0]}"):
                                connect.delete_profil(record[0])
                                self.update_table()
                        else:
                            self.f = form.Formulaire(self,"Nouveau mot de passe de  : "+record[0])
                            self.f.add_champ("Nouveau mot de passe : ",lambda master : Entry(master,show='•'),lambda p: p!='','Attention, ce champ est vide')
                            self.f.add_submit(conf=True)
                            l=self.f.run()
                            if l not in (None,False):
                                connect.change_psw(record[0],l[0])
                                self.update_table()
                    else:
                        messagebox.showerror("Opération refusée","Mot de passe administrateur invalide.\nAction refusée.",parent=self)

    def update_table(self):
        """Mise à jour de la table d'utilisateur"""
        for child in self.tree.get_children():
            self.tree.delete(child)
        self.add_all()