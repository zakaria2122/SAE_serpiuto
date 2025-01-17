# coding: utf-8
"""
            SAE1.02 SERPIUT'O
         BUT1 Informatique 2024-2025

    Module IA.py
    Ce module implémente toutes les fonctions ainsi que l'IA de votre serpent
"""

import partie
import argparse
import client
import random
import arene
import serpent
import matrice
direction_prec='X' # variable indiquant la décision précédente prise par le joueur. A mettre à jour soi-même

####################################################################
### A partir d'ici, implémenter toutes les fonctions qui vous seront 
### utiles pour prendre vos décisions
### Toutes vos fonctions devront être documentées
####################################################################

BONUS_INTERESSANT = {-1, -5, -2}


def directions_possibles(l_arene:dict,num_joueur:int)->str:
    """Indique les directions possible pour le joueur num_joueur
        c'est à dire les directions qu'il peut prendre sans se cogner dans
        un mur, sortir de l'arène ou se cogner sur une boîte trop grosse pour sa tête

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur

    Returns:
        str: une chaine composée de NOSE qui indique les directions
            pouvant être prise par le joueur. Attention il est possible
            qu'aucune direction ne soit possible donc la fonction peut retourner la chaine vide
    """    
    #complexité 0(N)
    return arene.directions_possibles(l_arene, num_joueur)

def objets_voisinage(l_arene:dict, num_joueur, dist_max:int):
    """Retourne un dictionnaire indiquant pour chaque direction possibles, 
        les objets ou boites pouvant être mangés par le serpent du joueur et
        se trouvant dans voisinage de la tête du serpent 

    Args:
        l_arene (dict): l'arène considérée
        num_joueur (int): le numéro du joueur considéré
        dist_max (int): le nombre de cases maximum qu'on s'autorise à partir du point de départ
    Returns:
        dict: un dictionnaire dont les clés sont des directions  et les valeurs une liste de triplets
            (distance,val_objet,prop) où distance indique le nombre de cases jusqu'à l'objet et id_objet
            val_obj indique la valeur de l'objet ou de la boite et prop indique le propriétaire de la boite
    """
    #complexité 0(N³)
    dico_final = {'N': [], 'S': [], 'E': [], 'O': []}

    lig_t, col_t = get_tete(l_arene, num_joueur)
    calque = matrice.Matrice(matrice.get_nb_lignes(l_arene['matrice']), matrice.get_nb_colonnes(l_arene["matrice"]))
    matrice.set_val(calque, lig_t, col_t, 0)
    modif = True 

    while modif :
        modif = False

        for lig in range(matrice.get_nb_lignes(l_arene["matrice"])):
            for col in range(matrice.get_nb_colonnes(l_arene["matrice"])):      
                position_act = (lig, col)
                val_act = matrice.get_val(calque, lig, col)

                if val_act == None and not arene.est_mur(l_arene, lig, col):
                    for pos_voisin in voisins_possible(l_arene, position_act): 
                        (lig_voisin, col_voisin) = pos_voisin
                        valeur_voisin = matrice.get_val(calque, lig_voisin, col_voisin)

                        if valeur_voisin != None :
                            if valeur_voisin < dist_max:
                                matrice.set_val(calque, lig, col, valeur_voisin + 1)
                                modif = True

                                if arene.get_val_boite(l_arene, lig, col) in BONUS_INTERESSANT or arene.get_val_boite(l_arene, lig, col) >= 1 and arene.get_val_boite(l_arene, lig, col) <= arene.get_val_boite(l_arene, lig_t, col_t) and arene.get_proprietaire(l_arene, lig, col) != num_joueur:

                                    met_dans_dico(l_arene, lig, col, lig_t, col_t, dico_final, valeur_voisin, calque)

    return dico_final

