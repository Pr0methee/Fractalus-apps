from __future__ import annotations
from PIL import Image

from typing import SupportsFloat

def resize(size_:SupportsFloat,dim:int,open_file:str,save_file:str):
    """
    Modifie la taille d'une image en respectant les proportions.
    O
    size_:int|float -> taille souhaitée pour la dimension {dim}
    dim:int -> dimension de l'image qui doit être à {size_} pixel. vaut 0 (largeur) ou 1 (hauteur) ou 'g' greatest
    open_file:str -> lien de fichier de départ
    save_file:str -> celui d'arrivée
    """
    img = Image.open(open_file)
    first_size=img.size
    if dim == 'g':
        if first_size[0]>first_size[1]:
            dim=0
        else:
            dim=1


    k = size_/first_size[dim]

    size = tuple(int(k*arg) for arg in first_size)

    img = img.resize(size,Image.LANCZOS)
    img.save(save_file, "PNG")

def cached_resize(size_:int|float,dim:int,open_file:str):
    """
    Modifie la taille d'une image en respectant les proportions.
    O
    size_:int|float -> taille souhaitée pour la dimension {dim}
    dim:int -> dimension de l'image qui doit être à {size_} pixel. vaut 0 (largeur) ou 1 (hauteur) ou 'g' greatest
    open_file:str -> lien de fichier de départ
    -> renvoie l'image mise a l'échelle sans sauvegarder
    """
    img = Image.open(open_file)
    first_size=img.size
    if dim == 'g':
        if first_size[0]>first_size[1]:
            dim=0
        else:
            dim=1


    k = size_/first_size[dim]

    size = tuple(int(k*arg) for arg in first_size)

    return img.resize(size,Image.LANCZOS)
