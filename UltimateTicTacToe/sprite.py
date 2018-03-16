import pygame
from math import pi,sqrt,cos,sin,floor
import polygons
import copy

class RecursiveDrawGroup(pygame.sprite.Group):
    """ Standard pygame.sprite.Group classes draw sprites by calling 'blit' on sprite images.
        Instead, this class calls 'draw' on each of its sprite """
    def draw(self,surf):
        for s in self:
            s.draw(surf)


class MySprite(pygame.sprite.Sprite):
    """ MySprite est un sprite qui connait l'image (ou les images) a afficher
    """

    def __init__(self,layername,tileid,x,y,imglist):
        pygame.sprite.Sprite.__init__(self)
        self.tileid = tileid # tileid identifie le sprite sur la spritesheet. Generalement, c'est le row/col dans le spritesheet
        self.imagelist = imglist
        self.masklist  = [pygame.mask.from_surface(im) for im in imglist]
        self.image = imglist[0]
        self.mask = self.masklist[0]
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = x,y
        #print("layername=",layername,"id = ",self.tileid)
    def dist(self,x,y):
        cx,cy = self.get_centroid()
        return sqrt( (cx-x)**2 + (cy-y)**2 )

    def get_pos(self,backup=False):
        assert backup==False , "erreur: tentative d'acces a backup_rect d'un sprite non mobile"
        return (self.rect.x,self.rect.y)

    def draw(self,surf):
        surf.blit(self.image,self.rect)
        
    def get_rowcol(self):
            assert int(self.rect.x) % self.rect.w == 0 and int(self.rect.y) % self.rect.h == 0, "sprite must not be accross tiles for this function"
            return int(self.rect.y) // self.rect.h , int(self.rect.x) // self.rect.w



class DrawOnceSprite(pygame.sprite.Sprite):
    """ DrawOnceSprite est un sprite qui va s'afficher pendant quelques frames, puis s'autodetruire
    """
    lifespan = 4
    def __init__(self,drawfun,arglist):
        pygame.sprite.Sprite.__init__(self)
        self.drawfun = drawfun
        self.arglist = arglist
        self.lifespan = DrawOnceSprite.lifespan

    def draw(self,surf):
        self.drawfun(surf,*self.arglist)
        self.lifespan -= 1
        if self.lifespan == 0:
            self.kill()



class MovingSprite(MySprite):

    """ Cette classe represente les sprites qui peuvent bouger (ex: player, creatures, deplacable)
        les coordonnees ne sont plus stockees dans self.rect comme dans MySprite,
        mais dans self.x,self.y sous forme de flottant.
    """

    # vecteur vitesse requis. Si collision, alors il ne se realisera pas

    def __init__(self,*args,**kwargs):
        MySprite.__init__(self,*args,**kwargs)
        self.x , self.y = self.rect.x , self.rect.y
        self.angle_degree  = 0
        self.backup()

    def backup(self):
        self.backup_x , self.backup_y = self.x , self.y
        self.backup_angle_degree = self.angle_degree
        self.backup_image = self.image
        self.resumed = False

    def resume_to_backup(self):
        self.x , self.y = self.backup_x , self.backup_y
        self.rect.x , self.rect.y = int(self.x) , int(self.y)
        self.angle_degree = self.backup_angle_degree
        self.image = self.backup_image
        self.resumed = True



    def get_pos(self,backup=False):
        return (int(self.backup_x),int(self.backup_y)) if backup else (int(self.x),int(self.y))

    def position_changed(self): return (self.backup_x,self.backup_y) != (self.x,self.y)

    def rotate_image(self,a):
        """ this function computes new image based on angle a in degree
            because images are stored in imagelist, it simply selects the appropriate one
        """
        l = len(self.imagelist)
        i = int(floor( a*l/360 + 0.5 )) % l
        self.image = self.imagelist[ i ]
        self.mask =  self.masklist [ i ]

    def translate_sprite(self,x,y,a,relative=True):
        # Attention, backup() est indispensable,
        # car la gestion des collision doit pouvoir revenir en arriere
        try:
            self.compteur +=1
        except:
            self.compteur = 0

        self.backup()
        if relative:
            self.x += x
            self.y += y
            self.angle_degree = (self.angle_degree + 720 + a) % 360
        else:
            self.x , self.y , self.angle_degree = x , y , a

        self.rotate_image(self.angle_degree)
        self.rect.x , self.rect.y = int(self.x) , int(self.y)


    def set_centroid(self,x,y):
        self.translate_sprite(x-self.rect.w//2,y-self.rect.h//2,self.angle_degree,relative=False)

    def get_centroid(self):
        #print "x=",self.x," , w=",self.rect.w
        return self.x+self.rect.w//2,self.y+self.rect.h//2

    def rotate(self,deg):
        self.translate_sprite(0,0, deg ,relative=True)

    def forward(self,t):
        dx,dy = cos(self.angle_degree * pi/180), sin(self.angle_degree * pi/180)
        if self.angle_degree % 90 == 0:
            dx,dy = round(dx),round(dy)
        self.translate_sprite(t*dx,t*dy,0)

    def get_rowcol(self):
        assert int(self.x) % self.rect.w == 0 and int(self.y) % self.rect.h == 0, "sprite must not be accross tiles for this function"
        return int(self.y) // self.rect.h , int(self.x) // self.rect.w

    def set_rowcol(self,row,col):
        self.translate_sprite(col*self.rect.w,row*self.rect.h,self.angle_degree,relative=False)
