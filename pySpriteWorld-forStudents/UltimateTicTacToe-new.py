# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18
# modifié par Laura Nguyen et Fatemeh Hamissi

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys


from grid2D import *
    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()


def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'tictactoeBis'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def ajout_successeurs(state, successeurs,terrains_jeu):
    (i,j)=state[-1]
    #si c'est une cas libre
    for case in terrains_jeu[j]:
        if case == 0:
            a=terrains_jeu[j].index(case)
            successeurs[state].append((a,j))
    return successeurs
    
'''   
# détermine si c'est une position qui va nous faire gagner
def pos_gagne(state,terrains_jeu,player):
    i,j=state[-1]
    morpion=terrain[i]
    
    t=False
    
    if j==0 :
    	hoz = morpion[i][1]==player and morpion[i][2]==player
    	vect = morpion[i][3]==player and morpion[i][6]==player
    	dig = morpion[i][4]==player and morpion[i][8]==player
    	
     if hoz or vect or dig:
        t=True
    
    if j==1 :
    	hoz = morpion[i][2]==player and morpion[i][0]==player
    	vect = morpion[i][4]==player and morpion[i][7]==player
    
    if hoz or vect:
        t=True
       
    if j==2 :
    	hoz = morpion[i][1]==player and morpion[i][0]==player
    	vect = morpion[i][5]==player and morpion[i][8]==player
    	dig = morpion[i][4]==player and morpion[i][6]==player
    	
    	if hoz or vect or dig:
        t=True
    	
    if j==3 :
    	hoz = morpion[i][4]==player and morpion[i][5]==player
    	vect = morpion[i][0]==player and morpion[i][6]==player
    	
    	if hoz or vect or:
        t=True
    
    if j==4 :
    	hoz = morpion[i][3]==player and morpion[i][5]==player
    	vect = morpion[i][1]==player and morpion[i][7]==player
    	dig = morpion[i][0]==player and morpion[i][8]==player
    	dig2 = morpion[i][2]==player and morpion[i][6]==player
    	
    	if hoz or vect or dig or dig2:
        t=True
        
    if j==5 :
    	hoz = morpion[i][4]==player and morpion[i][3]==player
    	vect = morpion[i][2]==player and morpion[i][8]==player
    	
    	if hoz or vec:
        t=True
    	
    if j==6 :
    	hoz = morpion[i][7]==player and morpion[i][8]==player
    	vect = morpion[i][0]==player and morpion[i][3]==player
    	dig = morpion[i][4]==player and morpion[i][2]==player
    	
    		
    	if hoz or vec or dig:
        t=True
    
    if j==7 :
    	hoz = morpion[i][6]==player and morpion[i][8]==player
    	vect = morpion[i][1]==player and morpion[i][4]==player

    	if hoz or vec:
        t=True
    	
    if j==8 :
    	hoz = morpion[i][6]==player and morpion[i][7]==player
    	vect = morpion[i][5]==player and morpion[i][2]==player
    	dig = morpion[i][4]==player and morpion[i][0]==player
    	
    	if hoz or vec or dig:
        t=True
   
   return t
   '''

def fh(state,j):
    if pos_gagne(state):
        nbr_vict_local[j]=nbr_vict_local[j]+1
        return 1
    else:
        return nbr_vict_local[j] 
 
def alphabeta(state):
    """ implementation de alphabeta, version Russel & Norvig, Chapter 6
        """
    v = maxValue(state,-inf,inf)
    return v
    
def maxValue(state,alpha,beta):
    if feuille(state): # si feuille on renvoie la valeur
        return valeur[state]
    v = -inf
    for s in successeurs[state]:
        print ("étendu noeud ", s)
        v = max(v,minValue(s,alpha,beta))
        if v >= beta: # coupe beta, pas la peine d'étendre les autres fils
            print ("coupe beta")
            return v
        alpha = max(alpha,v) # mise à jour de alpha par MAX
    return v  
 
def minValue(state,alpha,beta):
    if feuille(state): # si feuille on renvoie la valeur
        return valeur[state]
    v = inf
    for s in successeurs[state]:
        print ("étendu noeud ", s)
        v = min(v,maxValue(s,alpha,beta))
        if v <= alpha: # coupe alpha, pas la peine d'étendre les autres fils
            print ("coupe alpha")
            return v
        beta = min(beta,v)
    return v
   
def feuille(state): # les feuilles n'apparaissent pas comme clés dans mon dictionnaire successeurs
    return state not in successeurs  
   
