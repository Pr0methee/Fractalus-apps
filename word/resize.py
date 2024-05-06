from __future__ import annotations
from PIL import Image

def resize(size_:int|float,dim:int,open_file:str,save_file:str):
    """
    Modifie la taille d'une image en respectant les proportions.
    
    size_:int|float -> taille souhaitée pour la dimension {dim}
    dim:int -> dimension de l'image qui doit être à {size_} pixel. vaut 0 (largeur) ou 1 (hauteur)
    open_file:str -> lien de fichier de départ
    save_file:str -> celui d'arrivée
    """
    img = Image.open(open_file)
    first_size=img.size

    k = size_/first_size[dim]

    size = (k*arg for arg in first_size)

    img.thumbnail(size, Image.ANTIALIAS)
    img.save(save_file, "PNG")