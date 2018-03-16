# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 09:23:57 2016

@author: personne
"""
from __future__ import division,print_function
import numpy as np

"""

TODO:
- spécifier dans les sprites la liste des layers qui constituent des obstacles pour eux


- les collisions:
    soit on définit une propriété "blocking_collision" qui empeche tout sprite ayant cette propriété d'entrer en collision avec un autre.

le layer player ne doit pas entrer en collision avec des sprites d'obstacle ou player
ET C'EST TOUT !!!
toutes les autres collisions doivent être gérées manuellement.

on pourrait pour chaque sprite, avoir une liste:
   'blocking collision' (liste de layers)
   'alerting collision' (messages si collision)

idée: les 'blocking collisions' se font en O(n) et les autres en O(n^2)


Donc, on a les pixels-perfect collisions, seulement entre players et players+obstacles

Il faut une fonction qui check la pixel-perfect collision entre 2 sprites
Il faut une fonction qui check la pixel-perfect collision entre un point et un sprite (pour le laser)
"""

'''
In 2D, much better than naive O(n^2) algorithm, but not as good as O(n.log n)
Probably of order O(n^1.5) asymptotically.

Let k be the average number of collisions
If data is randomly and uniformly distributed, and rectangles have same width and height, then:
    If data is very sparse, then the Projection-Based is O(n.log n) and Dict-Based is O(n)
    If data is very dense,  then the projection-Based is O(n^1.5)   and Dict-Based is O(nk)

'''

import random
from collections import defaultdict
import numpy as np
import itertools

try:
    import cython
    cython_compiled = cython.compiled
except:
    cython_compiled = False




'''
ATTENTION !!!
DANS PYGAME, LES RECTANGLES
ont des coordonnees top,left,right,bottom,
mais on considere que le cote bas (bottom) et droite (right) sont à un pixel de moins.
Donc un carre 32x32 commencant en 0,0 aura les champs:
top=0
left=0
right=32  (et non pas 31)
bottom=32 (idem)
'''

class cyRectSprite:
    '''
    structure to store sprite location and access it fast, through cython (if available)
    '''
    def __init__(self,s,backup=False):
        self.sprite=s
        self.spriteid = id(s)

        if backup:
            self.top   = int(s.backup_y)
            self.left  = int(s.backup_x)
            self.right = self.left + s.rect.w
            self.bottom= self.top  + s.rect.h
        else:
            self.top=s.rect.top
            self.left=s.rect.left
            self.right=s.rect.right
            self.bottom=s.rect.bottom

    def size(self):
        h = self.bottom - self.top
        w = self.right - self.left
        return h if h > w else w

    def well_formed(self,maxspritesize,screensize):

        #print('rect=',self.right,self.left,self.top,self.bottom)
        #print(self.right > self.left,\
        #		self.bottom > self.top,\
        #		self.size() <= maxspritesize, \
        #		self.left >= 0 and self.top >= 0, \
        #		self.right <= screensize and self.bottom <= screensize)
        #print('sizes=',self.size(), maxspritesize)

        return self.right > self.left and \
               self.bottom > self.top and \
               self.size() <= maxspritesize





class FastGroupCollide:
    def __init__(self,group,display_size=1024,max_interv=None):
        '''
        parameters:
        group must be a container objects (e.g. sprites), each having a rect attribute,
        and rect attributes mush have left,top,bottom,right attributes
        max_interv must be None or the max size of sprites.
        '''
        if max_interv is None:
            self.max_interval = max( cyRectSprite(s).size() for s in group )
        else:
            self.max_interval = max_interv

        self.display_size = display_size
        # build a 2D numpy array of empty lists
        # of dimension array_size*array_size
        self.array_size  = 1 + display_size // self.max_interval
        self.array = np.empty( (self.array_size,self.array_size) , dtype=object , order='C')
        for i,j in itertools.product(range(self.array_size),range(self.array_size)):
            self.array[i,j] = []

        self.ref = {}
        for s in group: self.add_or_update_sprite(s)


    def _get_list(self,cys):
            i = cys.top  // self.max_interval
            j = cys.left // self.max_interval
            if i >= 0 and j >= 0 and i < self.array_size and j < self.array_size:
                return self.array[i,j]
            else:
                return None

    def _unsafe_add_cyRectSprite(self,cys,l):
            #print('!!!adding ',cys.spriteid)
            self.ref[cys.spriteid] = [l,len(l)]
            l.append( cys )

    def _add_cyRectSprite(self,cys,l=None):
            assert  cys.well_formed(self.max_interval,self.display_size), \
                    'error: sprite rect is not consistent. Probably sprite bigger than declared'
            assert cys.spriteid not in self.ref, 'error: trying to add sprite already in set'

            if l is None:
                l = self._get_list(cys)
                if l is None:
                    return
            self._unsafe_add_cyRectSprite(cys,l or self._get_list(cys))


    def remove_sprite(self,s):
        try:
            # removal will still work even if sprite has changed coords
            # because old coords have been store in self.ref
            #
            # To remove a sprite s:
            # 	- First remove it from the list l=self.d[ij]
            # 	  To achieve this quickly, let k be the position in the list of the sprite
            # 	  copy the last element to l[k] and pop the last element
            # 	- Finally, remove this sprite from self.ref
            ref = self.ref
            id_s = id(s)
            l,k = ref[id_s]
            last = l[-1]
            #print('%%%%%%%% l[k],last=',l[k].spriteid,last.spriteid)
            #print('%%%%%%%% id_s=',id_s)
            l[k] = last
            l.pop()
            ref[last.spriteid][1] = k
            del ref[id_s]
        except AttributeError:
            raise AttributeError('trying to remove sprite absent from list')

    def add_or_update_sprite(self,s,backup=False):
        cys = cyRectSprite(s,backup)
        id_s = id(s)
        new_l = self._get_list(cys)
        if id_s in self.ref:
            old_l = self.ref[id_s][0]
            if id(old_l) == id(new_l):
                return
            self.remove_sprite(s)
        if new_l is not None:
            self._add_cyRectSprite(cys,new_l)


    def _compute_collision_list(self,l,t,r,b,s=None,collision_callback=None):
        '''
        params:
        left,top,right,bottom (of a rectanble), sprite,callback
        '''
        candidates = []

        i = t // self.max_interval
        j = l // self.max_interval
        id_s = -1 if s is None else id(s)

        for di in range(i-1,i+2):
            for dj in range(j-1,j+2):
                if di >= 0 and dj >= 0 and di < self.array_size and dj < self.array_size:
                    lst2 = self.array[di,dj]
                    for s2 in lst2:
                        if s2.right <= l or s2.left >= r or s2.top >= b or s2.bottom <= t:
                            continue

                        if s2.spriteid != id_s:
                            if (collision_callback is None) or (s is None) or collision_callback(s,s2.sprite):
                                candidates.append( s2.sprite )
        return candidates


    def compute_collision_list(self,s,collision_callback=None):
        rec = s.rect
        l,t,r,b = rec.left,rec.top,rec.right,rec.bottom
        return self._compute_collision_list(l,t,r,b,s,collision_callback)

    def compute_collision_with_point(self,x,y):
        return self._compute_collision_list(x,y,x+1,y+1)


    def get_all_sprites_on_tile(self,i,j):
        return [cys.sprite for cys in self.array[i,j] ]