def main():

    #for arg in sys.argv:
    iterations = 500 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)
    
    mur = [False] * 20
    vide= [False] + [True] * 17 + [False, False]
    first=[False, True,True,False, False,True, False, False, False, True,False,False,False,True,False,False,True,True, False, False]
    sec=[False, True,True,False,True,True,True, False, True,True,True,False,True,True,True,False,True,True, False, False]
    
    mat=np.array((mur,vide,vide,first,sec,vide,sec,first,sec,vide,sec,first,sec,vide,sec,first,vide,vide, mur, mur)) # matrice représentant la map

    init()

        

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    scores = [0]*nbPlayers
    #fioles = {} # dictionnaire (x,y)->couleur pour les fioles
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
  #  print ("Init states:", initStates)
    
    
    # on localise tous les objets ramassables
    #goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    #print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    # et la zone de jeu pour le tic-tac-toe
    tictactoeStates = [(x,y) for x in range(3,16) for y in range(3,16)]
    #print ("Wall states:", wallStates)
 #   print(tictactoeStates)
    # les coordonnees des tiles dans la fiche
    tile_fiole_jaune = (19,1)
    tile_fiole_bleue = (20,1)
    
    # listes des objets fioles jaunes et bleues
    
    fiolesJaunes = [f for f in game.layers['ramassable'] if f.tileid==tile_fiole_jaune]
    fiolesBleues = [f for f in game.layers['ramassable'] if f.tileid==tile_fiole_bleue]   
    all_fioles = (fiolesJaunes,fiolesBleues) 
    fiole_a_ramasser = (0,0) # servira à repérer la prochaine fiole à prendre
    
    # renvoie la couleur d'une fiole
    # potentiellement utile
    
    def couleur(o):
        if o.tileid==tile_fiole_jaune:
            return 'jaune'
        elif o.tileid==tile_fiole_bleue:
            return 'bleue'
    
    
    #-------------------------------
    # Placement aleatoire d'une fioles de couleur 
    #-------------------------------
    
    def put_next_fiole(j,t):
        o = all_fioles[j][t]
    
        # et on met cette fiole qqpart au hasard
    
        x = random.randint(1,19)
        y = random.randint(1,19)
    
        while (x,y) in tictactoeStates or (x,y) in wallStates: # ... mais pas sur un mur
            x = random.randint(1,19)
            y = random.randint(1,19)
        o.set_rowcol(x,y)
        # on ajoute cette fiole dans le dictionnaire
        #fioles[(x,y)]=couleur(o)
    
        game.layers['ramassable'].add(o)
        game.mainiteration()
        return (x,y)
        
        
    def get_path(noeudFinal, posInit):
        chemin = []    
    
        pere = noeudFinal
        while pere.etat != posInit:
            chemin.append(pere.etat)
            pere = pere.pere
    
        return reversed(chemin)

    def go_to_position(posPlayer, player, chemin):
        for pos in chemin:
            row = pos[0]
            col = pos[1]
            player.set_rowcol(row, col)
            
            game.mainiteration()

            posPlayer=(row,col)

        return posPlayer
    
    def update_scores(score, j, morpions, terrains_jeu, terrain):
        fin = False
        t = terrains_jeu[terrain] # dernier terrain où le joueur a joué 
        v = False
        
        # lignes
        if t[0] == t[1] == t[2] == j: # 1ère ligne remplie
            v = True
        if t[3] == t[4] == t[5] == j:
            v = True
        if t[6] == t[7] == t[8] == j:
            v = True
            
        # colonnes
        if t[0] == t[3] == t[6] == j:
            v = True
        if t[1] == t[4] == t[7] == j:
            v = True
        if t[2] == t[5] == t[8] == j:
            v = True
            
        # diagonales
        if t[0] == t[4] == t[8] == j:
            v = True
        if t[2] == t[4] == t[6] == j:
            v = True
            
        if v: # le joueur a gagné le terrain
            morpions[terrain] = j
            v = False
            score += 1
            
            if terrain in [0, 1, 2] and morpions[0] == morpions[1] == morpions[2]: # 1ère lignée de terrain marquée
                v = True
            if terrain in [3, 4, 5] and morpions[3] == morpions[4] == morpions[5]:
                v = True
            if terrain in [6, 7, 8] and morpions[6] == morpions[7] == morpions[8]:
                v = True
            if terrain in [0, 3, 6] and morpions[0] == morpions[3] == morpions[6]: # 1ère colonne de terrain marquée
                v = True
            if terrain in [1, 4, 7] and morpions[1] == morpions[4] == morpions[7]:
                v = True
            if terrain in [2, 5, 8] and morpions[2] == morpions[5] == morpions[8]:
                v = True
            
            if v:
                fin = True
               
                
        return fin, score, morpions, terrains_jeu
   
    #-------------------------------
    # Boucle principale de déplacements, un joueur apres l'autre
    #-------------------------------
    
    posPlayers = initStates
    print(posPlayers)
    tour = 0    
    j = 1 # le joueur 0 commence
    # on place la premiere fiole jaune      

    fiole_a_ramasser = put_next_fiole(0,tour)    

    morpions = [0] * 9 # les 9 terrains de jeu, 0: match non terminé, 1: joueur 1 a gagné, 2: joueur 2 a gagné
    terrains_jeu = [
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ] # terrains de jeux, 0: case libre, 1: case occupée par le joueur 1, 2:case occupée par le joueur 2
                        
    terrain = random.randint(0,8) # terrain où va jouer le premier joueur 
    
    dict_terrains = {
                     (0,0): (4, 4), (0,1): (4,5) ,(0,2): (4,6), (0,3): (5, 4), (0,4): (5, 5), (0,5): (5, 6), (0,6): (6, 4), (0,7): (6,5),(0,8): (6, 6),
                     (1,0): (4, 8), (1,1): (4,9) ,(1,2): (4,10), (1,3): (5, 8), (1,4): (5, 9), (1,5): (5, 10), (1,6): (6, 8), (1,7): (6,9),(1,8): (6, 10),
                     (2,0): (4, 12), (2,1): (4,13) ,(2,2): (4,14), (2,3): (5, 12), (2,4): (5, 13), (2,5): (5, 14), (2,6): (6, 12), (2,7): (6,13),(2,8): (6, 14),
                     (3,0): (8, 4), (3,1): (8,5) ,(3,2): (8,6), (3,3): (9, 4), (3,4): (9, 5), (3,5): (9, 6), (3,6): (10, 4), (3,7): (10,5),(3,8): (10, 6),
                     (4,0): (8, 8), (4,1): (8,9) ,(4,2): (8,10), (4,3): (9, 8), (4,4): (9, 9), (4,5): (9, 10), (4,6): (10, 8), (4,7): (10,9),(4,8): (10, 10),    
                     (5,0): (8, 12), (5,1): (8,13) ,(5,2): (8,14), (5,3): (9, 12), (5,4): (9, 13), (5,5): (9, 14), (5,6): (10, 12), (5,7): (10,13),(5,8): (10, 14),
                     (6,0): (12, 4), (6,1): (12,5) ,(6,2): (12,6), (6,3): (13, 4), (6,4): (13, 5), (6,5): (13, 6), (6,6): (14, 4), (6,7): (14,5),(6,8): (14, 6),
                     (7,0): (12, 8), (7,1): (12,9) ,(7,2): (12,10), (7,3): (13, 8), (7,4): (13, 9), (7,5): (13, 10), (7,6): (14, 8), (7,7): (14,9),(7,8): (14, 10),
                     (8,0): (12, 12), (8,1): (12,13) ,(8,2): (12,14), (8,3): (13, 12), (8,4): (13, 13), (8,5): (13, 14), (8,6): (14, 12), (8,7): (14,13),(8,8): (14, 14)
                    }
    # dictionnaire (terrain, case du terrain) => case dans mat
    for i in range(iterations):
       print("Position joueur 0 : ", posPlayers[j])
       print("Position fiole : ", fiole_a_ramasser)
       
       p2 = ProblemeGrid2D(posPlayers[j],fiole_a_ramasser,mat,'manhattan')
       noeudFinal = probleme.astar(p2)
       chemin = get_path(noeudFinal, posPlayers[j])
       posPlayers[j] = go_to_position(posPlayers[j], players[j], chemin)
       o = players[j].ramasse(game.layers) # on ramasse la fiole 
       game.mainiteration()
       print ("Objet de couleur ", couleur(o), " trouvé par le joueur ", j)
      
       
       '''
       while True: # tant qu'on tombe sur une case occupée
            random_case = random.randint(0,8) # case du terrain où va jouer le joueur  
            if (terrains_jeu[terrain][random_case] == 0): # case libre
                break
                
     '''
       pos_but = dict_terrains[(terrain, random_case)] # la case où doit aller le personnage
       p2 = ProblemeGrid2D(posPlayers[j],pos_but,mat,'manhattan')
       noeudFinal = probleme.astar(p2)
        
       chemin = get_path(noeudFinal, posPlayers[j])
        
       posPlayers[j] = go_to_position(posPlayers[j], players[j], chemin)

       players[j].depose(game.layers)
       game.mainiteration()
       print("Le joueur ", j, " a déposé sa fiole en ", pos_but)
       terrains_jeu[terrain][random_case] = j+1 # la case est marquée

       fin, scores[j], morpions, terrains_jeu = update_scores(scores[j], j+1, morpions, terrains_jeu, terrain) # maj des scores  
        
       if fin: # l'un des joueurs à gagner
           break
        # on active le joueur suivant
        # et on place la fiole suivante
       
        
       fiole_a_ramasser=put_next_fiole(j,tour)    
       terrain = random_case # prochain terrain
       
       if not 0 in morpions: # tous les match sont terminés
           print("Partie terminée")
           break
       game.mainiteration()
       while morpions[terrain] != 0: # terrain déjà gagné par un des deux joueurs
           terrain = random.randint(0, 8) # choix aléatoire d'un autre terrain

        #break"""
       j = (j+1)%2     
       if j == 0:
           tour+=1

    
    print("Scores : ", scores)
    if scores[0] > scores[1]:
      print("Le joueur 1 a gagné")
    elif scores[0] < scores[1]:
      print("Le joueur 2 a gagné")
    else:
      print("Egalité")
    #  pygame.quit()
    
        

if __name__ == '__main__':
    main()
    


