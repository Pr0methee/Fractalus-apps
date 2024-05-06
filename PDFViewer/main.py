from tkinter import *
import shutil,pdf2image,os
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog, H.Apps.PDFViewer.resize as resize
#import resize

FILES = [
    ("PDF",'.pdf')
]

class PDFViewer(Toplevel):
    def __init__(self,parent:Tk,open_proc = lambda files,master: filedialog.askopenfilename(filetypes=files,parent=master),file=''):
        """Affiche le pdf"""
        super().__init__(parent)

        self.open_proc = open_proc

        self.transient(parent)

        self.title("PDF Viewer")

        self.f1=Frame(self)
        self.f1.grid(row=0,column=0,sticky=NSEW)

        self.open=Button(self.f1,text='Ouvrir',command=self.open_file)
        self.open.pack(side=LEFT)

        ttk.Separator(self,orient=HORIZONTAL).grid(row=1,column=0,sticky=NSEW)
        
        
        self.f2=Frame(self)
        self.f2.grid(row=2,column=0,sticky=NSEW)

        self.can=Canvas(self.f2)
        self.can.pack(side=LEFT)        
        self.can['height']=750
        self.can['width']=530

        self.img=[]

        self.scrollbar = ttk.Scrollbar(self.f2, orient=VERTICAL, command=self.can.yview)
        self.can.configure(yscrollcommand=self.scrollbar.set)
        self.can.config(scrollregion=self.can.bbox("all"))
        self.scrollbar.pack(expand=True,fill='y',side='right')

        self.resizable(0,0)

        if file != '':
            self.show(file)
        
        self.update()
        self.update_idletasks()
        self.can.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        self.can.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def open_file(self):
        op = self.open_proc(FILES,self)#filedialog.askopenfilename(filetypes=[("PDF",'.pdf')],parent=self)
        print(op,type(op))
        if not op == '':
            self.show(op)
    
    def show(self,file):
        pages = pdf2image.convert_from_path(file)
        try:
            os.mkdir('H\\cache\\binPDFViewer')
        except:
            pass

        for i in range(len(pages)):#crée dans le fichier bin une image de chaque page du pdf pour les afficher dans un Canvas
            pages[i].save(r'H\cache\binPDFViewer\page'+ str(i) +'.png', 'PNG')
            resize.resize(750,1,r'H\cache\binPDFViewer\page'+ str(i) +'.png',r'H\cache\binPDFViewer\page'+ str(i) +'.png')
        
        self.can.delete('all')
        self.img=[]

        self.img=[PhotoImage(file=fr"H\cache\binPDFViewer\page{i}.png",master=self) for i in range(len(pages))]
        for i in range(len(pages)):
            self.can.create_image(530//2,750//2+765*i,image=self.img[i])

        self.can.configure(yscrollcommand=self.scrollbar.set)
        self.can.config(scrollregion=self.can.bbox("all"))

        shutil.rmtree('H\cache\\binPDFViewer')



if __name__ == '__main__':
    root=Tk()
    PDFViewer(root)
    root.mainloop()