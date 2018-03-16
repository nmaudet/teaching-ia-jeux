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


#-------------------------------
    # renvoie les successeurs du noeud state
#-------------------------------
    
def ajout_successeurs(state, terrains_jeu):
    i=state[-2]
    j=state[-1]
    successeurs = []
    
    for k in range(9):
        #si c'est une cas libre
        if terrains_jeu[j][k] == 0:
            successeurs.append(state + (j,k))
    return successeurs
    
#-------------------------------
    # détermine si c'est une position qui va faire gagner le joueur player
#-------------------------------
    
def pos_gagne(state,terrains_jeu,player):
   # print(state)
    i=state[-2]
    j=state[-1]
    morpion=terrains_jeu[i]
    t=False
    
    if j==0 :
        hoz = morpion[1]==player and morpion[2]==player
        vect = morpion[3]==player and morpion[6]==player
        dig = morpion[4]==player and morpion[8]==player
    	
        if hoz or vect or dig:
            t=True
    
    if j==1 :
        hoz = morpion[2]==player and morpion[0]==player
        vect = morpion[4]==player and morpion[7]==player
    
        if hoz or vect:
            t=True
       
    if j==2 :
        hoz = morpion[1]==player and morpion[0]==player
        vect = morpion[5]==player and morpion[8]==player
        dig = morpion[4]==player and morpion[6]==player
    	
        if hoz or vect or dig:
            t=True
    	
    if j==3 :
        hoz = morpion[4]==player and morpion[5]==player
        vect = morpion[0]==player and morpion[6]==player
    	
        if hoz or vect:
            t=True
    
    if j==4 :
        hoz = morpion[3]==player and morpion[5]==player
        vect = morpion[1]==player and morpion[7]==player
        dig = morpion[0]==player and morpion[8]==player
        dig2 = morpion[2]==player and morpion[6]==player
    	
        if hoz or vect or dig or dig2:
            t=True
        
    if j==5 :
        hoz = morpion[4]==player and morpion[3]==player
        vect = morpion[2]==player and morpion[8]==player
    	
        if hoz or vect:
            t=True
    	
    if j==6 :
        hoz = morpion[7]==player and morpion[8]==player
        vect = morpion[0]==player and morpion[3]==player
        dig = morpion[4]==player and morpion[2]==player
    	
    		
        if hoz or vect or dig:
            t=True
    
    if j==7 :
        hoz = morpion[6]==player and morpion[8]==player
        vect = morpion[1]==player and morpion[4]==player

        if hoz or vect:
            t=True
    	
    if j==8 :
        hoz = morpion[6]==player and morpion[7]==player
        vect = morpion[5]==player and morpion[2]==player
        dig = morpion[4]==player and morpion[0]==player
    	
        if hoz or vect or dig:
            t=True
    return t
   
'''
def fh(state,j):
    if pos_gagne(state):
        nbr_vict_local[j]=nbr_vict_local[j]+1
        return 1
    else:
        return nbr_vict_local[j] 
 '''

#-------------------------------
    # détermine si le terrain est gagné par j ou non
#-------------------------------
    
def board_won(t, j):
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
            
    return v
    
    
def full_local_board(terrain):
    return not 0 in terrain

def full_global_board(terrains_jeu):
    for terrain in terrains_jeu:
        if not full_local_board(terrain):
            return False
    return True
 
def remaining_boards(terrains_jeu):
    boards = []
    for i in range(len(terrains_jeu)):
        if not full_local_board(terrains_jeu[i]):
            boards.append(i)
    return boards
    
    
successeurs = {}
valeur = {}


def alphabeta(state, terrains_jeu, player):
    """ implementation de alphabeta, version Russel & Norvig, Chapter 6
        """
    global successeurs
    global valeurs
    terrains_minimax = list(terrains_jeu) # terrain de jeu courant
    
    successeurs = {} # clé : tuple de positions (correspondant au chemin dans l'arbre), valeur : successeurs
    valeurs = {} 
    
    best_s = maxValue((state,),-1,1, terrains_minimax, player)
    print(best_s)
    return best_s
    
