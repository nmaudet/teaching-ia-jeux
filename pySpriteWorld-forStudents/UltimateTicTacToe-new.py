# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

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
    
    mat=np.array((mur,vide,vide,first,sec,vide,sec,first,sec,vide,sec,first,sec,vide,sec,first,vide,vide, mur, mur))

    init()

        

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    #score = [0]*nbPlayers
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
            return 'j'
        elif o.tileid==tile_fiole_bleue:
            return 'b'
    
    
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


    #-------------------------------
    # Boucle principale de déplacements, un joueur apres l'autre
    #-------------------------------
    
    posPlayers = initStates

    tour = 0    
    j = 0 # le joueur 0 commence
    # on place la premiere fiole jaune      

    fiole_a_ramasser = put_next_fiole(0,tour)    

    morpions = [0] * 9 # les 9 terrains de jeu, 0: matcg nul ou non terminé, 1: joueur 1 a gagné, 2: joueur 2 a gagné
    terrain = random.randint(0,8) # terrain où va jouer le premier joueur 
    
    dict_terrains = {(0,0): (4, 4), (0,1): (4,5) ,(0,2): (4,6), (0,3): (5, 4), (0,4): (5, 5), (0,5): (5, 6), (0,6): (6, 4), (0,7): (6,5),(0:8): (6, 6),
                     (1,0): (4, 8), (1,1): (4,9) ,(1,2): (4,10), (1,3): (5, 8), (1,4): (5, 9), (1,5): (5, 10), (1,6): (6, 8), (1,7): (6,9),(1:8): (6, 10),
                     (2,0): (4, 12), (2,1): (4,13) ,(2,2): (4,14), (2,3): (5, 12), (2,4): (5, 13), (2,5): (5, 14), (2,6): (6, 12), (2,7): (6,13),(2:8): (6, 14),
                     (3,0): (8, 4), (3,1): (8,5) ,(3,2): (8,6), (3,3): (9, 4), (3,4): (9, 5), (3,5): (9, 6), (3,6): (10, 4), (3,7): (10,5),(3:8): (10, 6),
                     (4,0): (8, 8), (4,1): (8,9) ,(4,2): (8,10), (4,3): (9, 8), (4,4): (9, 9), (4,5): (9, 10), (4,6): (10, 8), (4,7): (10,9),(4:8): (10, 10),    
                     (5,0): (8, 12), (5,1): (8,13) ,(5,2): (8,14), (5,3): (9, 12), (5,4): (9, 13), (5,5): (9, 14), (5,6): (10, 12), (5,7): (10,13),(5:8): (10, 14),
                     (5,0): (8, 12), (5,1): (8,13) ,(5,2): (8,14), (5,3): (9, 12), (5,4): (9, 13), (5,5): (9, 14), (5,6): (10, 12), (5,7): (10,13),(5:8): (10, 14),
   # dictionnaire (terrain, case du terrain) => case dans mat
   
   for i in range(iterations):
        print("Position joueur 0 : ", posPlayers[j])
        print("Position fiole : ", fiole_a_ramasser)
       
        p2 = ProblemeGrid2D(posPlayers[j],fiole_a_ramasser,mat,'manhattan')
        noeudFinal = probleme.astar(p2)

        chemin = get_path(noeudFinal, posPlayers[j])
        
        row,col = posPlayers[j]

        for pos in chemin:
            row = pos[0]
            col = pos[1]
            players[j].set_rowcol(row, col)
            
           # print ("pos :", j, next_row,next_col)
            game.mainiteration()

            posPlayers[j]=(row,col)
        
        o = players[j].ramasse(game.layers) # on la ramasse
        game.mainiteration()
        print ("Objet de couleur ", couleur(o), " trouvé par le joueur ", j)
            
        # ici il faudrait aller la mettre a la position choisie
        # pour jouer a ultimate tic-tac-toe
        # et verifier que la position est legale etc.            
        
        random_case = random.randint(0,8) # case du terrain où va jouer le prochain joueur  
            
        pos_but = dict_cases[(terrain, random_case)]
        p2 = ProblemeGrid2D(posPlayers[j],pos_but,mat,'manhattan')
        noeudFinal = probleme.astar(p2)
        
        chemin = get_path(noeudFinal, posPlayers[j])
        
        row,col = posPlayers[j]

        for pos in chemin:
            row = pos[0]
            col = pos[1]
            players[j].set_rowcol(row, col)

            game.mainiteration()

            posPlayers[j]=(row,col)
        
        players[j].depose(game.layers) # on la ramasse
        game.mainiteration()
            
        # on active le joueur suivant
        # et on place la fiole suivante
        j = (j+1)%2     
        if j == 0:
            tour+=1
        
        fiole_a_ramasser=put_next_fiole(j,tour)    
        terrain = random_case # prochain terrain
        
        if morpions[terrains] != 0:
            terrain = random.randint(0, 8)
                
        #break"""
    
            
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


