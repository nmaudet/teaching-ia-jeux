from __future__ import absolute_import, print_function, unicode_literals
from spritebuilder import SpriteBuilder
import glo
import pygame
from collections import OrderedDict
import random
from sprite import MySprite,MovingSprite
from functools import wraps
import copy
import os, sys

try:
    from toolz import first
except:
    def first(g): return next(iter(g))

from collisions2 import CollisionHandler2


def check_init_game_done(fun):
    """ decorator checking if init() has correctly been called before anything """
    @wraps(fun)
    def fun_checked(*args,**kwargs):
        try:
            Game.single_instance.screen
        except:
            raise Exception('Vous devez appeler la fonction init() avant toute chose')
        return fun(*args,**kwargs)
    return fun_checked


class Game(object):
    """ Design Pattern 'Singleton', so only one instance of Game can exist """
    single_instance = None
    def __new__(cls, *args, **kwargs):
        if cls.single_instance is None:
            cls.single_instance = object.__new__(cls, *args, **kwargs)

        return cls.single_instance


    def __init__(self, fichiercarte=None, _SpriteBuilder=None):
        # if no parameter is given, then __init__ will just create an empty Game object
        if fichiercarte is None or _SpriteBuilder is None:
            return

        #reset pygame
        pygame.quit() ; pygame.init()

        # callbacks is a dictionary of functions to call depending on key pressed
        self.callbacks = {}

        # charge la carte et le spritesheet
        self.spriteBuilder = _SpriteBuilder(fichiercarte)

        # cree la fenetre pygame
        self.screen = pygame.display.set_mode([self.spriteBuilder.spritesize * self.spriteBuilder.rowsize,
                                               self.spriteBuilder.spritesize * self.spriteBuilder.colsize])


        pygame.display.set_caption("pySpriteWorld Experiment")
        self.spriteBuilder.screen = self.screen

        self.fps = 60
        self.frameskip = 0
        # converti les sprites meme format que l'ecran
        self.spriteBuilder.prepareSprites()

        # cree un groupe de sprites pour chaque layer
        self.layers = self.spriteBuilder.buildGroups()
        pass
        # cherche le premier sprite joueur
        try:
            self.player = first(self.layers["joueur"])
        except Exception:
            raise IndexError("Je ne trouve aucun joueur dans le fichier TMX")

        # prepare le bitmap 'background'
        self.background = pygame.Surface([self.screen.get_width(), self.screen.get_height()]).convert()
        self.layers["bg1"].draw(self.background)
        self.layers["bg2"].draw(self.background)

        # cree un masque de la taille de l'ecran, pour le calcul des collisions
        self.mask = CollisionHandler2(self.screen,self.spriteBuilder.spritesize)

        # click clock
        self.clock = pygame.time.Clock()
        self.framecount = 0

    def setup_keyboard_callbacks(self):
        self.callbacks = self.player.gen_callbacks(self.player.rect.w, self.layers, self.mask)

    def update(self):
        self.mask.handle_collision(self.layers, self.player)

        for layer in glo.NON_BG_LAYERS:
            self.layers[layer].update()

    def draw(self):
        self.screen.blit(self.background, (0, 0), (0, 0, self.screen.get_width(), self.screen.get_height()))
        for layer in glo.NON_BG_LAYERS:
            if layer != "cache":
                self.layers[layer].draw(self.screen)


        pygame.display.flip()


    def kill_dessinable(self):
        while self.layers['dessinable']:
            first(self.layers['dessinable']).kill()
        while self.layers['eye_candy']:
            first(self.layers['eye_candy']).kill()

    def prepare_dessinable(self):
        if not self.layers['dessinable']:
            self.surfaceDessinable = pygame.Surface([self.screen.get_width(), self.screen.get_height()]).convert()
            self.surfaceDessinable.set_colorkey( (0,0,0) )
            self.layers['dessinable'].add( MySprite('dessinable',None,0,0,[self.surfaceDessinable]) )

    def mainiteration(self, _fps=None, _frameskip = None):
        if os.environ.get("SDL_VIDEODRIVER") != 'dummy': # if there is a real x-server
            if pygame.event.peek():
                for event in pygame.event.get():  # User did something
                    if event.type == pygame.QUIT:  # If user clicked close
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key in self.callbacks:
                            self.callbacks[event.key]()

        self.update()

        # call self.draw() once every 'frameskip' iterations
        fs = _frameskip if _frameskip is not None else self.frameskip
        self.framecount = (self.framecount+1) % (fs+1)
        if self.framecount==0:
            self.draw()
            self.clock.tick(_fps if _fps is not None else self.fps)


    def mainloop(self):
        while True:
            self.mainiteration()


    def populate_sprite_names(self,ontology):
        for layer in self.layers.values():
            for s in layer:
                s.firstname = ontology.firstname(s)


    def add_players(self,xy,player=None,tiled=True,draw_now=True):
        """
            Attemps to add one or many new players at position x,y
            Fails if the new player is colliding something, and then return False
            if success, then adds the new player to group of players and returns its reference
            :param xy:  either a tuple (x,y) of coordinates of the new sprite, either an iterable of tuples ((x1,y1),(x2,y2)...)
            :param player: an existing players or None. If not None, this function will use player.image for the new player
            :param tiled: if True, then x and y are not in pixel coordinates but tile coordinates
            :param draw_now: if True, then the main iteration loop is called
            :return: the list of sprites created successfully
            :example:
            >>> # Here, the attempt to create a new sprite fails because of collision
            >>> game.add_players( (2,3) , game.player )
            []
        """
        assert type(xy) is tuple
        x,y = xy

        if tiled:
            x,y = x*self.spriteBuilder.spritesize,y*self.spriteBuilder.spritesize

        try:
            tileid = player.tileid
        except:
            tileid = None

        if not MovingSprite.up_to_date:
            self.mask.handle_collision(self.layers)

        pnew = self.spriteBuilder.basicPlayerFactory(tileid,x=x,y=y)

        if self.mask.collision_blocking_player(pnew) == []:
            self.layers['joueur'].add( pnew )
            self.mask.draw_player_mask( pnew )
            self.mask.add_or_update_sprite( pnew )
            if draw_now: self.mainiteration()
            return pnew
        else:
            if draw_now: self.mainiteration()
            return False
