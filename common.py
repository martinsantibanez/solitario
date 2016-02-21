import random
import pygame, sys
from pygame.locals import *
from common import *

#tipos de areas del tablero
PILA = 0
PILASUBIR = 1
MAZO = 2
MOSTRADAS = 3
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

#distancias entre las cartas
DISTX_PILAS = 50
DISTY_PILAS = 20
#posiciones iniciales pilas
PILAS_XINICIAL = 10
PILAS_YINICIAL = 80
#posicion inicial mazo
MAZO_XINICIAL = 10
MAZO_YINICIAL = 10
#posicion inicial pilas_subir
PILASUBIR_XINICIAL = MAZO_XINICIAL+DISTX_PILAS*3
PILASUBIR_YINICIAL = MAZO_YINICIAL
#posicion inicial cartas mostradas
MOSTRADA_POSX = MAZO_XINICIAL + DISTX_PILAS
MOSTRADA_POSY = MAZO_YINICIAL
#tamano de las cartas
TAMX_CARTA = 39
TAMY_CARTA = 53

#pygame
LEFT = 1
#ventana
WIDTH = PILAS_XINICIAL*2 + DISTX_PILAS*7
HEIGHT = 500

def load_image(filename, transparent=False):
		try: image = pygame.image.load(filename)
		except pygame.error, message:
				raise SystemExit, message
		image = image.convert()
		if transparent:
				color = image.get_at((0,0))
				image.set_colorkey(color, RLEACCEL)
		return image