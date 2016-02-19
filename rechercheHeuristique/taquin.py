# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:32:05 2016

@author: nicolas
"""

import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod




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

class Probleme(object):
    """ On definit un probleme de taquin comme étant: 
        - un état initial
        - un état but
        - une heuristique
        """
        
    def __init__(self,init,but,heuristique):
        self.init=init
        self.but=but
        self.heuristique=heuristique
        
    @abstractmethod
    def estBut(self,e):
        """ retourne vrai si l'état e est un état but
            """
        pass
        
    @abstractmethod    
    def cost(self,e1,e2):
        """ donne le cout d'une action entre e1 et e2, 
            """
        pass
        
    @abstractmethod
    def successeurs(self,etat):
        """ retourne une liste avec les successeurs possibles
            """
        pass
        
    @abstractmethod
    def immatriculation(self,etat):
        """ génère une chaine permettant d'identifier un état de manière unique
            """
        pass
    
    

###############################################################################


class ProblemeTaquin(Probleme): 
    """ On definit un probleme de taquin comme étant: 
        - un état initial
        - un état but
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
    
    
class Noeud:
    def __init__(self, etat, g, pere=None):
        self.etat = etat
        self.g = g
        self.pere = pere
        
    def __str__(self):
        return np.array_str(self.etat) + "valeur=" + str(self.g)
        
    def expand(self,p):
        """ étend un noeud avec ces fils
            pour un probleme de taquin p donné
            """
        nouveaux_fils = [Noeud(s,self.g+p.cost(self.etat,s),self) for s in p.successeurs(self.etat)]
        return nouveaux_fils
        
    def expandNext(self,p,k):
        """ étend un noeud unique, le k-ième fils du noeud n
            ou liste vide si plus de noeud à étendre
            """
        nouveaux_fils = self.expand(p)
        if len(nouveaux_fils)<k: 
            return []
        else: 
            return self.expand(p)[k-1]
            
    def trace(self,p):
        """ affiche tous les ancetres du noeud
            """
        n = self
        c=0    
        while n!=None :
            print n
            n = n.pere
            c+=1
        print "Nombre d'étapes de la solution:", c-1
        return            
        
        
###############################################################################


def astar(p,verbose=False):
    """
    application de l'algorithme a-star
    sur un probleme donné
        """
    nodeInit = Noeud(p.init,0,None)
    frontiere = [(nodeInit.g+p.h_value(nodeInit.etat,p.but),nodeInit)] 

    reserve = {}        
    bestNoeud = nodeInit
    
    while frontiere != [] and not p.estBut(bestNoeud.etat):              
        (min_f,bestNoeud) = heapq.heappop(frontiere)
           
    # VERSION 1 --- On suppose qu'un noeud en réserve n'est jamais ré-étendu
    # Hypothèse de consistence de l'heuristique        
        
        if p.immatriculation(bestNoeud.etat) not in reserve:            
            reserve[p.immatriculation(bestNoeud.etat)] = bestNoeud.g #maj de reserve
            nouveauxNoeuds = bestNoeud.expand(p)            
            for n in nouveauxNoeuds:
                f = n.g+p.h_value(n.etat,p.but)
                heapq.heappush(frontiere, (f,n))

    # TODO: VERSION 2 --- Un noeud en réserve peut revenir dans la frontière        
        
 
        if verbose==True:
            raw_input("Press Enter to continue...")
            print "best", min_f, "\n", bestNoeud
            print "Frontière: \n"        
            print frontiere
            print "Réserve:", reserve
    
    bestNoeud.trace(p)          
            
            
    # Affichage des statistiques (approximatives) de recherche   
    print "=------------------------------="
    print "Nombre de noeuds explorés", len(reserve)
    c=0
    for (f,n) in frontiere:
        if p.immatriculation(n.etat) not in reserve:
            c+=1
    print "Nombre de noeuds de la frontière", c
    print "=------------------------------="

    return
    


def idastar(p,verbose=False):
    """ application de l'algorithme iterative deepening A*
        sur un probleme donné
        """
    nodeInit = Noeud(p.init,0,None)
    MaxSeuil=1000
    
    front = [(nodeInit,1)]
    seuil = p.h_value(nodeInit.etat,p.but)
    nextSeuil = MaxSeuil
   
    while not (front==[] and nextSeuil==MaxSeuil) : 
        
        #print "frontiere", front
        #raw_input("Press Enter to continue...")

        if front==[]: 
            seuil = nextSeuil
            nextSeuil = MaxSeuil
            nodeInit = Noeud(p.init,0,None)
            front = [(nodeInit,1)]
        (m,k) = front[-1]
        
        
        if p.estBut(m.etat): 
            print "Solution trouvée"
            break
        
    
        while True: 
            nextNoeud = m.expandNext(p,k)
            if (nextNoeud,) not in front:
                print nextNoeud
                print "fils num. k:",k
                break
            else:
                k+=1
        
        if nextNoeud == []:                 # si pas de noeud à étendre, on pop
            if front!=[]:
                 front.pop()     
        else:
            f = nextNoeud.g+p.h_value(nextNoeud.etat,p.but)
            print "f:", f
            print "seuil:", seuil
            if f <= seuil:                     
                #print "yes"
                front.pop()
                front.append((m,k+1))           # en se souvenant du prochain fils de m a d
                front.append((nextNoeud,1))     # on continue la recherche
            else:
                nextSeuil = min(nextSeuil,f)    # augmentation du seuil prochain
                front.pop()                     # 
                front.append((m,k+1))
                
                
    # Affichage de la solution
    n = m
    c=0    
    while n!=None :
        print n
        n = n.pere
        c+=1
    print "Nombre d'étapes de la solution:", c-1   

            
            
    # Affichage des statistiques de recherche        
    #print "Nombre de noueds explorés", len(closed)
    #c=0
    #for n in front:
    #    if p.immatriculation(n.etat) not in closed:
    #        c+=1
    #print "Nombre de noueds de la frontière", c
    
    return
    

            
###############################################################################
# Tests
###############################################################################
      


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




