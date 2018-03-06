









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
    vide= [True]*17
    first=[True,True,False, False,True, False, False, False, True,False,False,False,True,False,False,True,True]
    sec=[True,True,False,True,True,True, False, True,True,True,False,True,True,True,False,True,True]
    '''mat=np.array(([[True]*17,
         [True]*17,
         [True,True,False, False,True, False, False, False, True,False,False,False,True,False,False,True,True],
         [True,True,False,True,True,True,True, False, True,True,True,False,True,True,True,False,True,True],
         [True]*17,
         [True,True,False,True,True,True,True, False, True,True,True,False,True,True,True,False,True,True],
         [True,True,False, False, True, False, False, False, True,False,False,False,True,False,False,True,True],
         [True,True,False,True,True,True,True, False, True,True,True,False,True,True,True,False,True,True],
         [True]*17,
         [True,True,False,True,True,True,True, False, True,True,True,False,True,True,True,False,True,True],
         [True,True,False, False,True, False, False, False, True,False,False,False,True,False,False,True,True],
         [True,True,False,True,True,True,True, False, True,True,True,False,True,True,True,False,True,True],
         [True]*17,
         [True,True,False,True,True,True,True, False, True,True,True,False,True,True,True,False,True,True],
         [True,True,False, False,True, False, False, False, True,False,False,False,True,False,False,True,True],
         [True]*17,
         [True]*17]))'''
    
    mat=np.array([vide,vide,first,sec,vide,sec,first,sec,vide,sec,first,sec,vide,sec,first,vide,vide])    
   # mat = np.array([[False,False],[True,True]])     
    #mat = np.ones((17,17))         
    #np.reshape(mat,(17,17))     
    #print(mat.shape)
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
    print ("Init states:", initStates)
    
    
    # on localise tous les objets ramassables
    #goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    #print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    # et la zone de jeu pour le tic-tac-toe
    tictactoeStates = [(x,y) for x in range(3,16) for y in range(3,16)]
    #print ("Wall states:", wallStates)
    print(tictactoeStates)
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
        
        
    
    
    
    #-------------------------------
    # Boucle principale de déplacements, un joueur apres l'autre
    #-------------------------------
    
    posPlayers = initStates

    tour = 0    
    j = 0 # le joueur 0 commence
    # on place la premiere fiole jaune      

    fiole_a_ramasser = put_next_fiole(0,tour)    
    print(posPlayers[0])
    print(fiole_a_ramasser)
    #print(mat)
    p2 = ProblemeGrid2D(posPlayers[0],fiole_a_ramasser,mat,'manhattan')
    noeudFinal = probleme.astar(p2)
    
    chemin = []    
    
    pere = noeudFinal
    while pere.etat != posPlayers[0]:
        chemin.append(pere.etat)
        pere = pere.pere
    
    print(chemin)
    
    
    for i in range(iterations):        
        row,col = posPlayers[j]

        for pos in reversed(chemin):
            row = pos[0]
            col = pos[1]
            players[j].set_rowcol(row, col)
            
           # print ("pos :", j, next_row,next_col)
            game.mainiteration()

            posPlayers[j]=(row,col)
        
        #o = players[j].ramasse(game.layers) # on la ramasse
        game.mainiteration()
        #print ("Objet de couleur ", couleur(o), " trouvé par le joueur ", j)
            
        # ici il faudrait aller la mettre a la position choisie
        # pour jouer a ultimate tic-tac-toe
        # et verifier que la position est legale etc.            
            
            
        # on active le joueur suivant
        # et on place la fiole suivante
        j = (j+1)%2     
        if j == 0:
            tour+=1
        
        fiole_a_ramasser=put_next_fiole(j,tour)    
    
                
        #break"""
    
            
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