def met_dans_dico(aren, lig, col, lig_t, col_t, dico, distance, calque):
    """met dans le dictionnaire la distance avec un objet interressant à la bonne cardinalité

    Args:
        aren (dict): 
        lig (int): 
        col (int): 
        lig_t (int): 
        col_t (int): 
        dico (dict): dico final
        distance (int): distance de l'objet 
        calque (dict): 
    """
    #complexité 0(1)
    position_case = (lig, col)
    lst_chemin = plus_cours_chemin(calque, position_case, aren )

    case1_l, case1_c = lst_chemin[-2]

    

    if case1_l < lig_t:
        dico['N'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))


    if case1_l > lig_t:
        dico['S'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))


    if case1_c < col_t:    
        dico['O'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))


    if case1_c > col_t:
        dico['E'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))  


def plus_cours_chemin(calque, position_arrive, aren):
    """detrermine le plus court chemin entre deux position 

    Args:
        calque (dict): le claque creer par la fonction objet_voisinage
        position_arrive (tuple): position d'arrivé (ligne, colonne)
        aren (dict): l'arene en question 

    Returns:
        list: liste des posion du plus court chemin 
    """
    #complexité 0(N)
    trouve = False
    lst_final = [position_arrive]
    pos_act = position_arrive

    while not trouve:
        ens_voisin = voisins_possible(aren, pos_act)
        (lig_act, col_act) = pos_act
        val_act = matrice.get_val(calque, lig_act, col_act)

        if val_act == 0 :
            trouve = True 
        
        else:
            bon_voisin = False
            for voisin in ens_voisin:
                (lig_v, col_v) = voisin
                val_voisin = matrice.get_val(calque, lig_v, col_v)
                if val_voisin == val_act - 1 and not bon_voisin:
                    lst_final.append(voisin)
                    bon_voisin = True
                    pos_act = voisin    

    return lst_final 

def get_tete(aren, num_j):
    """renvoie la position de la tete

    Args:
        serpent(dict)): le serpent

    Returns:
        list: position
    """
    #complexité 0(1)
    return arene.get_serpent(aren, num_j)[0]

def voisins_possible(le_plateau, position):
    """Renvoie l'ensemble des positions cases voisines accessibles de la position renseignées
       Une case accessible est une case qui est sur le plateau et qui n'est pas un mur
    Args:
        le_plateau (plateau): un plateau de jeu
        position (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 

    Returns:
        set: l'ensemble des positions des cases voisines accessibles
    """
    #complexité 0(1)
    (lig_act, col_act) = position 

    pos_n_l, pos_n_c = lig_act - 1, col_act
    pos_s_l, pos_s_c = (lig_act + 1, col_act)
    pos_e_l, pos_e_c = (lig_act, col_act + 1)
    pos_o_l, pos_o_c = (lig_act, col_act - 1)

    ens_final = set()

    if est_sur_le_plateau(le_plateau, (pos_n_l, pos_n_c)) and not arene.est_mur(le_plateau, pos_n_l, pos_n_c):
        ens_final.add((pos_n_l, pos_n_c))

    if est_sur_le_plateau(le_plateau, (pos_s_l, pos_s_c)) and not arene.est_mur(le_plateau, pos_s_l, pos_s_c):
        ens_final.add((pos_s_l, pos_s_c))   

    if est_sur_le_plateau(le_plateau, (pos_e_l, pos_e_c)) and not arene.est_mur(le_plateau, pos_e_l, pos_e_c):
        ens_final.add((pos_e_l, pos_e_c))    

    if est_sur_le_plateau(le_plateau, (pos_o_l, pos_o_c)) and not arene.est_mur(le_plateau, pos_o_l, pos_o_c):
        ens_final.add((pos_o_l, pos_o_c))    

    return ens_final