def maxValue(state, alpha, beta, t, player):
    choice = False

    terrains_minimax = list(t)    
    for i in range(9):
        terrains_minimax[i] = t[i][:]

    if len(state) != 1:
        
        i = state[-2]
        j = state[-1]
        terrains_minimax[i][j] = player+1
 
        if pos_gagne(state, terrains_minimax, j+1): # terrain gagné 
            valeur[state] = 10
            return valeur[state]
        elif full_global_board(terrains_minimax): # plus de position possible 
            valeur[state] = 0
            return valeur[state]
        elif full_local_board(terrains_minimax[j]): # plus de position possible dans le terrain j
            choice = True
        elif board_won(terrains_minimax[j], player) or board_won(terrains_minimax[j], (player+1)%2): # terrain j déjà gagné
            choice = True
   
    v = -10000
    best_s = (-1, -1)
    successeurs[state] = []
    
    # création des successeurs
    
    if len(state) == 1 : # racine de l'arbre (numéro du terrain)
        for i in range(9):
            successeurs[state].append(state + (i,))
    elif not choice:
        successeurs[state] = ajout_successeurs(state, terrains_minimax) 
    else:
        terrains_restants = remaining_boards(terrains_minimax)
        i = state[-2]
        j = state[-1]
        for k in terrains_restants:
            for l in range(9):
                if terrains_minimax[k][l] == 0:
                    successeurs[state].append(state + (k,l))
    
    
    for s in successeurs[state]:
        #v = max(v,minValue(s,alpha,beta, terrains_minimax, (player+1)%2))
        minV = minValue(s,alpha,beta, terrains_minimax, (player+1)%2)
        if minV >= v:
            v = minV
            
            best_s = (s[-2],s[-1])
        
        if v >= beta: # coupe beta, pas la peine d'étendre les autres fils
            return v
        alpha = max(alpha,v) # mise à jour de alpha par MAX
        
    if len(state) == 1: # on est à la racine, il faut choisir la position : best_s
        return best_s
    else:
        return v
    
