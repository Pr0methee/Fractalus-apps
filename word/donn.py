class Pile:
    def __init__(self):
        """Crée une pile"""
        self.__l = []
    
    def empiler(self,elt):
        self.__l.append(elt)

    def depiler(self):
        return self.__l.pop()
    
    def Taille(self):
        return len(self.__l)
    
    def Vide(self):
        return self.__l == []

class File:
    def __init__(self):
        """Crée une file"""
        self.__l = []
    
    def emfiler(self,elt):
        self.__l.append(elt)

    def defiler(self):
        return self.__l.pop(0)
    
    def Taille(self):
        return len(self.__l)    
        
    def Vide(self):
        return self.__l == []

class TextIndex:
    def __init__(self):
        """Gère les index dans un widget text"""
        self.ind= '1.0'
    
    def add(self,l):
        if l=='\n':
            d,f = self.ind.split('.')
            d = str(int(d)+1)
            f='0'
            self.ind = d+'.'+f
        else:
            d,f = self.ind.split('.')
            f=str(int(f)+1)
            self.ind = d+'.'+f
    
    def get(self):
        return self.ind