# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:32:05 2016

@author: nicolas
"""

import numpy as np
import copy
import heapq
import probleme
from probleme import Probleme



def distManhattan(p1,p2):
    """ calcule la distance de Manhattan entre le tuple 
        p1 et le tuple p2
        """
    (x1,y1)=p1
    (x2,y2)=p2
    return abs(x1-x2)+abs(y1-y2) 

def randomPuzzle(n):
    """
    genere un taquin aléatoire de taille n
    """
    tiles = np.random.permutation(range(0,n**2)) # 0 is the empty slot
    puzzle = np.array(tiles)
    puzzle = np.reshape(puzzle,(n, n))
    return puzzle



    

###############################################################################


class ProblemeTaquin(Probleme): 
    """ On definit un probleme de taquin comme étant: 
        - un état initial du taquin
        - un état but du taquin
        - une heuristique (supporte nombre de tiles, Manhattan, uniforme)
        """
    
    def __init__(self,init,but,heuristique):
        self.init=init
        self.but=but
        self.heuristique=heuristique
    
    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            toujours 1 pour le taquin
            """
        return 1
        
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        return (self.but==e).all()
    
    def calculManhattan(self,t1,t2):
        """ calcule la somme des distances de Manhattan entre 
            deux taquins t1 et t2
            """
        (s,_) = t1.shape
        sommeMan = 0
        for i in range(s): 
            for j in range(s):
                tile = t1[i][j]
                ([x],[y]) = np.where(t2==tile)      # where retourne les coord
                sommeMan += distManhattan((i,j),(x,y))
        return sommeMan  
        
    def calculPieces(self,e1,e2):
        """ au moins sommePieces doient etre déplacés pour arriver au but
            """
        (s,_) = e1.shape
        sommePieces=0
        for i in range(s): 
            for j in range(s):
                if e1[i][j] != e2[i][j]:
                    sommePieces+=1
        return sommePieces
        
    def h_value(self,e1,e2):
        """ applique l'heuristique pour le calcul 
            """
        if self.heuristique=='manhattan':
            h = self.calculManhattan(e1,e2)
        elif self.heuristique=='pieces':
            h = self.calculPieces(e1,e2)
        elif self.heuristique=='uniform':
            h = 1
        return h
        
    
        
    def slide(self,t1,direction):
        """ 
        dans le taquin t1    
        la case vide échange avec une autre case indiquee par direction (g,d,h,b)
            """
        t2 = copy.copy(t1)
        ([zx],[zy]) = np.where(t1==0)       # on localise la case vide
        (ech1,ech2)=(zx,zy)                 # par défaut échange avec même case 
        (s,_) = t1.shape
        if direction=='g' and zy>0:
            (ech1,ech2)=(zx,zy-1)
        elif direction=='d' and zy<s-1:
            (ech1,ech2)=(zx,zy+1)
        elif direction=='h' and zx>0:
            (ech1,ech2)=(zx-1,zy)
        elif direction=='b' and zx<s-1:
            (ech1,ech2)=(zx+1,zy)
        t2[zx][zy]=t2[ech1][ech2]
        t2[ech1][ech2]=0
        return t2
        
    def successeurs(self,etat):
        """ retourne une liste avec les taquins successeurs possibles
            """
        directions = ('g','d','h','b')
        etatsApresSlides =[]
        for dir in directions:
            p = self.slide(etat,dir)
            if (p!=etat).any(): # si le puzzle n'a pas été modifié on n'ajoute pas
                etatsApresSlides.append(p)
        return etatsApresSlides
        
    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        s=""
        for l in etat:
            for c in l:  
                s+=str(c)
        return s
            
    

        


            
###############################################################################
# Tests
###############################################################################
      


#puzzle1 = randomPuzzle(3)
#puzzle2 = randomPuzzle(3)


'''
puzzle1 = np.array(([2,1,6,4,0,8,7,5,3]))
puzzle2 = np.array(([1,2,3,8,0,4,7,6,5]))


puzzle1 = np.reshape(puzzle1,(3,3))
puzzle2 = np.reshape(puzzle2,(3,3))


p1 = ProblemeTaquin(puzzle1,puzzle2,'manhattan')
print ("=------------------------------=")
print ("Heuristique:",  p1.heuristique)
print ("Etat initial:\n", puzzle1)
print ("Etat but:\n", puzzle2)
print ("=------------------------------=")
print ("Solution:\n")

#probleme.astar(p1,True)
probleme.idastar(p1,True)
'''





