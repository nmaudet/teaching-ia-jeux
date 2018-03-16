import pygame
from math import pi,cos,sin


#class Point(tuple):
#    def __init__(self,x,y):self = (x,y)
#    def __add__(self,p):   return Point(self.x+p.x,self.y+p.y)

def draw_arrow(surf,x,y,angle,r=20,tail_angle =  pi*0.4, clr=(255,0,0)):
    """ dessine une fleche pour indiquer la direction d'un sprite """

    def p(a,rayon=r):        return (int(x+rayon*cos(a)),int(y+rayon*sin(a)))

    pygame.draw.polygon(surf,clr,[  p(angle) ,\
                                    p(angle+pi-tail_angle/2) ,\
                                    p(angle+pi,rayon=r*0.4) ,\
                                    p(angle+pi+tail_angle/2) ])


def draw_transparent_arrow(surf,x,y,angle,alpha=150,r=20,tail_angle = pi*0.4,clr=(255,0,0)):
    """ dessine une fleche semi-transparente pour indiquer la direction d'un sprite """
    tmp = pygame.Surface((2*r,2*r))
    tmp.set_colorkey( (0,0,0) )
    tmp.set_alpha(alpha)

    draw_arrow(tmp,r,r,angle,r,tail_angle)
    surf.blit(tmp,(x-r,y-r))
    return tmp


def test_polygon():
    from gameclass import Game
    from spritebuilder import SpriteBuilder

    game = Game('Cartes/gardenofdelight.json',SpriteBuilder)
    game.draw()
    draw_transparent_arrow(game.screen , 400 , 100, 1+pi)
    draw_arrow(game.screen , 300 , 100, 1)
    pygame.display.flip()

    while True:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                pygame.quit()
                quit()

if __name__ == '__main__':
    test_polygon()
