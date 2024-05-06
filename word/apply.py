from __future__ import annotations
from tkinter import *

import H.Apps.word.get_index as get_index,os, H.Apps.word.style as style

class PyFontApplier:
    def __init__(self,text:Text):
        """Applicateur de style pour les mots se référant à Python"""
        self.text=text

        self.strstyle = style.Style.from_txt("H/cache/word/String Python.txt")
        self.strstyle.text=self.text
        self.strstyle.tag_create()
        self.comstyle = style.Style.from_txt("H/cache/word/Commentaires Python.txt")
        self.comstyle.text=self.text
        self.comstyle.tag_create()
        self.funcstyle = style.Style.from_txt("H/cache/word/Fonctions Python.txt")
        self.funcstyle.text=self.text
        self.funcstyle.tag_create()
        self.modstyle = style.Style.from_txt("H/cache/word/Modules Python.txt")
        self.modstyle.text=self.text
        self.modstyle.tag_create()
        self.kwstyle = style.Style.from_txt("H/cache/word/Mots-Clés Python.txt")
        self.kwstyle.text=self.text
        self.kwstyle.tag_create()
        self.builtstyle = style.Style.from_txt("H/cache/word/Built-In Python.txt")
        self.builtstyle.text=self.text
        self.builtstyle.tag_create()
        self.errstyle = style.Style.from_txt("H/cache/word/Erreurs Python.txt")
        self.errstyle.text=self.text
        self.errstyle.tag_create()
    
    def apply(self):
        """Appliquer le style dans le Text widget"""
        for pos_len  in get_index.find_built(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.builtstyle.tag_add(pos_len[0],fin)
        
        for pos_len  in get_index.find_err(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.errstyle.tag_add(pos_len[0],fin)
        
        for pos_len  in get_index.find_func(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.funcstyle.tag_add(pos_len[0],fin)

        for pos_len  in get_index.find_kw(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.kwstyle.tag_add(pos_len[0],fin)
        
        for pos_len  in get_index.find_mod(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.modstyle.tag_add(pos_len[0],fin)

        self.comstyle.tag_remove()
        for pos_couple in get_index.index_commentaire(self.text.get('0.0','end')):
            self.comstyle.tag_add(pos_couple[0],pos_couple[1])
        
        self.strstyle.tag_remove()
        for pos_couple in get_index.index_str(self.text.get('0.0','end')):
            self.strstyle.tag_add(pos_couple[0],pos_couple[1])
    
    def remove_all(self):
        """Enlever tous les styles"""
        self.builtstyle.tag_remove()
        self.comstyle.tag_remove()
        self.errstyle.tag_remove()
        self.funcstyle.tag_remove()
        self.kwstyle.tag_remove()
        self.modstyle.tag_remove()
        self.strstyle.tag_remove()

class SQLFontApplier:
    def __init__(self,text:Text):
        """Applicateur de style SQL"""
        self.text=text
        self.text.tag_configure("sqlkw",foreground='#000080')
        self.sqlstyle =style.Style.from_txt("H/cache/word/Mots-Clés SQL.txt")
        self.sqlstyle.text=self.text
        self.sqlstyle.tag_create()
    
    def apply(self):
        """Tout appliquer"""
        for pos_len in get_index.find_sqlkw(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.sqlstyle.tag_add(pos_len[0],fin)
    
    def remove_all(self):
        """Tout retirer"""
        self.sqlstyle.tag_remove()

class LatexFontApplier:
    def __init__(self,text:Text):
        """Applicateur de style LaTeX"""
        self.text=text

        self.latexstyle = style.Style.from_txt("H/cache/word/Mots-Clés LaTeX.txt")
        self.latexstyle.text=self.text
        self.latexstyle.tag_create()
        self.mathstyle = style.Style.from_txt("H/cache/word/Math Mode LaTeX.txt")
        self.mathstyle.text=self.text
        self.mathstyle.tag_create()
        self.crochetstyle = style.Style.from_txt("H/cache/word/Math Mode 2 LaTeX.txt")
        self.crochetstyle.text=self.text
        self.crochetstyle.tag_create()
        self.comstyle = style.Style.from_txt("H/cache/word/Commentaires LaTeX.txt")
        self.comstyle.text=self.text
        self.comstyle.tag_create()
    
    def apply(self):
        """Tout appliquer"""
        indexes = get_index.index_crochetmode(self.text.get('0.0','end'))
        
        l = [(indexes[2*i],indexes[2*i+1]) for i in range(len(indexes)//2)]

        for tup in l:
            self.crochetstyle.tag_add(tup[0].split('.')[0]+'.'+str(int(tup[0].split('.')[1])-1),tup[1].split('.')[0]+'.'+str(int(tup[1].split('.')[1])+1))
        
        for com in get_index.latex_com(self.text.get('0.0','end')):
            self.comstyle.tag_add(com[0],com[1])

        for pos_len in get_index.find_latex(self.text.get('0.0','end')):
            fin = pos_len[0]
            fin = fin.split('.')[0] + '.'+ str(int(fin.split('.')[1])+pos_len[1])
            self.latexstyle.tag_add(pos_len[0],fin)
        
        for indexes in get_index.index_mathmode(self.text.get('0.0','end')):
            self.mathstyle.tag_add(indexes[0],indexes[1])
    
    def remove_all(self):
        """Tout retirer"""
        self.comstyle.tag_remove()
        self.crochetstyle.tag_remove()
        self.latexstyle.tag_remove()
        self.mathstyle.tag_remove()
            
class Applier:
    def __init__(self,text:Text):
        """Permet d'appliquer tous les styles dans le widget Text"""
        self.text=text
        self.pyapplier=PyFontApplier(text)
        self.sqlapplier = SQLFontApplier(text)
        self.latexapplier = LatexFontApplier(text)

        self.styles = style.StyleGestion()
        self.styles.add("String Python",self.pyapplier.strstyle)
        self.styles.add("Fonctions Python",self.pyapplier.funcstyle)
        self.styles.add("Modules Python",self.pyapplier.modstyle)
        self.styles.add("Mots-Clés Python",self.pyapplier.kwstyle)
        self.styles.add("Built-In Python",self.pyapplier.builtstyle)
        self.styles.add("Erreurs Python",self.pyapplier.errstyle)
        self.styles.add("Commentaires Python",self.pyapplier.comstyle)

        self.styles.add("Mots-Clés SQL",self.sqlapplier.sqlstyle)

        self.styles.add('Mots-Clés LaTeX',self.latexapplier.latexstyle)
        self.styles.add('Math Mode LaTeX',self.latexapplier.mathstyle)
        self.styles.add('Math Mode 2 LaTeX',self.latexapplier.crochetstyle)

    
    def update(self,cur):
        """Vérifier ce qui doit être appliquer"""
        self.remove()
        if os.path.splitext(cur)[1] in ('.py','.pyw'):
            self.pyapplier.apply()
        elif os.path.splitext(cur)[1] in ('.sql',):
            self.sqlapplier.apply()
        elif os.path.splitext(cur)[1] in ('.tex',):
            self.latexapplier.apply()
    
    def change(self):
        """Tout effacer"""
        self.pyapplier.remove_all()
        self.sqlapplier.remove_all()
        self.latexapplier.remove_all()
    
    def remove(self):
        for tag in ['sqlkw','str','func','mod','builtin','kw','err','latex']:
            self.text.tag_remove(tag,'0.0','end')