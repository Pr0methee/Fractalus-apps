import sqlalchemy

def ouvrir_connexion(user,passwd,database,host="127.0.0.1"):
    """ 
    ouverture d'une connexion MySQL 
    paramètres: 
    user (str) le login MySQL de l'utilsateur
    passwd (str) le mot de passe MySQL de l'utilisateur 
    host (str) le nom ou l'adresse IP de la machine hébergeant le serveur MySQL  database (str) le nom de la base de données à utiliser 
    résultat: l'objet qui gère le connection MySQL si tout s'est bien passé 
    """ 
    try: 
        #creation de l'objet gérant les interactions avec le serveur de BD 
        engine=sqlalchemy.create_engine('mysql+mysqlconnector://'+user+':'+passwd+'@'+host+'/'+database)  #creation de la connexion 
        cnx = engine.connect() 
    except Exception as err: 
        print(err) 
        raise err 
    print("connexion réussie") 
    return cnx 

def use_cursor_as_str(cursor:sqlalchemy.engine.cursor.LegacyCursorResult):
    """Résultat d'une requette sql passé dans un str"""
    r = ''
    try:
        for each in cursor:
            r+=str(each)
    except:
        r = 'R.A.S.'
    return r