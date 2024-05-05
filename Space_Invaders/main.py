from __future__ import annotations

from tkinter import *
from tkinter.font import Font
import time,random 
from math import cos,sin,radians
from PersonalWidgets import PopingToplevel

class Score:
    def __init__(self,can:Canvas):
        """Dessine le score du joueur"""
        self.n = 0
        self.can=can
        self.id = self.can.create_text(int(self.can['width'])-50,25,text="Score : 0",fill="white",font=Font(size=15))
    
    def update(self):
        self.can.itemconfig(self.id,text="Score : "+str(self.n))
    
    def increment(self,n):
        self.n+=n
        self.update()

class HealthBar:
    def __init__(self,can:Canvas):
        """Dessine la barre de PV du joueur"""
        self.can=can
        self.text = self.can.create_text(int(self.can['width'])-45,70,text='P.V. : 100',fill='white')
        self.ext_bar = self.can.create_rectangle(int(self.can['width'])-50,85,int(self.can['width'])-30,285,fill='#646464')#barre extèrieure
        self.int_bar = self.can.create_rectangle(int(self.can['width'])-50,85,int(self.can['width'])-30,285,fill='#00b500')#barre intérieure
        self.pv=100

    def decrease(self,n):
        self.pv-=n 
        self.draw()
    
    def draw(self):
        self.can.coords(self.int_bar,int(self.can['width'])-50,85+2*(100-self.pv),int(self.can['width'])-30,285)
        self.can.itemconfig(self.text,text='P.V. : '+str(self.pv))

class Vaisseau:
    def __init__(self,can:Canvas):
        """Le joueur"""
        self.tirs:list[PlayerProjectile]=[]#liste des missilles qu'il a envoyé
        self.dt=0#decompte entre 2 tirs
        
        self.stop=False

        self.can=can
        self.id = self.can.create_polygon(
            10,int(self.can['height'])-10,
            10,int(self.can['height'])-20,
            20,int(self.can['height'])-30,
            40,int(self.can['height'])-30,
            50,int(self.can['height'])-20,
            50,int(self.can['height'])-10,
            fill='#006a00')#le vaisseau
        
        self.buse = self.can.create_line(30,int(self.can['height'])-30,30,int(self.can['height'])-40,fill='#006a00',width=2)#le canon
        self.score = Score(self.can)#on a un score

        self.health = HealthBar(self.can)#et des pv

        self.dx=int(self.can["width"])/2-130/2
        self.move()#se placer au centre
        self.dx=random.choice([-5,5])

    
    def move(self):
        c=(self.can.coords(self.id))
        if c[0]+self.dx >=10 and c[-2]+self.dx<=int(self.can['width'])-120 and not self.stop:#si on peut se déplacer sans sortir du cadre
            self.can.move(self.id,self.dx,0)
            self.can.move(self.buse,self.dx,0)
            time.sleep(1e-4)
        elif not self.stop:
            self.dx=-self.dx
    
    def fire(self,ennemies):#tirer
        if self.dt>=.25 and not self.stop:#on peut tirer toutes les 250 ms
            c=self.can.coords(self.buse)
            self.tirs.append(PlayerProjectile(self.can,c[-2],c[-1]-10,self,ennemies))
            self.dt=0
    
    def update(self):
        for t in self.tirs:#on déplace tous les tirs
            r=t.move()
            if r[0]=='eol':#si le tir à touché le bord on l'enlève
                self.tirs.remove(t)
            if r[1]==False:#si en plus il a touché un ennemi on ajoute 10 pts
                self.score.increment(10)

        self.dt+=0.05
        self.move()
        if not self.stop:#recommencer à mettre à jour
            self.can.after(50,self.update)

    def attacked(self):#si un projectille ennemi nous touche : -5 pv
        self.health.decrease(5)
    
    def change_dx(self,dx):
        self.dx=dx

