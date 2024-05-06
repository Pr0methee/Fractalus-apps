#essaye de prendre en compte le plus de version de python possible.
try :
    from tkinter import *
except:
    from Tkinter import *

try:
    import conversion
except:
    import H.Apps.Conversions.conversion as conversion
import time
import tkinter.colorchooser as colorchooser
import tkinter.messagebox as messagebox
from PersonalWidgets import PopingToplevel

#########################################################
#Variables indispensable tout au long du programme :    #
#-couleurs : variable de type dict, contient les différ #
# entes couleurs choisies par l'utilisateur             #
#-precision : variable de type dict, contient le nombre #
# de bits associés à chaque précision (IEEE754)         #
#-state : variable de type int, "état" de l'application #
# 0=Menu, 1=conversion, 2=informations, 3=options       #
#########################################################

couleurs={
    "bg":"SystemButtonFace",
    "error":"red",
    "text":"SystemButtonText",
    "button_bg":"SystemButtonFace",
    "button_fg":"SystemButtonText"
}

precision ={
    '128':'quadruple',
    '64':'double',
    '32':'simple'
}

state=0

#Fonction de mise à jour :
def verif():
    #selection des bases d'arrivée et de départ
    base = ["10","2","8","16","float","C2-8","C2-16","C2-32","IEEE754-32","IEEE754-64","IEEE754-128"][basedepact.get()]
    base_ar = ["10","2","8","16","C2-8","C2-16","C2-32","IEEE754-32","IEEE754-64","IEEE754-128"][basedarract.get()]

    #affiche les bases de départ et d'arrivée choisis
    str_var_dep.set("Base de départ : "+base)
    str_var_arr.set("Base d'arrivée : "+base_ar)

    error = False#booléen qui vérifie si il y a une erreur dans le nombre à coder (C2) ou dans la base d'arrivée cf en dessous
    if conversion.is_of_base(entry.get(),base):
        Lab['fg'] = couleurs["text"]

        #1er if : obtenir l'entrée en base 10
        if base.isdigit() and base != "10":
            dix = conversion.to_ten(entry.get(),int(base))
        elif base == "10":
            if 'inf' in entry.get():
                dix=entry.get()
            else:
                dix=int(entry.get())
        elif "C2" in base:
            dix = conversion.from_C2(entry.get())
        elif  "IEEE754" in base :
            dix = conversion.from_IEEE754(entry.get())
        else:
            dix = float(entry.get())

        #2ème if : convertir
        if base_ar == "10":
            nb = dix
            if type(nb)==str:#si nb est un str soit c'est +/- inf soit NaN
                if nb[1:] == "inf":#afficher le symbole infini
                    nb=nb[0]+chr(8734)
                else:#sinon c'est NaN
                    Lab["fg"] = couleurs["error"]
        else:
            #gérer les erreurs de base finale
            if (type(dix)==float and not "IEEE754" in base_ar):#on ne fait pas d'arrondis !
                textvar.set("ERREUR-Mauvaise base d'arrivée")
                Lab['fg']=couleurs["error"]
                error = True
            if type(dix) != str:
                if dix<0 and ((not ('C2'in base_ar)) and (not ('IEEE754' in base_ar))):#on ne peuut mettre des négatif qu'en IEEE754 ou en C2 !
                    textvar.set("ERREUR-Mauvaise base d'arrivée")
                    Lab['fg']=couleurs["error"]
                    error = True
            if (dix == '-inf' and not 'IEEE754'in base_ar) or (dix == '+inf' and not 'IEEE754'in base_ar):#on ne code +/- inf qu'en IEEE754 !
                textvar.set("ERREUR-Mauvaise base d'arrivée")
                Lab['fg']=couleurs["error"]
                error = True
            #convertir
            if not error :
                if 'C2' in base_ar :
                    try:#vérifie que le nombre entré par l'utilisateur peut se coder en C2
                        nb = conversion.C2(dix, int(base_ar.split('-')[1]))
                    except AssertionError:
                        error = True
                        textvar.set("ERREUR-Pas assez de bits pour afficher le nombre")
                        Lab['fg']=couleurs["error"]
                elif 'IEEE754' in  base_ar :
                    nb = conversion.to_IEEE754(dix,precision[base_ar.split('-')[1]])
                else:
                    nb = conversion.from_ten(dix,int(base_ar))
        
        if not error:
            if base_ar == 'IEEE754-128':#lisibilité pour la quadruple précision, sur une seule ligne, c'est un chouïa illisible !
                textvar.set(nb[:64]+'\n'+nb[64:])
            else:
                textvar.set(str(nb))
    else:
        textvar.set("ERREUR-Mauvaise entrée")
        Lab['fg']=couleurs["error"]


