import H.Apps.word.donn as donn

def well_parent(text:str):
    """Verifie qu'il y a le bon nombre de () dans text"""
    p = donn.Pile()
    for letter in text:
        if letter == '(':
            p.empiler('(')
        elif letter == ')':
            if p.Vide():
                return False
            else:
                p.depiler()
    return p.Vide()

def well(text:str,b_car,e_car):
    """Verifie qu'il y a autant de b_car que de e_car (dans le bon ordre) dans text"""
    p=donn.Pile()
    for letter in text:
        if letter == b_car:
            p.empiler(b_car)
        elif letter == e_car:
            if p.Vide():
                return False
            else:
                p.depiler()
    return p.Vide()

def well_dollar(text:str):
    """Verifie une expression latex"""
    p = donn.Pile()
    for letter in text:
        if letter == '$':
            if p.Vide():
                p.empiler('$')
            else:
                p.depiler()
    return p.Vide()

def well_quoted(text:str):
    simple = donn.Pile()
    double = donn.Pile()
    tripled = donn.Pile()
    triples = donn.Pile()
    preantislash =False
    i=0
    while i <len(text):
        letter =text[i]

        if not simple.Vide():
            if letter =='\n' and not preantislash:
                return False
            elif letter == "'":
                simple.depiler()
        elif not double.Vide():
            if letter =='\n' and not preantislash:
                return False
            elif letter == '"':
                double.depiler()
        elif not tripled.Vide():
            if text[i-2:i+1] =='"""':
                tripled.depiler()
        elif not triples.Vide():
            if text[i-2:i+1] =="'''":
                triples.depiler()
        else:#Pas encore entré dans un str
            if letter == "'":
                if i >= len(text)-3:
                    simple.empiler("'")
                else:
                    if text[i:i+3] =="'''":
                        tripled.empiler("'''")
                        i+=2
                        print(i)
                    else:
                        double.empiler("'")
            elif letter =='"':
                if i >= len(text)-3:
                    double.empiler('"')
                else:
                    if text[i:i+3] =='"""':
                        tripled.empiler('"""')
                        i+=2
                        print(i)
                    else:
                        double.empiler('"')

        #verifie la présence de \ pour renvoie à la ligne
        if letter == '\\':
            preantislash=True
        else:
            preantislash=False
        i+=1

    return simple.Vide() and double.Vide() and tripled.Vide() and triples.Vide()