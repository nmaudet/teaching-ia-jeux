# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:32:05 2016

@author: nicolas
"""

import numpy as np
import copy
import heapq
from abc import ABCMeta, abstractmethod
import functools
import time



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
    """ On definit un probleme comme étant: 
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

@functools.total_ordering # to provide comparison of nodes
class Noeud:
    def __init__(self, etat, g, pere=None):
        self.etat = etat
        self.g = g
        self.pere = pere
        
    def __str__(self):
        #return np.array_str(self.etat) + "valeur=" + str(self.g)
        return str(self.etat) + "valeur=" + str(self.g)
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __lt__(self, other):
        return str(self) < str(other)
        
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
            print (n)
            n = n.pere
            c+=1
        print ("Nombre d'étapes de la solution:", c-1)
        return            
        
        
###############################################################################


def astar(p,verbose=False,stepwise=False):
    """
    application de l'algorithme a-star
    sur un probleme donné
        """
        
    startTime = time.time()

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
        
        stop_stepwise=""
        if stepwise==True:
            stop_stepwise = input("Press Enter to continue (s to stop)...")
            print ("best", min_f, "\n", bestNoeud)
            print ("Frontière: \n", frontiere)
            print ("Réserve:", reserve)
            if stop_stepwise=="s":
                stepwise=False
    
    bestNoeud.trace(p)          
            
    # Mode verbose            
    # Affichage des statistiques (approximatives) de recherche   
    #
    if verbose:
        print ("=------------------------------=")
        print ("Nombre de noeuds explorés", len(reserve))
        c=0
        for (f,n) in frontiere:
            if p.immatriculation(n.etat) not in reserve:
                c+=1
        print ("Nombre de noeuds de la frontière", c)
        print ("Nombre de noeuds en mémoire:", c + len(reserve))
        print ("temps de calcul:", time.time() - startTime)
        print ("=------------------------------=")

    return


###############################################################################
# ITERATIVE DEEPENING A*
###############################################################################


def idastar(p,verbose=False,stepwise=False):
    """ application de l'algorithme iterative deepening A*
        sur un probleme donné
        """
        
    startTime = time.time()
    
    nodeInit = Noeud(p.init,0,None)
    MaxSeuil=1000
    
    front = [(nodeInit,1)]
    seuil = p.h_value(nodeInit.etat,p.but)
    nextSeuil = MaxSeuil
    
    nb_noeuds = 0
   
    while not (front==[] and nextSeuil==MaxSeuil) : 
        
        #print "frontiere", front
        #raw_input("Press Enter to continue...")

        if front==[]:
            if stepwise:
                    print("Augmentation du seuil:",nextSeuil)
            seuil = nextSeuil
            nextSeuil = MaxSeuil
            nodeInit = Noeud(p.init,0,None)
            front = [(nodeInit,1)]
        (m,k) = front[-1]
        
        
        if p.estBut(m.etat): 
            print ("Solution trouvée")
            break
        
    
        while True: 
            nextNoeud = m.expandNext(p,k)
            nb_noeuds +=1
            if (nextNoeud,) not in front:
                if stepwise:
                    print (nextNoeud)
                    print ("fils num. k:",k)
                break
            else:
                k+=1
        
        if nextNoeud == []:                 # si pas de noeud à étendre, on pop
            if front!=[]:
                 front.pop()     
        else:
            f = nextNoeud.g+p.h_value(nextNoeud.etat,p.but)
            if stepwise:
                print ("valeur f:", f)
                print ("seuil:", seuil)
            if f <= seuil:                     
                front.pop()
                front.append((m,k+1))           # en se souvenant du prochain fils de m a d
                front.append((nextNoeud,1))     # on continue la recherche
            else:
                nextSeuil = min(nextSeuil,f)    # augmentation du seuil prochain
                front.pop()                     # 
                front.append((m,k+1))
                if stepwise:
                    #print("Augmentation du seuil:",nextSeuil)
                    input("Press Enter to keep exploring")
                
                
    # Affichage de la solution
    n = m
    c=0    
    while n!=None :
        print (n)
        n = n.pere
        c+=1
    print ("Nombre d'étapes de la solution:", c-1)  

            
    # Mode verbose    
    # Affichage des statistiques de recherche
    if verbose:
        print ("=------------------------------=")
        print ("Nombre de noeuds étendus", nb_noeuds)
        #c=0
        #for n in front:
        #    if p.immatriculation(n.etat) not in closed:
        #        c+=1
        print ("Nombre de noeuds en mémoire", len(front))
        print ("temps de calcul:", time.time() - startTime)
        print ("=------------------------------=")

    
    return
    

            

