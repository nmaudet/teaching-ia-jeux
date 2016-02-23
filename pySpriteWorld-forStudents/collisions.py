import pygame
import random
from itertools import chain

class CollisionHandler:
    pixel_perfect = True  # calls pixel_collision otherwise box_collision

    def __init__(self, screen):
        self.mask = pygame.mask.from_surface(screen)
        self.mask.clear()

    def draw_sprite(self, spr, backup=False):
        self.mask.draw(spr.mask, spr.get_pos(backup))

    def erase_sprite(self, spr, backup=False):
        self.mask.erase(spr.mask, spr.get_pos(backup))

    def collide_sprite(self, spr, backup=False):
        return self.mask.overlap(spr.mask, spr.get_pos(backup))

    def fill_with_group(self, group, backup=False):
        self.mask.clear()
        for spr in group:
            self.mask.draw(spr.mask, spr.get_pos(backup))

    ###############  compute collision ###################


    def handle_collision(self, gDict, player):
        """ dispatches among all collision detection algorithms
        """
        if len(gDict["joueur"] ) > 1 or gDict["personnage"]:
            self.handle_pixel_collisions_many_players(gDict)
        else:
            if CollisionHandler.pixel_perfect:
                self.handle_pixel_collisions_single_player(gDict, player)
            else:
                self.handle_box_collisions_single_player(gDict, player)

    def out_of_screen(self, player):
        w, h = self.mask.get_size()
        w -= player.rect.w
        h -= player.rect.h
        return player.rect.x > w or player.rect.x < 0 or player.rect.y > h or player.rect.y < 0


    def handle_box_collisions_single_player(self, gDict, player):
        block_hit_list =  pygame.sprite.spritecollide(player, chain(gDict["obstacle"] , gDict["personnage"]), False)
        if block_hit_list or self.out_of_screen(player):
            player.resume_to_backup()

    def handle_pixel_collisions_single_player(self, gDict, player):
        # computes collisions mask of all obstacles (for pixel-based collisions)
        self.fill_with_group( chain(gDict["obstacle"] , gDict["personnage"]) )

        # send it to the player
        assert not self.collide_sprite(player, True), "sprite collision before any movement !!!"
        if self.collide_sprite(player) or self.out_of_screen(player):
            #print("COLLISION !!! in ",player.x,",",player.y)
            #print("resuming to ",player.backup_x,",",player.backup_y)
            #print("int coordinates:",player.rect.x,player.rect.y,player.)
            #print "\n\n"
            player.resume_to_backup()

    def handle_pixel_collisions_many_players(self, gDict):
        persos = list(gDict["joueur"])+list(gDict["personnage"])
        random.shuffle(persos)

        self.fill_with_group(gDict["obstacle"])

        # test if sprites at backup position do not collide anything and draw them on the mask
        for j in persos:
            assert not self.collide_sprite(j, True), "sprite collision before any movement !!!"
            self.draw_sprite(j, backup=True)

        # try their new position one by one
        for j in persos:
            self.erase_sprite(j, backup=True)
            if self.collide_sprite(j) or self.out_of_screen(j):
                j.resume_to_backup()
            self.draw_sprite(j)


    def get_box_collision_list(self, groupe, player):
        """ attention, la fonction ne teste pas la sortie d'ecran """
        return pygame.sprite.spritecollide(player, groupe, False)
