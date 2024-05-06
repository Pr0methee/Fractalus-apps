from __future__ import annotations
import H.Apps.word.donn as donn,sys

#CONSTANTES
ERRORS =['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError']
BUILTIN = ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__']
MODULES = sys.modules.keys()
KEYWORDS = ['and','as','assert','break','class','continue','def','del','elif','else','except','finally','for','from','global','if','in','import','is','lambda','not','or','pass','raise','return','try','while','with','yield']
FUNC = ['__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
with open("H/cache/word/kwsql.txt","r") as f:
    SQLKW = f.read().split(',')

#L'ensemble des méthodes (sauf exceptions signalées) renvoient une liste de liste 
# les find_... renvoie l'index de début suivit de la longueur de l'elt 
# les index_... renvoie l'index de début et celui de fin.

def index_str(text:str)->list:
    """
    Renvoie une liste de liste
    chaque sous-liste contient 2 éléments:
    l'index de début de str et l'index de fin de str
    """
    simple = donn.Pile()
    double = donn.Pile()
    tripled = donn.Pile()#str dans """ """
    triples = donn.Pile()#str dans ''' '''

    preantislash =False
    comment=False
    ind = donn.TextIndex()
    i=0
    l=[]
    while i <len(text):
        letter =text[i]
        

        if not simple.Vide() or not double.Vide():
            ind.add(letter)
            if (letter =='\n' and not preantislash) or (letter == "'" and not preantislash) or (letter == '"' and not preantislash):
                try:
                    simple.depiler()
                except:
                    double.depiler()
                l[-1].append(ind.get())

        elif not tripled.Vide():
            ind.add(letter)
            if text[i-2:i+1] =='"""':
                tripled.depiler()
                l[-1].append(ind.get())
        elif not triples.Vide():
            ind.add(letter)
            if text[i-2:i+1] =="'''":
                ind.add('a')
                ind.add('a')
                triples.depiler()
                l[-1].append(ind.get())
            
            
        else:#Pas encore entré dans un str
            if comment ==False:
                if letter == "'":
                    if i >= len(text)-3:
                        simple.empiler("'")
                        l.append([ind.get()])
                    else:
                        if text[i:i+3] =="'''":
                            triples.empiler("'''")
                            l.append([ind.get()])
                            i+=2
                        else:
                            simple.empiler('"')
                            l.append([ind.get()])
                elif letter =='"':
                    if i >= len(text)-3:
                        double.empiler('"')
                        l.append([ind.get()])
                    else:
                        if text[i:i+3] =='"""':
                            tripled.empiler('"""')
                            l.append([ind.get()])
                            i+=2
                        else:
                            double.empiler('"')
                            l.append([ind.get()])
                elif letter=='#':
                    comment=True
            else:
                if letter=='\n':
                    comment=False
            ind.add(letter)
            

        #verifie la présence de \ pour renvoie à la ligne ou passer un " ou un '
        if letter == '\\':
            preantislash=True
        else:
            preantislash=False
        i+=1
        
    if len(l)>0:
        if len(l[-1])==1:
            l[-1].append(ind.get())
    return l

def index_commentaire(text:str)->list:
    """
    Renvoie une liste de liste
    chaque sous-liste contient 2 éléments:
    l'index de début de commentaire et l'index de fin de commentaire
    """
    simple = donn.Pile()
    double = donn.Pile()
    tripled = donn.Pile()#str dans """ """
    triples = donn.Pile()#str dans ''' '''

    preantislash =False
    comment=False
    ind = donn.TextIndex()
    i=0
    l=[]
    while i <len(text):
        letter =text[i]
        
        if not simple.Vide() or not double.Vide():
            ind.add(letter)
            if (letter =='\n' and not preantislash) or (letter == "'" and not preantislash) or (letter == '"' and not preantislash):
                try:
                    simple.depiler()
                except:
                    double.depiler()
        elif not tripled.Vide():
            ind.add(letter)
            if text[i-2:i+1] =='"""':
                tripled.depiler()
        elif not triples.Vide():
            ind.add(letter)
            if text[i-2:i+1] =="'''":
                ind.add('a')
                ind.add('a')
                triples.depiler()
            
            
        else:#Pas encore entré dans un str
            if comment ==False:
                if letter == "'":
                    if i >= len(text)-3:
                        simple.empiler("'")
                    else:
                        if text[i:i+3] =="'''":
                            triples.empiler("'''")
                            i+=2
                        else:
                            simple.empiler('"')
                elif letter =='"':
                    if i >= len(text)-3:
                        double.empiler('"')
                    else:
                        if text[i:i+3] =='"""':
                            tripled.empiler('"""')
                            i+=2
                        else:
                            double.empiler('"')
                elif letter=='#':
                    l.append([ind.get()])
                    comment=True
            else:
                if letter=='\n':
                    ind.add(letter)
                    l[-1].append(ind.get())
                    comment=False
            ind.add(letter)
            

        #verifie la présence de \ pour renvoie à la ligne ou passer un " ou un '
        if letter == '\\':
            preantislash=True
        else:
            preantislash=False
        i+=1
        
    if len(l)>0:
        if len(l[-1])==1:
            l[-1].append(ind.get())
    return l


def letter_index(text:str)->list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément du tuple est une lettre, 
    Le 2nd l'index de cette lettre
    """
    ind=donn.TextIndex()
    d= []
    for l in text:
        d.append((l,ind.get()))
        ind.add(l)
    return d

def cut_with_index(text:str)-> list:
    """
    Renvoie une liste de tuple
    le 1er élément du tuple est un mot
    le 2nd l'index du mot
    """
    l = letter_index(text)
    return_list = []
    mot =''
    i=''
    for couple in l:
        if couple[0] in ' \t\n':
            if mot != '':
                return_list.append((mot,i))
            mot = ''
        else:
            if mot == '':
                i=couple[1]
            mot+=couple[0]
    return return_list

def find_sqlkw(text:str)-> list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément est l'index du 1er caractère du mot clé sql
    Le 2nd la longueur du mot clé sql.
    """ 
    l =cut_with_index(text)
    return_list=[]
    for couple in l:
        if couple[0].upper() in SQLKW:
            return_list.append((couple[1],len(couple[0])))
    return return_list

def find_latex(text:str):
    """Renvoie une liste de liste : index debut, longueur du mot-clé latex"""
    l =cut_with_index(text)
    return_list=[]
    for couple in l:
        try:
            mot =couple[0].split('{')[0].split('[')[0].split(']')[0]
            if mot[0] == '\\' and len(mot)!=1 and mot !='\\\\' and mot != '\\':
                return_list.append((couple[1],len( couple[0].split('{')[0].split('[')[0])))
        except:
            pass
    return return_list

def find_func(text:str)-> list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément est l'index du 1er caractère du nom de la fct
    Le 2nd la longueur du nom de la fct.
    """  
    l = cut_with_index(text)
    return_list = []
    for couple in l:
        if couple[0].split('(')[0] in FUNC:
            return_list.append((couple[1],len(couple[0].split('(')[0])))
    return return_list

def find_mod(text:str)-> list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément est l'index du 1er caractère du nom du module
    Le 2nd la longueur du nom du module.
    """  
    l = cut_with_index(text)
    return_list = []
    for couple in l:
        if couple[0].split('.')[0] in MODULES:
            return_list.append((couple[1],len(couple[0].split('.')[0])))
    return return_list

def find_err(text:str)-> list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément est l'index du 1er caractère du nom de l'erreur
    Le 2nd la longueur du nom de l'erreur.
    """  
    l = cut_with_index(text)
    return_list = []
    for couple in l:
        if couple[0].split('(')[0] in ERRORS:
            return_list.append((couple[1],len(couple[0].split('(')[0])))
    return return_list

def find_built(text:str)-> list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément est l'index du 1er caractère du nom du built-in
    Le 2nd la longueur du nom du built-in.
    """  
    l = cut_with_index(text)
    return_list = []
    for couple in l:
        if couple[0].split('(')[0].split('.')[0] in BUILTIN:
            return_list.append((couple[1],len(couple[0].split('(')[0].split('.')[0])))
    return return_list

def find_kw(text:str)-> list[tuple[str,str]]:
    """
    Renvoie une liste de tuple
    Le 1er élément est l'index du 1er caractère du nom du mot clé
    Le 2nd la longueur du nom du mot clé.
    """  
    l = cut_with_index(text)
    return_list = []
    for couple in l:
        if couple[0].split(':')[0] in KEYWORDS:
            return_list.append((couple[1],len(couple[0].split(':')[0])))
    return return_list

def index_mathmode(text:str):
    """Index des éléments dans un mathmode délimité par $ $ (latex)"""
    l=letter_index(text)
    return_list=[]
    comment=False
    d=False
    for letter_indexes in l:
        if letter_indexes[0] == '$' and comment==False:
            if d:
                return_list[-1].append(letter_indexes[1].split('.')[0]+'.'+str(int(letter_indexes[1].split('.')[1])+1))
                d=False
            else:
                return_list.append([letter_indexes[1]])
                d=True

        if d == False:
            if letter_indexes[0]=='%':
                comment=True
            if comment and letter_indexes[0]=='\n':
                comment=False
    
    if len(return_list)!=0:
        if len(return_list[-1])==1:
            return_list[-1].append(l[-1][1])

    return return_list

def index_crochetmode(text:str):
    """Index des éléments en mathmode délémité par \[ \] (latex) """
    l=letter_index(text)
    return_list=[]
    d=False#début ? 
    q=False#on se demande si il faut commencer/finir

    comment=False

    for letter_indexes in l:     
        if comment==False:  
            if q and letter_indexes[0] == '[' and not d:
                d=True
                return_list.append(letter_indexes[1])

            if q and d:
                if letter_indexes[0] == ']':
                    return_list.append(letter_indexes[1])
                    d=False

            if letter_indexes[0] == '\\' and d:
                q=True
            elif letter_indexes[0]=='\\':
                q=True
            else:
                q=False
            if letter_indexes[0] == '%' and not d:
                comment=True

        if comment and letter_indexes[0]=='\n':
            comment=False
    
    if len(return_list)%2!=0:
        return_list.append(l[-1][1])

    return return_list


def latex_com(text:str):
    crochetmode=False
    q=False#on se demande si il faut commencer/finir
    mathmode=False
    comment=False
    return_list=[]
    l=letter_index(text)
    for letter_indexes in l:
        if letter_indexes[0] == '$' and comment==False:
            if mathmode:mathmode=False
            else:mathmode=True


        if comment==False:  
            if q and letter_indexes[0] == '[' and not crochetmode:
                crochetmode=True
            if q and crochetmode:
                if letter_indexes[0] == ']':
                    crochetmode=False

            if letter_indexes[0] == '\\' and crochetmode:
                q=True
            elif letter_indexes[0]=='\\':
                q=True
            else:
                q=False
        
        if mathmode ==False and crochetmode ==False:
            if letter_indexes[0]=='%':
                comment=True
                return_list.append([letter_indexes[1]])
            elif comment and letter_indexes[0]=='\n':
                return_list[-1].append(letter_indexes[1])
                comment=False
    
    if len(return_list)!=0:
        if len(return_list[-1])==1:
            return_list.append(l[-1][1])
    return return_list