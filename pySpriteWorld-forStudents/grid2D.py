# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:32:05 2016

@author: nicolas
"""

import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod
import probleme
from probleme import Probleme




def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2) 


    
###############################################################################


class ProblemeGrid2D(Probleme): 
    """ On definit un probleme de labyrithe comme étant: 
        - un état initial
        - un état but
        - une grid, donné comme un array booléen (False: obstacle)
        - une heuristique (supporte Manhattan, euclidienne)
        """ 
    def __init__(self,init,but,grid,heuristique):
            self.init=init
            self.but=but
            self.grid=grid
            self.heuristique=heuristique
        
    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            toujours 1 pour le taquin
            """
        return 1
        
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        return (self.but==e)
        
    def estObstacle(self,e):
        """ retorune vrai si l'état est un obsacle
            """
        return (self.grid[e]==False)
        
    def estDehors(self,etat):
        """retourne vrai si en dehors de la grille
            """
        (s,_)=self.grid.shape
        (x,y)=etat
        return ((x>=s) or (y>=s) or (x<0) or (y<0))

    
        
    def successeurs(self,etat):
            """ retourne des positions successeurs possibles
                """
            current_x,current_y = etat
            d = [(0,1),(1,0),(0,-1),(-1,0)]
            etatsApresMove = [(current_x+inc_x,current_y+inc_y) for (inc_x,inc_y) in d]
            return [e for e in etatsApresMove if not(self.estDehors(e)) and not(self.estObstacle(e))]

    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        s=""
        (x,y)= etat
        s+=str(x)+str(y)
        return s
        
    def h_value(self,e1,e2):
        """ applique l'heuristique pour le calcul 
            """
        if self.heuristique=='manhattan':
            h = distManhattan(e1,e2)
        elif self.heuristique=='uniform':
            h = 1
        return h


            
###############################################################################
# Tests
###############################################################################
      

'''
#puzzle1 = randomPuzzle(3)
#puzzle2 = randomPuzzle(3)

puzzle1 = np.array(([2,1,6,4,0,8,7,5,3]))
puzzle2 = np.array(([1,2,3,8,0,4,7,6,5]))


puzzle1 = np.reshape(puzzle1,(3,3))
puzzle2 = np.reshape(puzzle2,(3,3))


p1 = ProblemeTaquin(puzzle1,puzzle2,'manhattan')
print "=------------------------------="
print "Heuristique:",  p1.heuristique
print "Etat initial:\n", puzzle1
print "Etat but:\n", puzzle2
print "=------------------------------="
print "Solution:\n"

astar(p1)
#idastar(p1)
'''

g = np.array((
[True,True,True,True,True,True],
[True,True,False,True,True,True],
[True,True,False,False,False,True],
[True,True,True,True,True,True],
[True,True,False,True,False,False],
[True,True,False,True,True,True]))

p2 = ProblemeGrid2D((0,2),(5,4),g,'manhattan')

probleme.astar(p2)




