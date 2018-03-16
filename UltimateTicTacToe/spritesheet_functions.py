"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame
import glo


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """


    def __init__(self, file_name,_spritesize):
        """ Constructor. Pass in the file name of the sprite sheet. """
        # Load the sprite sheet and set some variables


        # This points to our sprite sheet image
        self.sprite_sheet    = None
        # size of a sprite (nb of columns or nb of rows)
        self.spritesize      = None
        # number of sprites in a row , column
        self.rowsize,self.colsize = None,None
        # list of sprite images of type pygame.surface (in a bottom to down and left to right order)
        self.sprite_images   = []


        self.sprite_sheet = pygame.image.load(file_name)
        self.spritesize   = _spritesize
        w , h             = self.sprite_sheet.get_width() , self.sprite_sheet.get_height()
        self.rowsize =  w // _spritesize
        self.colsize =  h // _spritesize

        assert  (self.rowsize*_spritesize ==  w) and (self.colsize*_spritesize == h) , \
                "le spritesheet a une taille incorrecte"


        for i in range(0,h,_spritesize):
            for j in range(0,w,_spritesize):
                img = self.get_image(j,i,_spritesize,_spritesize)
                self.sprite_images.append( img )



    def get_image(self, x, y, width, height):
        """
        Grab a single image out of a larger spritesheet
        Pass in the x, y location of the sprite
        and the width and height of the sprite.
        """

        # Create a new blank image
        image = pygame.Surface([width, height])
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # Assuming black works as the transparent color
        image.set_colorkey(glo.BLACK)
        # Return the image
        return image


    def convert_sprites(self):
        try:
            self.sprite_images = [img.convert() for img in self.sprite_images]
        except pygame.error as e:
            print( "-- Erreur: il faut initialiser pygame avec pygame.display.set_mode(...) AVANT d'utiliser la fonction pygame convert(...) --")
            print ("-- sinon, pygame ne saura pas dans quelle resolution convertir les bitmaps --")
            raise e


    def get_row_col(self,idx):
        return int(idx / self.rowsize) , int(idx % self.rowsize)


    def __getitem__(self,idx):
        '''     either call self[k] or self[(i,j)] to get image of the k^th sprite
                or sprite at row i and column j
        '''
        if isinstance(idx,tuple):
            i,j = idx
            return self.sprite_images[int(i*self.rowsize + j)]
        else:
            return self.sprite_images[idx]
