import requests,json,os,H.Apps.Updater.markdown_tk as markdown_tk,resize,json,H.Apps.Updater.form as form
from io import StringIO,BytesIO
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk
from PersonalWidgets import PopingToplevel
import launcherror,tkinter.messagebox as messagebox

class Loader:
    def __init__(self):
        self.base = r"https://raw.githubusercontent.com/Pr0methee/test_apps/main/"
        self.index = self.load_indexer()

    def load_indexer(self)->dict:
        rep = self.load_an_object(r"desc.json").decode()#desc.json
        rep=rep.replace('{"--début--"}','')
        rep=rep.replace('{"--fin--"}','')
        io =StringIO(rep)
        return json.load(io)
    
    def load_json(self,path):
        rep = self.load_an_object(path).decode()#desc.json
        io =StringIO(rep)
        return json.load(io)

    def load_an_object(self,path)->bytes:
        rep = requests.get(self.base+path)
        return rep.content
    
    def load_app(self,nom,location):
        data = self.index[nom]['content']
        if not os.path.exists(location):
            os.mkdir(location)
        if not os.path.exists(location+'\\'+nom):
            os.mkdir(location+'\\'+nom)
        
        for elt in data:
            res = self.load_an_object(nom+'/'+elt)
            
            with open(location+nom+'\\'+elt,"wb") as f:
                f.write(res)

class Loading_App(PopingToplevel):
    def __init__(self, master,loader:Loader):
        
        super().__init__(master)
        self.transient(master)

        self.loader = loader
        self.changed=False
        self.btns={}
        i=0
        self.imgs=[]
        Label(self,text='Applications disponibles :\n\n',font=("Comic",15,'bold','underline')).pack()

        self.f2=Frame(self)
        self.f2.pack()
        for elt in self.loader.index.keys():
            f=Frame(self.f2)
            text=scrolledtext.ScrolledText(f,bg='SystemButtonFace',height=10,width=45,wrap=WORD)
            text.pack()
            self.imgs.append(self.loader.load_an_object(elt+'/'+self.loader.index[elt]['icon']))
            self.imgs[-1] = ImageTk.PhotoImage(resize.cached_resize(75,1,BytesIO(self.imgs[-1])))

            text.image_create('0.0',image=self.imgs[-1])
            text.insert('end','\n')

            result = self.loader.load_an_object(elt+"/article.md").decode()
            markdown_tk.add_markdown(result,text)

            text.config(state='disabled')
            btn=Button(f,text='Download',command=lambda name=elt:self.download(name))
            btn.pack(side=LEFT)
            up=Button(f,text='Update',command=lambda name=elt:self.update_app(name))
            up.pack(side=LEFT)

            if os.path.exists("H\\Apps\\"+elt):
                btn.configure(state='disabled')
                with open("H\\Apps\\"+elt+"\\VERSION.json",'r')as file:
                    if json.load(file)["VERSION"] == self.loader.index[elt]['VERSION']:
                        up.config(state='disabled')
            else:
                up.config(state='disabled')
            self.btns[elt]={
                "Download":btn,
                "Update":up
            }
            f.grid(row=i//4,column=i%4)
            i+=1
        self.poping()
        self.protocol("WM_DELETE_WINDOW", self.exit)
    
    def download(self,name):
        self.changed=True
        self.loader.load_app(name,r"H\Apps\\")
        self.btns[name]["Download"].config(state="disabled")
    
    def update_app(self,name):
        self.changed=True
        data = self.loader.load_json(name+"/VERSION.json")
        for elt in data['UPDATES']:
            ch = elt.split(' ')
            match ch:
                case ['rewrite', file]:
                    with open("H\\Apps\\"+name+'\\'+file,"wb") as f:
                        f.write(self.loader.load_an_object(name+'/'+file))
                case ['erase',file]:
                    os.remove("H\\Apps\\"+name+'/'+file)
        with open("H\\Apps\\"+name+'\\VERSION.json',"wb") as f:
            f.write(self.loader.load_an_object(name+'/VERSION.json'))
        self.btns[name]["Update"].config(state="disabled")
    
    def exit(self):
        if not self.changed:
            self.destroy()
            return
        
        rep= messagebox.askyesno("Launch again ?","You downloaded/updated some apps, and these changes won't be applied until you relaunch the programm.\nDo you want to relaunch the program ?")
        if rep:
            self.destroy()
            self.master.launchagain=(True,'admin','@dmin')
        else:
            self.destroy()



    def relaunch(self):
        raise launcherror.LaunchAgain