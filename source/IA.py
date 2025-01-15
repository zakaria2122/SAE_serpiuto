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
                                if arene.est_bonus(l_arene, lig, col):
                                    met_dans_dico(l_arene, lig, col, lig_t, col_t, dico_final, valeur_voisin + 1)
                                   

    return dico_final


def met_dans_dico(aren, lig, col, lig_d, col_d, dico, distance):
    if lig < lig_d :
        dico['N'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))
    if lig > lig_d:
        dico['S'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))
    if col < col_d :    
        dico['O'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))
    if col > col_d :
        dico['E'].append((distance, arene.get_val_boite(aren, lig, col), arene.get_proprietaire(aren, lig, col)))  


def get_tete(aren, num_j):
    """renvoie la position de la tete

    Args:
        serpent(dict)): le serpent

    Returns:
        list: position
    """
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
        le_plateau (aren): l'arene
        position (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 

    Returns:
        [bool]: True si la position est bien sur le plateau
    """
    taille_l, taille_c = pos
    nb_lig_ar, nb_col_ar = arene.get_dim(aren)
    return taille_l > -1 and taille_l < nb_lig_ar - 1 and taille_c > -1 and taille_c < nb_col_ar - 1



#==========================================================================================

def recherche_mini(dico_radar):
    mini = None
    card = ""
    for cardi, lst_tuple in dico_radar.items():
        for dist,_, _ in lst_tuple:
            if mini is None or dist < mini :
                mini = dist
                card = cardi
    return mini, card
































def mon_IA2(num_joueur:int, la_partie:dict)->str:
    return recherche_mini(objets_voisinage(la_partie['arene'], num_joueur, 5))[1]
   
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
    le_client.afficher_msg("terminé")s