def est_sur_le_plateau(aren, pos):
    """Indique si la position est bien sur le plateau

    Args:
        aren (dict): l'arene en question
        position (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 

    Returns:
        [bool]: True si la position est bien sur le plateau
    """
    #complexité 0(1)
    taille_l, taille_c = pos
    nb_lig_ar, nb_col_ar = arene.get_dim(aren)
    return taille_l > -1 and taille_l < nb_lig_ar and taille_c > -1 and taille_c < nb_col_ar



#==========================================================================================

def recherche_mini(dico_radar):
    """recherche de minimum dans un dictionnaire 

    Args:
        dico_radar (dict): dictionnaire identique à celui renvoyé par la fonction objet voisinage

    Returns:
        str: cardinalité idéal 
    """
    #complexité 0(N²)
    mini = None
    card = ""
    for cardi, lst_tuple in dico_radar.items():
        for dist,_, _ in lst_tuple:
            if mini is None or dist < mini :
                mini = dist
                card = cardi           
    return card

def auto_mange(aren, num_joueur, lig_t, col_t):
    """ si le serpent se bloque dans un mur, il s'auto mange pour faire demi-tour 

    Args:
        aren (dict): l'arene
        num_joueur (int): le numero du joueur
        lig_t (int): numero de lige de la tete du serpent
        col_t (int): numero colonne de la tete du serpent 

    Returns:
        str: cardinalité pour faire demi-tour
    """
    #complexité 0(1)
    position_serpent = arene.get_serpent(aren, num_joueur)

    if len(position_serpent) >= 2:
        pos_cou_l, pos_cou_c = position_serpent[1]

        if pos_cou_l < lig_t :
            return 'N'
        elif pos_cou_l > lig_t:
            return 'S'
        elif pos_cou_c > col_t :
            return 'E'
        else :
            return 'O'

    else:
        return 'N'










def mon_IA2(num_joueur: int, la_partie: dict) -> str:
    """
    Implémente une IA basique pour choisir une direction valide pour un joueur.

    Args:
    num_joueur (int): Numéro du joueur.
    la_partie (dict): Dictionnaire contenant les informations de la partie.

    Returns:
    str: Une direction parmi celles possibles ('N', 'S', 'E', 'O'), ou 'X' si aucune n'est possible.
    """
    #complexité 0(N³)
    l_arene = la_partie.get('arene') #complexité 0(1)
    tete_l, tete_c = get_tete(l_arene, num_joueur) #complexité 0(1)
    dir_pos = directions_possibles(l_arene, num_joueur) #complexité 0(N)
    if not dir_pos: #complexité 0(1)
        return auto_mange(l_arene, num_joueur, tete_l, tete_c) #complexité 0(1)
        
    direction = random.choice(dir_pos) #complexité 0(1)
    voisins = objets_voisinage(l_arene, num_joueur, 10) #complexité 0(N³)
    direction_optimale = recherche_mini(voisins) #complexité 0(N²)
    return direction_optimale if direction_optimale in dir_pos else direction #complexité 0(N)
    

def mon_IA(num_joueur:int, la_partie:dict)->str:
    """Fonction qui va prendre la decision du prochain coup pour le joueur de numéro ma_couleur

    Args:
        num_joueur (int): un entier désignant le numero du joueur qui doit prendre la décision
        la_partie (dict): structure qui contient la partie en cours

    Returns:
        str: une des lettres 'N', 'S', 'E' ou 'O' indiquant la direction que prend la tête du serpent du joueur
    """
    direction=random.choice("NSEO")
    direction_prec=direction #La décision prise sera la direction précédente le prochain tour
    dir_pos=arene.directions_possibles(partie.get_arene(la_partie),num_joueur)
    if dir_pos=='':
        direction=random.choice('NOSE')
    else:
        direction=random.choice(dir_pos)
    return direction

if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu,_=le_client.prochaine_commande()
        if ok:
            la_partie=partie.partie_from_str(le_jeu)
            actions_joueur=mon_IA2(int(id_joueur),la_partie)
            le_client.envoyer_commande_client(actions_joueur)
    le_client.afficher_msg("terminé")
