from tkinter import *
from typing import Literal
from math import ceil

class Bandeau:
    def __init__(self,master:Canvas,y:int|Literal['c']) -> None:
        x=0
        self.w = 35
        self.items=[]
        self.centered = False
        if y == 'c':
            self.centered = True
            y = master.winfo_height()/2-self.w/2

        nb = ceil(master.winfo_width()/self.w)
        for i in range(nb):
            self.items.append(master.create_rectangle(x,y,x+self.w,y+self.w))
            x+=self.w
        self.master=master
    
    def config(self):#,evt:Event):
        y = self.master.winfo_height()/2-self.w/2
        for it in self.items:
            if self.centered:
                act = self.master.coords(it)
                self.master.coords(it,act[0],y,act[2],y+self.w)
        
        nb = ceil(self.master.winfo_width()/self.w)
        if nb <= len(self.items):return
        x= len(self.items)*self.w
        while nb >len(self.items):
            self.items.append(self.master.create_rectangle(x,y,x+self.w,y+self.w))
            x+=self.w

class Head:
    def __init__(self,master:Canvas):
        self.master=master
        self.w=35#largeur
        x= 0
        while not (x<= self.master.winfo_width()/2 <=x+self.w):
            x+=self.w
        x = (2*x+self.w)/2
        y = self.master.winfo_height()/2+self.w/2
        self.item =self.master.create_polygon(x,y,
                                   x+self.w/2,y+20,
                                   x+self.w/2-10,y+20,
                                   x+self.w/2-10,y+35,
                                   x+self.w/2-25,y+35,
                                   x+self.w/2-25,y+20,
                                   x-self.w/2,y+20,
                                   x,y,fill='',outline='black')
        #self.master.bind('<Configure>',self.config_)

    def config(self):#,evt:Event):
        x= 0
        while not (x<= self.master.winfo_width()/2 <=x+self.w):
            x+=self.w
        x = (2*x+self.w)/2
        y = self.master.winfo_height()/2+self.w/2
        self.master.coords(self.item,x,y,
                                   x+self.w/2,y+20,
                                   x+self.w/2-10,y+20,
                                   x+self.w/2-10,y+35,
                                   x+self.w/2-25,y+35,
                                   x+self.w/2-25,y+20,
                                   x-self.w/2,y+20,
                                   x,y)

class Ecriture:
    def __init__(self,master:Canvas,content:str):
        self.master=master
        self.items=[]
        self.w=35

        self.create(content)
    
    def create(self,content:str):
        self.index=0

        x= 0
        while not (x<= self.master.winfo_width()/2 <=x+self.w):
            x+=self.w
        x = (2*x+self.w)/2
        y = self.master.winfo_height()/2

        for car in content:
            self.items.append(self.master.create_text(x,y,text=car))
            x+=self.w

    def config(self):
        x= 0
        while not (x<= self.master.winfo_width()/2 <=x+self.w):
            x+=self.w
        x = (2*x+self.w)/2
        y = self.master.winfo_height()/2

        for it in self.items:
            self.master.coords(it,x,y)
            x+=self.w
        
    def deplacer(self,direction:Literal['d']|Literal['g']|Literal['']):
        if direction == '':return

        if direction == 'D':
            for it in self.items:
                self.master.move(it,-self.w,0)
            self.index+=1
        elif direction=='G':
            for it in self.items:
                self.master.move(it,self.w,0)
            self.index-=1
    
    def get(self):
        if not 0<=self.index<len(self.items):
            return ''
        r=self.master.itemcget(self.items[self.index],'text')
        return '' if r==' ' else r

    def write(self,val:str):
        if val == '':val=' '
        if 0<=self.index<len(self.items):
            self.master.itemconfig(self.items[self.index],text=val)
        elif self.index>=0:
            x= 0
            while not (x<= self.master.winfo_width()/2 <=x+self.w):
                x+=self.w
            x = (2*x+self.w)/2
            y = self.master.winfo_height()/2
            self.items.append(self.master.create_text(x,y,text=val))
        elif self.index == -1:
            x= 0
            while not (x<= self.master.winfo_width()/2 <=x+self.w):
                x+=self.w
            x = (2*x+self.w)/2
            y = self.master.winfo_height()/2
            self.items = [self.master.create_text(x,y,text=val)]+self.items
            self.index=0
        else:
            raise KeyError("Can't create a text here, ")
    
    def get_content(self):
        return ''.join([self.master.itemcget(it,'text') for it in self.items])
    
    def initial_pos(self):
        if self.index<0:
            s='D'
        else:
            s='G'

        while self.index != 0:
            self.deplacer(s)

        
        #content=self.get_content()

        #for it in self.items:
        #    self.master.delete(it)
        #self.items=[]

        #self.create(content)
