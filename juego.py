import random
import pygame, sys
from pygame.locals import *

from const import *


#pinta TREBOL, PICA, CORAZON, DIAMANTE

class Carta(pygame.sprite.Sprite):
	def __init__(self, numero, pinta):
		self.pinta = pinta
		self.numero = numero
		self.estado = ABAJO

		self.image = load_image("cards\\back.png")
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.centery = HEIGHT / 2
	def mostrar(self):
		if(self.estado == ABAJO):
			self.estado = ARRIBA
			self.image = load_image("cards\\"+self.pinta+str(self.numero)+".png")
	def ocultar(self):
		if(self.estado == ARRIBA):
			self.estado = ABAJO
			self.image = load_image("cards\\back.png")

class Mazo:
	def __init__(self):
		self.cartas = []
		self.crearmazo()
		# self.revolver()

	def crearmazo(self):
		for pinta in PINTAS:
			for numero in range(13):
				new_carta = Carta(numero, pinta)
				self.cartas.append(new_carta)
	def revolver(self):
		random.shuffle(self.cartas)

	#dev only
	def debug(self):
		for c in self.cartas:
			print c.sprite



class Juego:
	def __init__(self):
		self.maz = Mazo()
		self.pilas = []

	#reparte las cartas en las 7 pilas
	def deal(self):
		for pilaact in range(1,8): 
			pila = []
			for numcarta in range(pilaact): 
				carta_ins = self.maz.cartas[0]
				pila.append(carta_ins)
				self.maz.cartas.remove(carta_ins)
				if numcarta==pilaact-1: # Si es la ultima carta de la pila
					carta_ins.estado = ARRIBA


			self.pilas.append(pila)


def load_image(filename, transparent=False):
		try: image = pygame.image.load(filename)
		except pygame.error, message:
				raise SystemExit, message
		image = image.convert()
		if transparent:
				color = image.get_at((0,0))
				image.set_colorkey(color, RLEACCEL)
		return image


def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Pruebas Pygame")
	background = load_image('bg.png')
	
	# juego
	j = Juego()
	j.deal()
	# --
	drawcarta = Carta(2, TREBOL)
	drawcarta.mostrar()

	while True:
		keys = pygame.key.get_pressed()
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)
		if keys[K_UP]:
			drawcarta.mostrar()
		if keys[K_DOWN]:
			drawcarta.ocultar()
		screen.blit(background, (0, 0))
		screen.blit(drawcarta.image, drawcarta.rect)
		pygame.display.flip()

if __name__ == "__main__":
	pygame.init()
	main()

