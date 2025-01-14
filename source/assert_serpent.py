import serpent as s 

serpent1 = s.Serpent('esteban', 1, 100, [[0,0], [0,1], [1,1]], 5, 0, 5, 'E')
serpent2 = s.Serpent('louis', 2, 200, [[2,0], [2,1], [2,1]], 0, 6, 0, 'S')
serpentv = s.Serpent('', 3, 0, [[0,0]])

def test_get_nom():
    assert s.get_nom(serpent1) == 'esteban'
    assert s.get_nom(serpent2) == 'louis'
    assert s.get_nom(serpentv) == ''

def test_get_num_joueur():
    assert s.get_num_joueur(serpent1) == 1
    assert s.get_num_joueur(serpent2) == 2
    assert s.get_num_joueur(serpentv) == 3

def test_get_point():
    assert s.get_points(serpent1) == 100
    assert s.get_points(serpent2) == 200
    assert s.get_points(serpentv) == 0

def test_get_pos():
    assert s.get_liste_pos(serpent1) ==   [[0,0], [0,1], [1,1]]  
    assert s.get_liste_pos(serpent2) ==   [[2,0], [2,1], [2,1]]
    assert s.get_liste_pos(serpentv) ==   [[0,0]]

def test_get_queue():
    assert s.get_queue(serpent1) == [0,0]  
    assert s.get_queue(serpent2) == [2,0]   
    assert s.get_queue(serpentv) == [0,0]    

def test_get_derniere_direction():
    assert s.get_derniere_direction(serpent1) == 'E'    
    assert s.get_derniere_direction(serpent2) == 'S'    
    assert s.get_derniere_direction(serpentv) == 'N'    

def test_get_bonus():
    assert s.get_bonus(serpent1) == [-3, -4]  
    assert s.get_bonus(serpent2) == [-5] 
    assert s.get_bonus(serpentv) == [] 

def test_ajouter_points():
    s.ajouter_points(serpent1, 10) 
    assert serpent1['points'] == 110

    s.ajouter_points(serpent1, -10) 
    assert serpent1['points'] == 100

    s.ajouter_points(serpent2, 10) 
    assert serpent2['points'] == 210

    s.ajouter_points(serpent2, -10) 
    assert serpent2['points'] == 200

    s.ajouter_points(serpentv, 10) 
    assert serpentv['points'] == 10

    s.ajouter_points(serpentv, -10) 
    assert serpentv['points'] == 0

def test_set_liste_pos():
    s.set_liste_pos(serpent1, [9,9])
    assert serpent1['positions'] == [9,9]
    serpent1['positions'] = [[0,0], [0,1], [1,1]]

    s.set_liste_pos(serpent2, [1,9])
    assert serpent2['positions'] == [1,9]
    serpent2['positions'] = [[2,0], [2,1], [2,1]]

    s.set_liste_pos(serpentv, [1,5])
    assert serpentv['positions'] == [1,5]
    serpentv['positions'] = [[0,0]]   

def test_new_direction():
    s.set_derniere_direction(serpent1, 'S')
    assert serpent1['direction'] ==  'S'
    serpent1['direction'] = 'E'

    s.set_derniere_direction(serpent2, 'E')
    assert serpent2['direction'] ==  'E'
    serpent2['direction'] = 'S'    

    s.set_derniere_direction(serpentv, 'S')
    assert serpentv['direction'] ==  'S'
    serpentv['direction'] = 'E'  

def test_to_str():
    assert s.to_str(serpent1) == 'esteban 1 -> 100 s:5 m:5 p:0'    
    assert s.to_str(serpent2) == 'louis 2 -> 200 s:0 m:0 p:6'  
    assert s.to_str(serpentv) == ' 3 -> 0 s:0 m:0 p:0'    

def test_get_tps_protection():
    assert s.get_temps_protection(serpent1) == 0    
    assert s.get_temps_protection(serpent2) == 6  
    assert s.get_temps_protection(serpentv) == 0   

def test_get_tps_mange_mur():
    assert s.get_temps_mange_mur(serpent1) == 5   
    assert s.get_temps_mange_mur(serpent2) == 0
    assert s.get_temps_mange_mur(serpentv) == 0      

def test_get_tps_surpuissance():
    assert s.get_temps_surpuissance(serpent1) == 5  
    assert s.get_temps_surpuissance(serpent2) == 0
    assert s.get_temps_surpuissance(serpentv) == 0       

def test_copie_serpent():
    copie = s.copy_serpent(serpent1)
    assert serpent1 == copie

    copie['nom_j'] = 'modif'
    assert copie['nom_j'] != serpent1['nom_j']   

    copie['positions'] = [[0,0]]
    assert copie['positions'] != serpent1['positions']

def test_str_machin():
    s1 = s.serpent_2_str(serpent1)
    s2 =  s.serpent_2_str(serpent2)
    assert s1 == 'esteban;1;100;5;5;0;E\n0;0;0;1;1;1\n'
    assert s2 == 'louis;2;200;0;0;6;S\n2;0;2;1;2;1\n'

    assert s.serpent_from_str(s1) == {'nom_j': 'esteban', 'num_j': 1, 'points': 100, 'positions': [[0, 0], [0, 1], [1, 1]], 'tps_surpuissance': 5, 'tps_protection': 0, 'tps_mange_mur': 5, 'direction' : 'N'}
    assert s.serpent_from_str(s2) == {'nom_j': 'louis', 'num_j': 2, 'points': 200, 'positions': [[2, 0], [2, 1], [2, 1]], 'tps_surpuissance': 0, 'tps_protection': 6, 'tps_mange_mur': 0, 'direction' : 'N'}