class PlayerProjectile:
    def __init__(self,can:Canvas,x,y,parent:Vaisseau,ennemies:list[Ennemy]):
        """Tir du joueur"""
        self.can=can
        self.id = self.can.create_oval(x-1,y,x+1,y+10,fill='orange',outline='red')
        self.parent=parent#le vaisseau
        self.ennemies=ennemies#les ennemis

        self.alive=True
    
    def move(self):
        self.detect_collisions()
        c=self.can.coords(self.id)
        if c[-1]-10>0 and self.alive:#si on vit on bouge
            self.can.move(self.id,0,-10)
        else:#sinon on dit qu'on est détruit
            self.can.delete(self.id)
            return 'eol',self.alive 
        
        return None,None
    
    def detect_collisions(self):
        coll = list(self.can.find_overlapping(*self.can.coords(self.id)))#si on touche qqch
        coll.remove(self.id)#autre que nous même
        if self.parent.buse in coll:coll.remove(self.parent.buse)#autre que le canon
        if self.parent.score.id in coll:coll.remove(self.parent.score.id)#et peut être le score

        if coll != []:#i on touche qqch
            for collide in coll:
                for en in self.ennemies:
                    if collide in en.get_ids():
                        en.eol()#on tue l'ennemi
            
            self.eol()#et on disparait
    
    def eol(self):
        self.alive=False

class EnnemyProjectile:
    def __init__(self,can:Canvas,x,y,player:Vaisseau):
        """Tirs ennemis"""
        self.can=can
        self.player=player
        self.id = self.can.create_oval(x-5,y-5,x+5,y+5,fill='#006a00')
        self.alive=True

    def move(self):
        """Même principe que pour PlayerProjectile"""
        self.can.move(self.id,0,5)
        self.detect_collisions()
        if self.can.coords(self.id)[3] >= int(self.can['height']) or self.alive==False:
            self.can.delete(self.id)
            return 'eol'
    
    def detect_collisions(self):
        coll = list(self.can.find_overlapping(*self.can.coords(self.id)))
        coll.remove(self.id)
        if self.player.buse in coll or self.player.id in coll:
            self.player.attacked()
            self.eol()
    
    def eol(self):
        self.alive=False

class Ennemy:
    def __init__(self,can:Canvas,player:Vaisseau,proj_list,dx=5):
        """Les ennemis"""
        self.can=can
        self.id=self.can.create_polygon(10,30,10,20,20,10,50,10,60,20,60,30,fill='#006a00')#le corps
        #les yeux
        self.leye = self.can.create_oval(22.5,15,27.5,20,fill='white',outline='white')
        self.reye = self.can.create_oval(42.5,15,47.5,20,fill='white',outline='white')

        #les antennes
        self.lfeeler = self.can.create_line(20,10,20-5*cos(radians(25)),10-5*sin(radians(25)),fill='#006a00')
        self.rfeeler = self.can.create_line(50,10,50+5*cos(radians(25)),10-5*sin(radians(25)),fill='#006a00')
        self.foot=[
            self.can.create_line(10,30,10,40,fill='#006a00'),
            self.can.create_line(20,30,20,40,fill='#006a00'),
            self.can.create_line(30,30,30,40,fill='#006a00'),
            self.can.create_line(40,30,40,40,fill='#006a00'),
            self.can.create_line(50,30,50,40,fill='#006a00'),
            self.can.create_line(59,30,59,40,fill='#006a00'),
        ]#les pattes

        self.alive = True

        self.player=player
        self.proj_list = proj_list

        self.dx=dx
        self.dt=0
    
    def move(self):
        """Se déplacer"""
        c=self.can.coords(self.id)

        if not self.alive:#destruction
            self.delete()
            return 'eol'
        
        #se déplacer
        if c[0]+self.dx<=10 or  c[-2]+self.dx>=int(self.can['width'])-120:#si on doit aller dans l'autre sens (on touche le bord)
            dx=0
            dy=40
            self.dx=-self.dx
        else:#sinon on avance
            dx=self.dx
            dy=0
        
        if self.dt >= 2.05:#tirer
            if random.randint(1,3) == 2:#1/3 chance de tirer
                self.dt=0
                self.proj_list.append(EnnemyProjectile(self.can,c[0]/2+c[-2]/2,c[1],self.player))

        #se déplacer
        self.can.move(self.id,dx,dy)
        self.can.move(self.leye,dx,dy)
        self.can.move(self.reye,dx,dy)
        self.can.move(self.lfeeler,dx,dy)
        self.can.move(self.rfeeler,dx,dy)
        self.move_foot(dx,dy)

        self.dt += 0.05
        
    def move_foot(self,dx,dy):
        """Déplacer les pattes"""
        for f in self.foot:
            self.can.move(f,dx,dy)
    
    def get_ids(self):
        """id de tous les objets qui compose le monstre"""
        return [self.id,self.leye,self.reye,self.lfeeler,self.rfeeler]+self.foot

    def eol(self):
        self.alive=False
    
    def delete(self):
        """Suppression"""
        for id in self.get_ids():
            self.can.delete(id)