#Fonctions de créations :
def create_home(master):
    """Fonction qui permet de creer la fenetre de menu de l'application"""
    global state
    state=0
    #on efface tout ...
    n=master.children.copy()
    for child in n.values():
        child.destroy()

    #on définie bien la fenetre pour ce qu'on fait
    master.geometry("200x175")
    master['bg']=couleurs["bg"]
    master.title('Menu')

    #on crée les boutons de redirection
    Label(master, text="Bienvenue",bg=couleurs["bg"],fg=couleurs["text"], font=('Papyrus',10)).pack(padx=50)
    Button(master, text="Convertir",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command= lambda boss=master:create_convert(boss)).pack(padx=50,pady=10)
    Button(master, text="Informations",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command= lambda boss=master:create_info(boss)).pack(padx=50,pady=10)
    Button(master, text="Options",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command= lambda boss=master:create_options(boss)).pack(padx=50,pady=10)


def create_convert(master):
    """Fonction qui permet de créer l'interface de conversion"""
    global Lab, basedepact, basedarract, entry, textvar,state, str_var_dep, str_var_arr
    state=1
    #on efface tout ...
    n=master.children.copy()
    for child in n.values():
        child.destroy()

    #on définie bien la fenetre pour ce qu'on fait
    master.geometry("600x125")
    master['bg']=couleurs["bg"]
    master.title("Convertisseur")
    
    frame1= Frame(master,bg=couleurs["bg"])#partie de la fenetre avec les menus déroulants
    frame1.pack()
    
    frame2 = Frame(master,bg=couleurs["bg"])#2ème partie
    frame2.pack(padx=5,pady=20)

    #Creation des champs de saisie et de reponse
    textvar = StringVar()
    entry = Entry(frame2)
    entry.pack(side=LEFT)
    Lab= Label(frame2, textvariable=textvar,bg=couleurs["bg"], fg=couleurs['text'])
    Lab.pack(side=RIGHT)
    Label(frame2,text=" = ",bg=couleurs["bg"], fg=couleurs['text']).pack(side=RIGHT)

    #menu deroulant pour choisir la base entrée
    str_var_dep = StringVar()
    Label(frame1,textvariable=str_var_dep,bg=couleurs["bg"], fg=couleurs['text'], height=1).pack(side=LEFT)#label qui informe de la base de départ choisie

    basedep = Menubutton(frame1, text="Base de départ",bg=couleurs["button_bg"], fg=couleurs["button_fg"],relief=RAISED)
    basedep.pack(side=LEFT)

    basedepact = IntVar()
    menubasedep = Menu(basedep)
    for (v,lab) in [(0,"Décimale (entier)"),(1,"Binaire"),(2,"Octale"),(3,"Héxadécimale"),(4,"Décimale (flotant)"),(5,"Complément à 2 (8bits)"),(6,"Complément à 2 (16bits)")
    ,(7,"Complément à 2 (32bits)"),(8,"IEEE754 (32bits)"),(9,"IEEE754 (64bits)"),(10,"IEEE754 (128bits)")]:
        menubasedep.add_radiobutton(label=lab, variable=basedepact, value = v)
    basedep.configure(menu = menubasedep)

    #menu deroulant pour choisir la base de conversion
    str_var_arr = StringVar()
    Label(frame1,textvariable=str_var_arr,bg=couleurs["bg"], fg=couleurs['text']).pack(side=RIGHT)#label qui informe de la base d'arrivée choisie

    basedarr = Menubutton(frame1, text="Base d'arrivée",bg=couleurs["button_bg"], fg=couleurs["button_fg"],relief=RAISED)
    basedarr.pack(side=LEFT)

    basedarract = IntVar()
    menubasedarr = Menu(basedarr)
    for (v,lab) in [(0,"Décimale"),(1,"Binaire"),(2,"Octale"),(3,"Héxadécimale"),(4,"Complément à 2 (8bits)"),(5,"Complément à 2 (16bits)")
    ,(6,"Complément à 2 (32bits)"),(7,"IEEE754 (32bits)"),(8,"IEEE754 (64bits)"),(9,"IEEE754 (128bits)")]:
        menubasedarr.add_radiobutton(label=lab, variable=basedarract, value = v)
    basedarr.configure(menu = menubasedarr)

    #bouton 'Menu'
    Button(master, text="Menu",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command = lambda boss=master : create_home(boss)).pack()
    entry.insert(0,"0")
    
