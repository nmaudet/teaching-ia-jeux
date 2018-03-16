import pygame
import pygame.sprite
import random
from itertools import chain
import fast_rect_collision
from sprite import MovingSprite

class CollisionHandler2:
    pixel_perfect = True             # calls pixel_collision otherwise box_collision
    allow_overlaping_players = True

    def __init__(self, screen,spritesize):
        self.mask_obstacles = pygame.mask.from_surface(screen)
        self.mask_players   = pygame.mask.from_surface(screen)

        self.mask_obstacles.clear()
        self.mask_players.clear()

        wh = max( screen.get_width() , screen.get_height() )
        self.fastGroupCollide = fast_rect_collision.FastGroupCollide(group={},display_size=wh,max_interv=spritesize)


    def erase_player_mask(self, spr, backup=False):
        self.mask_players.erase(spr.mask, spr.get_pos(backup))

    def draw_player_mask(self, spr, backup=False):
        self.mask_players.draw(spr.mask, spr.get_pos(backup))

    def collide_player_w_players(self, spr, backup=False):
        return self.mask_players.overlap(spr.mask, spr.get_pos(backup))

    def collide_player_w_obstacles(self, spr, backup=False):
        return self.mask_obstacles.overlap(spr.mask, spr.get_pos(backup))

    def fill_with_obstacles(self, group, backup=False):
        self.mask_obstacles.clear()

        for spr in group:
            self.mask_obstacles.draw(spr.mask, spr.get_pos(backup))

    #### Interface to fastGroupCollide
    def _filter_by_layername(self,lst,layernames=None):
        return [s for s in lst if (layernames is None or s.layername in layernames)]

    def add_or_update_sprite(self,spr):
        self.fastGroupCollide.add_or_update_sprite(spr)

    def remove_sprite(self,spr):
        self.fastGroupCollide.remove_sprite(spr)

    def sprites_on_tile(self,i,j,group_filter=None):
        l = self.fastGroupCollide.get_all_sprites_on_tile(i,j)
        return self._filter_by_layername(l,group_filter)

    def collision_list(self,s,group_filter=None):
        l = self.fastGroupCollide.compute_collision_list(s,pygame.sprite.collide_mask)
        return self._filter_by_layername(l,group_filter)

    def collision_blocking_player(self,s):
        blockinglayers = {'obstacle'} if self.allow_overlaping_players else {'obstacle','joueur'}
        return self.collision_list(s,blockinglayers)

    def collision_with_point(self,x,y,group_filter):
        s = PointSprite(x=x,y=y)
        return self.collision_list(s,group_filter)

    ###############  compute collision ###################

    def handle_collision(self, gDict,_safe_collision=True):

        persos = list(gDict["joueur"])

        allow_overlap = CollisionHandler2.allow_overlaping_players
        multi_player_and_not_allow_overlap = len(persos)>1 and not allow_overlap

        random.shuffle(persos)

        self.fill_with_obstacles(gDict["obstacle"])
        self.mask_players.clear()

        # test if sprites at backup position do not collide anything and draw them on the mask
        for j in persos:
            if _safe_collision:
                assert not self.collide_player_w_obstacles(j, backup=True), "sprite collision with obstacles before any movement !!!"
                if multi_player_and_not_allow_overlap:
                    assert not self.collide_player_w_players(j, backup=True), "sprite collision before any movement !!!"
                    self.draw_player_mask(j, backup=True)

        # try their new position one by one

        for j in persos:

            if multi_player_and_not_allow_overlap: self.erase_player_mask(j, backup=True)

            c1 = self.collide_player_w_obstacles(j)
            c2 = self.collide_player_w_players(j)


            if c1 or (c2 and not allow_overlap) or self.out_of_screen(j):
                j.resume_to_backup()

            self.draw_player_mask(j)

        # Update fastGroupCollide object
        good_layernames = set(gDict) - {'bg1','bg2','dessinable','eye_candy'}
        for layername in good_layernames:
            for spr in gDict[layername]:
                self.fastGroupCollide.add_or_update_sprite(spr)

        MovingSprite.up_to_date = True


    def out_of_screen(self, player):
        w, h = self.mask_obstacles.get_size()
        w -= player.rect.w
        h -= player.rect.h
        return player.rect.x > w or player.rect.x < 0 or player.rect.y > h or player.rect.y < 0





''' UNUSED CODE :

    self._collision_lock = None # if not None, then cannot call 'handle_collision'
                                # allows external functions to use self.mask,
                                # without risking this mask to be modified by handle_collision

    def capture_lock(self,name):
        assert self._collision_lock is None
        self._collision_lock = name

    def release_lock(self,name):
        assert self._collision_lock == name
        self._collision_lock = None

    self.capture_lock('handle_collision')
    self.release_lock('handle_collision')

'''