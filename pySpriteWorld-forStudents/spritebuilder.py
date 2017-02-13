from spritesheet_functions import SpriteSheet
import json
import glo
import pygame
from collections import OrderedDict
from sprite import MySprite,MovingSprite,RecursiveDrawGroup
from players import Player
import os
import zlib

class SpriteBuilder(object):
    '''
        cette classe charge le fichier TMX decrivant la carte du monde
        ensuite, elle cree des sprites et des groupes de sprites

        Remarque: dans le fichier TMX, il y a le nom du fichier image des sprites,
                  qui est charge aussi par la fonction load_sprite_sheet()
    '''




    def __init__(self, file_name):
        ''' (1) charge le fichier TMX
            (2) charge le fichier image ou se trouvent les sprites dans l'objet sheet
        '''

        self.carte    = None                 # json data from file
        self.sheet    = None                 # SpriteSheet object
        self.spritesize = 0                  # sprite size in pixels (assume its a square)
        self.rowsize,self.colsize = None,None# number of sprites in a row , column

        dirname = os.path.dirname(os.path.abspath(__file__))

        with open(dirname + "/" + file_name, 'r') as f:
            self.carte = json.load(f)

        assert self.carte["tilewidth"]==self.carte["tileheight"], "les sprites doivent etre carres"

        self.spritesize               = self.carte["tilewidth"]
        self.rowsize , self.colsize   = self.carte["width"],self.carte["height"]
        
        # print (self.carte["tilesets"][0]["image"])

        try:
            sheet_filename  = dirname + "/" + self.carte["tilesets"][0]["image"]
            self.sheet      = SpriteSheet(sheet_filename,self.spritesize)
        except pygame.error:
            try:
                sheet_filename  = dirname + "/Cartes/" + self.carte["tilesets"][0]["image"]
                self.sheet      = SpriteSheet(sheet_filename,self.spritesize)
            except pygame.error as e2:
                print ("Error - impossible de trouver le fichier images des sprites -")
                raise e2

    def prepareSprites(self):
        self.sheet.convert_sprites()


    def buildGroups(self):
        """ builds one group of sprites for each layer """

        # build ordered dictionary - first add groups from glo.ALL_LAYERS, with correct order

        Grps = OrderedDict( [(gr,self.basicGroupFactory(gr)) for gr in glo.ALL_LAYERS])

        for l in self.carte["layers"]:
            layername = l["name"].rstrip('s')
            if layername not in Grps:
                Grps.update( {layername:self.basicGroupFactory(layername) } )

            g = Grps[layername]
            dat = l["data"]
            if "compression" in l:
                assert l["compression"] == "zlib"
                # algo super-moche pour decompresser et decoder les donnees dat
                dat2 = dat.decode('base64').decode('zlib')
                dat3 = [dat2[i*4:i*4+4]for i in range(len(dat2)//4)]
                dat  = map(lambda x: ord(x[0])+256*ord(x[1])+256**2*ord(x[2])+256**3*ord(x[3]),dat3)

            for idx,e in enumerate(dat):
                y,x = (idx // self.rowsize)*self.spritesize , (idx % self.rowsize)*self.spritesize
                #if (e > 0 and  64<=x<=200 and 64<=y<=200) or (layername=='joueur' and e > 0):
                if e > 0:
                    s = self.basicSpriteFactory( layername , self.sheet.get_row_col(e-1) , x,y , self.sheet[e-1])
                    Grps[layername].add(s)
        return Grps

    ##########  Methodes a surcharger pour adapter la classe ##########
    def basicPlayerFactory(self,tileid=None,x=0.0,y=0.0,img=None):
            assert not img is None
            return Player("joueur",tileid,x,y,[img])

    def basicSpriteFactory(self , layername,tileid,x,y,img=None):
        if img is None: img = self.sheet[tileid]

        if layername == "joueur":
            return self.basicPlayerFactory(tileid,x,y,img)

        elif layername in ["ramassable","cache","personnage"]:
            return MovingSprite(layername,tileid,x,y,[img])
        else:
            return MySprite(layername,tileid,x,y,[img])

    def basicGroupFactory(self,layername):
        if layername in ["eye_candy","joueur"]:
            return RecursiveDrawGroup()
        else:
            return pygame.sprite.Group()

    ##################################################################