def create_info(master):
    """Fonction qui permet de creer la fenetre d'information"""
    global state
    state=2
    #on efface tout...
    n=master.children.copy()
    for child in n.values():
        child.destroy() 

    #et on affiche correctement
    master.geometry("400x350")
    master['bg']=couleurs["bg"]
    master.title("Informations")

    txt=Text(master, height=19, bg = couleurs['bg'],fg=couleurs["text"])
    txt.pack()
    txt.insert(1.0,"\tBonjour, bienvenue dans cette application de changement de base. Cette application répond au projet n°7 de NSI. \
Dans la partie 'convertir' du menu d'accueil vous pourrez convertir le nomnbre que vous souhaitez, écrit dans la base que vous souhaitez, dans une autre base.\n\
\tCette application propose plusieurs bases de départ : décimale, binaire, octale, héxadécimale, décimale flottante, complément à 2 sur 8/16/32 bits et IEEE754 sur 32/64/128 bits\n\
\tElle propose également les mêmes bases d'arrivée.\n\
Il y a également plusieurs valeurs spéciales: en base décimale vous pouvez entrer +inf ou -inf mais ceci ne pourra être interprété qu'en IEEE754 ou en base décimale.\n\
Enfin, en IEE754 vous pouvez entrer les chaines correspondant à NaN, -infini et +infini.")
    txt.configure(state="disabled")
    Button(master, text="Menu",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command = lambda boss=master : create_home(boss)).pack()