class Jeu(PopingToplevel):
    def __init__(self,master):
        """Classe du jeu"""
        super().__init__(master)
        self.transient(master)
        self.title("Space Invaders")
        self.resizable(0,0)

        self.canvas = Canvas(self,height=675,width=750,highlightthickness=0)
        self.canvas.pack(expand=True,fill=BOTH)

        self.welcome_screen()
    
    def welcome_screen(self,*args):
        """Ecran d'accueil"""
        self.canvas.delete('all')
        self.canvas['bg']="black"
        self.canvas.create_text(750/2,750/2-50,text="Space Invaders",font=Font(family="OCR A Extended",size=50),fill='white')
        self.canvas.create_text(750/2,750/2,text="Appuyer sur <Entrée> pour commencer",fill='white',font=Font(family='Arial',size=10))
        self.canvas.bind_all('<Return>',self.playing_screen)#on attend une action
    
    def playing_screen(self,*args):
        """Ecran de jeu"""
        self.ennemies:list[Ennemy]=[]#liste des monstres
        self.ennemies_proj:list[EnnemyProjectile]=[]#liste desprojectiles ennemis

        self.dt=0#gérer apparition ennemis

        self.canvas.delete('all')#tout nettoyer

        self.vais = Vaisseau(self.canvas)

        #detection touches
        self.canvas.bind_all('<Right>',lambda arg: self.vais.change_dx(5))
        self.canvas.bind_all('<Left>',lambda arg: self.vais.change_dx(-5))
        self.canvas.bind_all('<space>',lambda arg: self.vais.fire(self.ennemies))

        self.canvas.create_line(750-110,0,750-110,675,fill='white')#séparation écran de jeu

        self.vais.update()
        self.update()
    
    def game_over(self):
        """Message Game Over"""
        self.canvas.delete('all')
        self.canvas.create_text(750/2,750/2-50,text="Game Over...",font=Font(family="OCR A Extended",size=50),fill='white')
        self.canvas.create_text(750/2,750/2,text="Appuyer sur <Entrée> pour revenir à l'écran d'accueil",fill='white',font=Font(family='Arial',size=10))
        self.canvas.bind_all('<Return>',self.welcome_screen)
    
    def update(self):
        """Mise à jour de l'écran"""
        if self.dt<=0:#créer un nouvel ennemi
            self.ennemies.append(Ennemy(self.canvas,self.vais,self.ennemies_proj))
            self.dt=2.05
        self.dt-=0.05

        for ennemy in self.ennemies:#deplacer tous les ennemis
            if ennemy.move()=='eol':
                self.ennemies.remove(ennemy)

        for tir in self.ennemies_proj:#déplacer tous les tirs 
            if tir.move() =='eol':
                self.ennemies_proj.remove(tir)

        if self.vais.health.pv<=0:
            self.vais.stop=True
            self.game_over()
        else:   
            self.canvas.after(50,self.update)#répeter
