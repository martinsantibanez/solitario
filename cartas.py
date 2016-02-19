import random
import pygame, sys
from pygame.locals import *
from common import *

#pinta TREBOL, PICA, CORAZON, DIAMANTE
class Carta(pygame.sprite.Sprite):
	def __init__(self, numero, pinta, posx=-1, posy=-1):
		self.clicked = False
		self.pinta = pinta
		self.numero = numero
		self.estado = ABAJO
		# pygame
		self.image = load_image("cards\\back.png")
		self.settopleft(posx, posy)
	def settopleft(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x
		self.posy = y
		self.rect.topleft = (self.posx, self.posy)
	def setcenter(self, x, y):
		self.rect = self.image.get_rect()
		self.posx = x-TAMX_CARTA/2
		self.posy = y-TAMY_CARTA/2
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

class Mazo:
	def __init__(self):
		self.cartas = []
		self.crearmazo()
		self.revolver()

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