def create_options(master):
    """Fonction qui permet de creer la fenetre où l'utilisateur va choisir les couleurs de l'application, ensuite stockées dans le dict couleurs"""
    global state
    state=3
    #on efface tout...
    n=master.children.copy()
    for child in n.values():
        child.destroy() 

    #et on affiche correctement
    master.geometry("300x575")
    master['bg']=couleurs["bg"]
    master.title("Options")

    #Pour chaque couleur, il y a un paragraphe avec:
    #un label qui indique de quelle couleur on parle
    #un label qui donne la valeur actuellle de cette couleur
    #et un bouton qui va permettre de modifier la couleur

    #1er § : arrière plan, clé : "bg"
    Label(master,text="Couleur d'arrière plan :",bg=couleurs["bg"], fg=couleurs['text']).pack()
    Label(master, text=couleurs["bg"],font=('TkDefaultFont',10,'italic'),bg=couleurs["bg"], fg=couleurs['text']).pack()
    Button(master,text="Changer",command=lambda which = "bg",master=master:change_colour(which,master),bg=couleurs["button_bg"],fg=couleurs["button_fg"]).pack()

    #2eme § : avant plan, clé : "text"
    Label(master,text="\n\nCouleur du texte :",bg=couleurs["bg"], fg=couleurs['text']).pack()
    Label(master, text=couleurs["text"],font=('TkDefaultFont',10,'italic'),bg=couleurs["bg"], fg=couleurs['text']).pack()
    Button(master,text="Changer",command=lambda which = "text",master=master:change_colour(which,master),bg=couleurs["button_bg"],fg=couleurs["button_fg"]).pack()

    #3eme § : avant plan si erreur, clé : "error"
    Label(master,text="\n\nCouleur du texte d'erreur :",bg=couleurs["bg"], fg=couleurs['text']).pack()
    Label(master, text=couleurs["error"],font=('TkDefaultFont',10,'italic'),bg=couleurs["bg"], fg=couleurs['text']).pack()
    Button(master,text="Changer",command=lambda which = "error",master=master:change_colour(which,master),bg=couleurs["button_bg"],fg=couleurs["button_fg"]).pack()

    #3eme § : arrière plan des boutons, clé : "button_bg"
    Label(master,text="\n\nCouleur des boutons :",bg=couleurs["bg"], fg=couleurs['text']).pack()
    Label(master, text=couleurs["button_bg"],font=('TkDefaultFont',10,'italic'),bg=couleurs["bg"], fg=couleurs['text']).pack()
    Button(master,text="Changer",command=lambda which = "button_bg",master=master:change_colour(which,master),bg=couleurs["button_bg"],fg=couleurs["button_fg"]).pack()

    #4eme § : avant plan des boutons, clé : "button_fg"
    Label(master,text="\n\nCouleur du texte des boutons :",bg=couleurs["bg"], fg=couleurs['text']).pack()
    Label(master, text=couleurs["button_fg"],font=('TkDefaultFont',10,'italic'),bg=couleurs["bg"], fg=couleurs['text']).pack()
    Button(master,text="Changer",command=lambda which = "button_fg",master=master:change_colour(which,master),bg=couleurs["button_bg"],fg=couleurs["button_fg"]).pack()

    #un bouton pour réinitialiser les couleurs
    Button(master, text="Réinitialiser",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command = lambda boss=master : default(boss)).pack(pady=15)
    
    #un dernier pour quiter le menu 'options'
    Button(master, text="Menu",bg=couleurs["button_bg"],fg=couleurs["button_fg"], command = lambda boss=master : create_home(boss)).pack()
    
def change_colour(which, master):
    """Fonction qui demande à l'utilisateur de saisir une couleur avec colorchooser.askcolor, which correspond à la clé du dict couleurs à modifier, master=fenetre Tk()"""
    answer = colorchooser.askcolor()
    #si l'utilisateur ferme la fenêtre, renvoie (None,None)
    if answer != (None, None):
        couleurs[which] = answer[1]
        create_options(master)#rafraichir l'affichage

def default(master):
    """Fonction qui met les valeurs par défaut dans le dict, master=fenetre Tk()"""
    couleurs["bg"]="SystemButtonFace"
    couleurs['error'] ="red"
    couleurs["text"]="SystemButtonText"
    couleurs["button_bg"]="SystemButtonFace"
    couleurs["button_fg"]="SystemButtonText"
    create_options(master)

##################################
# Partie principale du programme #
# Valentin Novo - NSI projet 7   #
##################################
def run(master):
    fen = PopingToplevel(master)
    fen.transient(master)
    fen.resizable(0,0)

    create_home(fen)

    loop(fen)
    return fen

def loop(fen:PopingToplevel):
    if state ==1:
        verif()
    fen.after(500,lambda:loop(fen))

class Fenetre(PopingToplevel):
    def __init__(self,master):
        super().__init__(master)
        self.transient(master)
        self.resizable(0,0)

        create_home(self)
        
if __name__ == '__main__':
    
    fen = Tk()
    fen.resizable(0,0)

    create_home(fen)

    #petite animation
    fen.iconify()
    fen.update()
    fen.deiconify()

    while 1:#boucle principale du programme : on met à jour !
        try:
            time.sleep(1*10**-3)
            fen.update()
            if state == 1:
                verif()
        except:
            break
    master = Tk()
    master.withdraw()
    messagebox.showinfo("Crédits","Projet n°7 de NSI.\nApplication de conversion entre 2 bases.\nValentin Novo, 1G4")