def minValue(state, alpha, beta, t, player):
    choice = False # le joueur peut jouer sur le terrain qu'il veut ou non
    
    # copie des listes
    terrains_minimax = list(t)
    for i in range(9):
        terrains_minimax[i] = t[i][:]
        
    # on n'est pas à la racine de l'arbre    
    if len(state) != 1:
        i = state[-2]
        j = state[-1]
        terrains_minimax[i][j] = player+1 # le joueur joue à cette position
 
        if pos_gagne(state, terrains_minimax, j+1): # terrain gagné 
            valeur[state] = 10
            return valeur[state]
        elif full_global_board(terrains_minimax): # plus de position possible 
            valeur[state] = 0
            return valeur[state]
        elif full_local_board(terrains_minimax[j]): # plus de position possible dans le terrain j
            choice = True
        elif board_won(terrains_minimax[j], player) or board_won(terrains_minimax[j], (player+1)%2): # terrain j déjà gagné
            choice = True
            
    v = 10000
    successeurs[state] = []
    best_s = (-1, -1) # coordonnées du meilleur successeur
    
    # création des successeurs
    
    if len(state) == 1 : # racine de l'arbre (numéro du terrain)
        for i in range(9):
            successeurs[state].append(state + (i,))
    elif not choice:
        successeurs[state] = ajout_successeurs(state, terrains_minimax) 
    else: # terrain plein ou match terminé, on choisit le terrain que l'on veut
        terrains_restants = remaining_boards(terrains_minimax)
        i = state[-2]
        j = state[-1]
        for k in terrains_restants:
            for l in range(9):
                if terrains_minimax[k][l] == 0:
                    successeurs[state].append(state + (k,l))
    
    
    for s in successeurs[state]:
       # v = min(v,maxValue(s,alpha,beta, terrains_minimax, (player+1)%2))
        
        maxV = maxValue(s,alpha,beta, terrains_minimax, (player+1)%2) 
        if maxV <= v:
            v = maxV
            best_s = (s[-2],s[-1])
        
        if v <= alpha: # coupe beta, pas la peine d'étendre les autres fils
            return v
        
        beta = min(beta,v)
        
    if len(state) == 1:
        return v, best_s
    else:
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
        
     
    #-------------------------------
    # Trouve le chemin jusqu'à une position finale avec a-star 
    #-------------------------------
    
    def get_path(posInit, posFinale):
        p2 = ProblemeGrid2D(posInit,posFinale,mat,'manhattan')
        noeudFinal = probleme.astar(p2)
        chemin = []    
    
        pere = noeudFinal
        while pere.etat != posInit:
            chemin.append(pere.etat)
            pere = pere.pere
    
        return reversed(chemin)

    #-------------------------------
    # Déplace le personnage  
    #-------------------------------
    
    def go_to_position(posPlayer, player, chemin):
        for pos in chemin:
            row = pos[0]
            col = pos[1]
            player.set_rowcol(row, col)
            
            game.mainiteration()

            posPlayer=(row,col)

        return posPlayer
    
    #-------------------------------
    # Met à jour le score
    #-------------------------------
    def update_scores(score, j, morpions, terrains_jeu, terrain):
        fin = False
        t = terrains_jeu[terrain] # dernier terrain où le joueur a joué 
        v = False
        
        v = board_won(t, j)

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
   
    
    def random_strategy(terrains_jeu, terrain):
        while True: # tant qu'on tombe sur une case occupée
            random_case = random.randint(0,8) # case du terrain où va jouer le joueur  
            if (terrains_jeu[terrain][random_case] == 0): # case libre
                break
        return (terrain, random_case)
    
    def minimax_strategy(terrain, terrains_jeu, player):
        return alphabeta(terrain, terrains_jeu, player)
    
    #-------------------------------
    # Détermine le prochain coup du joueur en fonction de la stratégie adoptée
    #-------------------------------
    
    def choose_next_move(strategy, terrains_jeu, terrain):
        
        if (strategy == 'random'):
            return random_strategy(terrains_jeu, terrain)
        else:
            return minimax_strategy(terrain, terrains_jeu, j)
    #-------------------------------
    # Boucle principale de déplacements, un joueur apres l'autre
    #-------------------------------
    
    posPlayers = initStates
    tour = 0    
    j = 0

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
    
    strategies = ["minimax","random"] # stratégies des personnages
    
    for i in range(iterations):
        
       #p2 = ProblemeGrid2D(posPlayers[j],fiole_a_ramasser,mat,'manhattan')
      # noeudFinal = probleme.astar(p2)
       
       chemin = get_path(posPlayers[j], fiole_a_ramasser)
       posPlayers[j] = go_to_position(posPlayers[j], players[j], chemin)
       
       o = players[j].ramasse(game.layers) # on ramasse la fiole 
       game.mainiteration()
       print ("Objet de couleur ", couleur(o), " trouvé par le joueur ", j, "(", strategies[j], ")")
      
       t, c = choose_next_move(strategies[j], terrains_jeu, terrain) 
       pos_but = dict_terrains[(t,c)] # la case où doit aller le personnage
      
        
       chemin = get_path(fiole_a_ramasser, pos_but)
        
       posPlayers[j] = go_to_position(posPlayers[j], players[j], chemin)

       players[j].depose(game.layers)
       game.mainiteration()
       print("Le joueur ", j, " a déposé sa fiole en ", pos_but)
       terrains_jeu[t][c] = j+1 # la case est marquée

       fin, scores[j], morpions, terrains_jeu = update_scores(scores[j], j+1, morpions, terrains_jeu, terrain) # maj des scores  
        
       if fin: # l'un des joueurs à gagné
           break
        # on active le joueur suivant
        # et on place la fiole suivante
       
       j = (j+1)%2     
       if j == 0:
           tour+=1
           
       fiole_a_ramasser=put_next_fiole(j,tour)    
       terrain = c # prochain terrain
       
       if full_global_board(terrains_jeu):
           print("Partie terminée")
           break

       game.mainiteration()
       
       while morpions[terrain] != 0: # terrain déjà gagné par un des deux joueurs
           terrain = random.randint(0, 8) # choix aléatoire d'un autre terrain

        #break"""
       

    
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
    


