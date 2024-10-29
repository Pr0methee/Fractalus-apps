import sqlite3,os

def connect(id,mdp):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("SELECT * FROM profils ")
    for elt in cur:
        if elt == (id,mdp):
            cur.close()
            conn.close()
            return True

    cur.close()
    conn.close()
    return False

def get_profils():
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("SELECT * FROM profils")
    result=list(cur)
    cur.close()
    conn.close()

    return result

def good_admin_psw(psw):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("SELECT * FROM profils WHERE id='admin' AND mdp='%s'"%(psw))
    result=list(cur)
    cur.close()
    conn.close()

    return result!=[]

def get_psw(id):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("SELECT mdp FROM profils WHERE id='%s'"%(id))
    result=list(cur)
    cur.close()
    conn.close()

    return result

def delete_profil(id):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("DELETE FROM profils WHERE id='%s'"%(id))
    cur.execute("DELETE FROM preferances WHERE user='%s'"%(id))

    os.rmdir('H/Users/'+id)

    conn.commit()
    
    cur.close()
    conn.close()


def change_psw(id,mdp):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("UPDATE profils SET mdp='%s' WHERE id='%s'"%(mdp,id))

    conn.commit()

    cur.close()
    conn.close()

def create_profil(id,mdp):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()
    #verifier que l'utilisateur n'existe pas !

    cur.execute("SELECT * FROM profils WHERE id='%s'"%(id))
    if any(car in id for car in '.!:/;,?§<>"\\|*'):
        return 'Erreur, caractère interdit utilisé dans le nom d\'utilisateur.\nPour rappel, il s\'agit des caractères : .!:/;,?§<>"\\|*'
    if list(cur) != []:
        return 'Erreur, impossible de recréer'

    cur.execute("INSERT INTO profils VALUES ('%s','%s')"%(id,mdp))
    cur.execute("""INSERT INTO preferances VALUES ('%s',
    'fond4.jpg',
    'Style("#9bcdff","","TkFixedFont")',
    'Style("#74886b","","TkFixedFont")',
    'Style("#6a8a35","","TkFixedFont")',
    'Style("#c3063c","","TkFixedFont")',
    'Style("#900090","","TkFixedFont")',
    'Style("#af0850","","TkFixedFont")',
    'Style("#00c800","","TkFixedFont")',
    'Style("#3fb591","","TkFixedFont")',
    'Style("#0000ff","","TkFixedFont")',
    'Style("#9579c0","","TkFixedFont")',
    'Style("#000080","","TkFixedFont")',
    'Style("#008000","","TkFixedFont")'
    )"""%(id))
    conn.commit()

    cur.close()
    conn.close()

    os.mkdir('H/Users/'+id)
    return 'OK'

def get_preferances(id):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("SELECT * FROM preferances WHERE user='%s'"%(id))
    result=tuple(cur)
    cur.close()
    conn.close()

    return result

def change_bg(id,bg):
    change_in_pref(id,'bg',bg)

def change_in_pref(id,col,arg):
    conn =sqlite3.connect('H/cache/profils.sq3')
    cur=conn.cursor()

    cur.execute("UPDATE preferances SET %s='%s' WHERE user='%s'"%(col,arg,id))

    conn.commit()

    cur.close()
    conn.close()