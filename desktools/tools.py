from tkinter import *
from math import sin,cos,radians
from time import asctime
import psutil
from PersonalWidgets import PopingToplevel

def time_float():
    """Renvoie le nombre de secondes écoulées depuis minuit"""
    h= asctime().split(' ')[4]
    l=h.split(':')
    l=[int(elt) for elt in l]
    return l[0]*3600+l[1]*60+l[2]

class Clock(PopingToplevel):
    def __init__(self,master):
        """Horloge"""
        super().__init__(master,width=250,height=250)
        self.transient(master)
        self.pack_propagate(False)
        self.resizable(0,0)
        self.title('Horloge')

        self.can=Canvas(self,bg='white')
        self.can.pack()
        self.can.create_oval(5,5,245,245,width=5,outline='black')

        for i in range(12):#les 12 graduations
            self.can.create_line(125+cos(radians(30*i))*116,125-sin(radians(30*i))*116,125+cos(radians(30*i))*105,125-sin(radians(30*i))*105)

        self.g=self.can.create_line(125,125,125,35)#grande aiguille
        self.s=self.can.create_line(125,125,125,15,fill='red')#troteuse
        self.p = self.can.create_line(125,125,125,50)#petite aiguille

        self.update()
    
    def update(self):
        s=time_float()%60#nb secondes
        m=time_float()%3600/60#nb minutes
        h=time_float()%43200/3600#nb heures
        #on fait tourner toutes les aiguilles
        self.can.coords(self.s,125,125,125+cos(radians(-6*s+90))*110,125-sin(radians(90-6*s))*110  )
        self.can.coords(self.g,125,125,125+cos(radians(-6*m+90))*90,125-sin(radians(90-6*m))*90  )
        self.can.coords(self.p,125,125,125+cos(radians(-30*h+90))*75,125-sin(radians(90-30*h))*75  )

        self.after(500,self.update)#et on recommence

class Battery(PopingToplevel):
    def __init__(self,master):
        """Affichage du %age de batterie"""
        super().__init__(master,width=120,height=50)
        self.transient(master)
        self.pack_propagate(False)
        self.resizable(0,0)
        self.title('Batterie')


        self.can=Canvas(self,height=50,width=120,bg='white')
        self.can.pack()

        self.can.create_polygon(10,10,110,10,110,20,115,20,115,30,110,30,110,40,10,40,fill='',outline='black')#contour
        self.can.create_rectangle(110,20,115,30,fill='black')#

        self.filled = self.can.create_rectangle(10+2,10+2,10+psutil.sensors_battery().percent-1,40-1,outline='',fill='black')#avancée de la charge
        self.w = self.can.create_text(20,25,text=str(psutil.sensors_battery().percent),fill='white')#%age

        self.update()#mise a jour
    
    def update(self):
        self.can.coords(self.filled,10+2,10+2,10+psutil.sensors_battery().percent-1,40-1)
        self.can.itemconfig(self.w,text=str(psutil.sensors_battery().percent))
        self.after(1500,self.update)


if __name__=='__main__':
    tk=Tk()
    c=Clock(tk)
    b=Battery(tk)
    tk.update()
    tk.mainloop()