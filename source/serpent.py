# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module serpent.py
    Ce module implémente l'API permettant de gérer les informations des joueurs (idenfier à leur serpent)
"""
import arene

def Serpent(nom_joueur:str, num_joueur:int,points:int=0,positions:list=None,tps_s:int=0,tps_p:int=0,tps_m:int=0,direction:str='N')->dict:
    """Créer un joueur avec toutes les informations le concernant.

    Args:
        nom_joueur (str): nom du joueur
        num_joueur (int): numero du joueur
        points (int, optional): nombre de points attribués au joueur. Defaults to 0.
        positions (list, optional): la liste des positions occupées par le serpent sur l'arène. Defaults to None.
        tps_s (int, optional): temps restant pour le bonus surpuissance. Defaults to 0.
        tps_p (int, optional): temps restant pour le bonus protection. Defaults to 0.
        tps_m (int, optional): temps restant pour le bonus mange-mur. Defaults to 0.
        direction (str, optional): dernière direction prise par le serpent. Defaults to 'N'.

    Returns:
        dict: une dictionnaire contenant les informations du serpent
    """   
    dico_info = {'nom_j': nom_joueur, 'num_j': num_joueur,'points':points, 'positions':positions, 'tps_surpuissance':tps_s, 'tps_protection':tps_p, 'tps_mange_mur':tps_m, 'direction':direction}
    return dico_info

def get_nom(serpent:dict)->str:
    """retourne le nom du joueur associé au serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: le nom du joueur associé à ce serpent
    """ 
    return serpent['nom_j']

def get_num_joueur(serpent:dict)->int:
    """retourne le numéro du joueur associé au serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le numéro du joueur associé à ce serpent
    """   
    return serpent['num_j']

def get_points(serpent:dict)->int:
    """retourne le nombre de points du joueur associé au serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de points du joueur associé à ce serpent
    """   
    return serpent['points']

def get_liste_pos(serpent:dict)->list:
    """retourne la liste des positions occupées par le serpent sur l'arène. La première position étant la tête du serpent

    Args:
        serpent (dict): le serpent considéré

    Returns:
        list: la liste des positions occupées par le serpent
    """    
    return serpent['positions']

def get_queue(serpent:dict) -> [int,int]:
    """retourne la position (lig,col) de la queue du serpent dans l'arène

    Args:
        serpent (dict): le serpent considéré

    Returns:
        [int,int]: la position lig,col du la queue du serpent
    """    

    return serpent['positions'][-1]

def get_derniere_direction(serpent:dict)->str:
    """retourne la dernière direction choisie par le joueur pour se déplacer

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: un des caractère N S E O
    """    
    return serpent['direction']

def get_bonus(serpent:dict)->list:
    """retourne une liste contenant les bonus obtenus par le joueur
        c'est-à-dire ceux pour lesquels le temps restant est supérieur à 0

    Args:
        serpent (dict): le serpent considéré

    Returns:
        list: la liste des bonus du joueur
    """    
    lst_final = []
    if serpent['tps_surpuissance'] > 0 :
        lst_final.append(-3)

    if serpent['tps_mange_mur'] > 0 :
        lst_final.append(-4)

    if serpent['tps_protection'] > 0 :
        lst_final.append(-5)
    return lst_final            



def ajouter_points(serpent:dict,nb_points:int):
    """ajoute (ou enlève) des points à un serpent

    Args:
        serpent (dict): le serpent considéré
        nb_points (int): le nombre de points à ajouter (si négatif enlève des points)
    """    
    serpent['points'] += nb_points

def set_liste_pos(serpent:dict, tete:list):
    """initialise la liste des positionsd'un serpent

    Args:
        serpent (dict): le serpent considéré
        tete (list): la liste des positions occupées par ce serpent
    """    
    serpent['positions'] = tete

def set_derniere_direction(serpent:dict, direction:str):
    """Met à jout la dernière direction utilisée par le serpent (utile pour l'affichage)

    Args:
        serpent (dict): le serpent considéré
        direction (str): un des caractère N S E O
    """    
    if direction in {'N', 'S', 'E', 'O'}:
        serpent['direction'] = direction

def to_str(serpent:dict)->str:
    """produit une chaine de caractères contenant les informations principales d'un serpent sour la forme
    Joueur 1 -> 143 s:0 m:4 p:0
    où Joueur 1 est le nom du joueur, après la flèche se trouve le nombre de point
    puis le temps restant de chaque bonus (supuissante, mange mur et protection)

    Args:
        serpent (dict): le serpent considéré

    Returns:
        str: la chaine de caractères donnant les informations principales d'un serpent 
    """    
    return serpent['nom_j'] + ' ' + str(serpent['num_j']) + ' -> ' + str(serpent['points']) + ' s:' + str(serpent['tps_surpuissance']) + ' m:' + str(serpent['tps_mange_mur']) + ' p:' + str(serpent['tps_protection'])

def get_temps_protection(serpent:dict)->int:
    """indique le temps restant pour le bonus protection

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """    
    return serpent['tps_protection']

def get_temps_mange_mur(serpent:dict)->int:
    """indique le temps restant pour le bonus mange mur

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """
    return serpent['tps_mange_mur']

def get_temps_surpuissance(serpent:dict)->int:
    """indique le temps restant pour le bonus surpuissance

    Args:
        serpent (dict): le serpent considéré

    Returns:
        int: le nombre de tours restant pour ce bonus
    """   
    return serpent['tps_surpuissance']

def ajouter_temps_protection(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus protection

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent['tps_protection'] += temps
    return serpent['tps_protection']

def ajouter_temps_mange_mur(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus mange mur

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent['tps_mange_mur'] += temps
    return serpent['tps_mange_mur']

def ajouter_temps_surpuissance(serpent:dict, temps:int)->int:
    """ajoute du temps supplémentaire pour le bonus surpuissance

    Args:
        serpent (dict): le serpent considéré
        temps (int): le nombre de tours à ajouter

    Returns:
        int: le nombre de tours total restant pour ce bonus
    """    
    serpent['tps_surpuissance'] += temps
    return serpent['tps_surpuissance']

def maj_temps(serpent:dict):
    """Décrémente les temps restant pour les bonus de ce serpent
    Attention les temps ne peuvent pas être négatif

    Args:
        serpent (dict): le serpent considéré
    """    
    if serpent['tps_surpuissance']>0:
         serpent['tps_surpuissance'] -= 1
    if serpent['tps_protection']>0:
         serpent['tps_protection'] -= 1
    if serpent['tps_mange_mur']>0:
         serpent['tps_mange_mur'] -= 1

def serpent_2_str(serpent:dict, sep=";")->str:
    """Sérialise un serpent sous la forme d'une chaine de caractères
    contenant 2 lignes.
    nom_j;num_j;nb_point;tps_surpuissance;tps_mange_mur;tps_protection
    lig1;col1;lig2;col2;...
    La première ligne donne les informations autres que la liste des positions du serpent
    la deuxième ligne donné la liste des position du serpent en commençant par la tête
    Args:
        serpent (dict): le serpent considéré
        sep (str, optional): le caractère séparant les informations du serpent. Defaults to ";".

    Returns:
        str: la chaine de caractères contenant les toutes informations du serpent
    """   
    positions = ""
    for pos in serpent['positions']:
        positions = positions + str(pos[0]) + sep + str(pos[1]) + sep
    info_serpent = serpent['nom_j'] + sep + str(serpent['num_j']) + sep + str(serpent['points']) + sep + str(serpent['tps_surpuissance']) + sep + str(serpent['tps_mange_mur']) + sep + str(serpent['tps_protection']) + sep + str(serpent['direction']) + "\n" + positions 
    return info_serpent[:-1] + '\n'



def serpent_from_str(la_chaine, sep=";")->dict:
    """Reconstruit un serpent à partir d'une chaine de caractères
       telle que celle produite par la fonction précédente

    Args:
        la_chaine (_type_): la chaine de caractères contenant les informations du serpent
        sep (str, optional): le caractère servant à séparer les informations du serpent. Defaults to ";".

    Returns:
        dict: Le serpent représenté dans la chaine de caractères
    """    
    lst_cle = [('nom_j', str), ('num_j', int), ('points', int), ('tps_surpuissance', int), ('tps_mange_mur', int), ('tps_protection', int)]
    res = Serpent('est', 1, 0, [], 0, 0, 0, 'N')

    serpent = la_chaine.split('\n')
    s1, s2 = serpent 
    lst_s1 = s1.split(sep)
    lst_s2 = s2.split(sep)
    i = 0

    for cle,typ in lst_cle:
        res[cle] = typ(lst_s1[i])
        i += 1
    res['direction'] = lst_s1[i]
   
    lst_position = []
    for posi in range(0, len(lst_s2) -1 , 2):
    
        lst_position.append([int(lst_s2[posi]), int(lst_s2[posi + 1])])  
    res['positions'] = lst_position      
    return res












def copy_serpent(serpent:dict)->dict:
    """fait une copie du serpent passer en paramètres
    Attention à bien faire une copie de la liste des positions
    

    Args:
        serpent (dict): le serpent à recopier

    Returns:
        dict: la copie du serpent passé en paramètres
    """ 
    copie = {}
    for cle, val in serpent.items():
        if type(val) is list :
            copie[cle] = val[:]  
        else:
            copie[cle] = val   
    return copie                
