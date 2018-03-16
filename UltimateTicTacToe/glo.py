"""
Globals (mainly constants)
"""

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

ALL_LAYERS = ["bg1", "bg2", "cache", "obstacle", "ramassable", "actionnable", "dessinable","eye_candy", "joueur", "personnage", "en_hauteur"]
assert all(s[-1]!='s' for s in ALL_LAYERS),"layername should not end with an s"

ALL_LAYERS_SET = set(ALL_LAYERS)

NON_BG_LAYERS = [l for l in ALL_LAYERS if l not in ["bg1", "bg2"]]
