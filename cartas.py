import random
import pygame, sys
from pygame.locals import *
from common import *

#pinta TREBOL, PICA, CORAZON, DIAMANTE
class Carta(pygame.sprite.Sprite):
	def __init__(self, numero, pinta, posx=-1, posy=-1):
		self.pila = None
		self.clicked = False
		self.pinta = pinta
		if pinta == TREBOL or pinta == PICA:
			self.color = NEGRO
		else:
			self.color = ROJO
		self.numero = numero
		self.estado = ABAJO
		# pygame
		self.image = load_image("cards\\back.png")
		self.settopleft(posx, posy)
	def settopleft(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.posfx = self.posx
		self.posfy = self.posy
		self.rect.topleft = (self.posx, self.posy)
	def arrastrar(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x-TAMX_CARTA/2
		self.posy = y-TAMY_CARTA/2
		self.rect.topleft = (self.posx, self.posy)
	def setcenter(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x-TAMX_CARTA/2
		self.posy = y-TAMY_CARTA/2
		self.posfx = self.posx
		self.posfy = self.posy
		self.rect.topleft = (self.posx, self.posy)

	def mostrar(self):
		if(self.estado == ABAJO):
			self.estado = ARRIBA
			self.image = load_image("cards\\"+self.pinta+str(self.numero+1)+".png")
			# print "cards\\"+self.pinta+str(self.numero)+".png"
	def ocultar(self):
		if(self.estado == ARRIBA):
			self.estado = ABAJO
			self.image = load_image("cards\\back.png")
	def switch(self):
		if(self.estado == ARRIBA):
			self.ocultar()
		else:
			self.mostrar()

class PilaSubir(pygame.sprite.Sprite):
	def __init__(self, pinta, posx=-1, posy=-1):
		self.pinta = pinta
		self.image = load_image("cards\\"+pinta+".png")
		self.settopleft(posx, posy)
		self.cartas = []
	def settopleft(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.rect.topleft = (self.posx, self.posy)

class Area(pygame.sprite.Sprite):
	def __init__(self, posx=-1, posy=-1):
		self.image = load_image("area.jpg")
		self.settopleft(posx, posy)
	def settopleft(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.rect.topleft = (self.posx, self.posy)

class Mazo(pygame.sprite.Sprite):
	def __init__(self):
		self.image = load_image("cards\\back.png")
		self.settopleft(MAZO_XINICIAL, MAZO_YINICIAL)
		self.cartas = []
		self.crearmazo()
		self.revolver()
	def settopleft(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.rect.topleft = (self.posx, self.posy)

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
