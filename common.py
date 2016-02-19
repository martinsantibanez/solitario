import random
import pygame, sys
from pygame.locals import *
from common import *

#pintas
TREBOL = "T"
PICA = "P"
CORAZON = "C"
DIAMANTE = "D"
PINTAS = [TREBOL, PICA, CORAZON, DIAMANTE]
#colores
NEGRO = 0
ROJO = 1

#estado
ABAJO = 0
ARRIBA = 1

#ventana
WIDTH = 400
HEIGHT = 300

#distancias entre las cartas
DISTX_PILAS = 50
DISTY_PILAS = 20
PILAS_XINICIAL = 10
PILAS_YINICIAL = 60

#tamano de las cartas
TAMX_CARTA = 39
TAMY_CARTA = 53

#pygame
LEFT = 1

def load_image(filename, transparent=False):
		try: image = pygame.image.load(filename)
		except pygame.error, message:
				raise SystemExit, message
		image = image.convert()
		if transparent:
				color = image.get_at((0,0))
				image.set_colorkey(color, RLEACCEL)
		return image