import random
import pygame, sys
from pygame.locals import *
from common import *

from cartas import *


class Juego:
	def __init__(self):
		self.maz = Mazo()
		self.pilas = []
		self.pilasareas = []
	#reparte las cartas en las 7 pilas
		
	def deal(self):
		xact = PILAS_XINICIAL
		for pilaact in range(7): 
			yact = PILAS_YINICIAL
			pila = []
			for numcarta in range(pilaact+1): 
				carta_ins = self.maz.cartas[0]
				carta_ins.settopleft(xact, yact)
				carta_ins.pila = pila
				pila.append(carta_ins)
				self.maz.cartas.remove(carta_ins)
				if numcarta==pilaact: # Si es la ultima carta de la pila
					carta_ins.mostrar()
				yact += DISTY_PILAS
			pilaarea = Area(xact, PILAS_YINICIAL)
			self.pilasareas.append(pilaarea)
			self.pilas.append(pila)
			xact += DISTX_PILAS

	#Retorna en que pila esta la posicion pos
	def check_pila_area(self, posx, posy):
		for pilaact in range(7):
			carta = -1
			p_xi = PILAS_XINICIAL + (pilaact*DISTX_PILAS)
			p_xf = p_xi + TAMX_CARTA
			p_yi = PILAS_YINICIAL
			p_yf = p_yi + TAMY_CARTA + (DISTY_PILAS*pilaact)
			if(posx > p_xi and posx < p_xf and posy > p_yi):
				return pilaact
		return -1

def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Pruebas Pygame")
	background = load_image('bg.png')
	
	# juego
	j = Juego()
	j.deal()
	# --

	numpila = 1
	running = 1
	pressed = 0
	dragging = []
	clicked_sprites = []
	while running:
		screen.blit(background, (0, 0)) # fondo
		#eventos
		keys = pygame.key.get_pressed()
		if dragging:
			desp = 0
			for card in dragging:
				card.arrastrar(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+desp)
				desp += 20

		for x in j.pilasareas:
			screen.blit(x.image, x.rect)
		#dibujar pilas
		for p in j.pilas:
			for c in p:
				screen.blit(c.image, c.rect)

		for evento in pygame.event.get():
			if evento.type == QUIT:
				sys.exit(0)
			elif evento.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				#juntar todos los sprites y juntar los clickeados.
				for i in j.pilas:
					for x in i:
						if x.rect.collidepoint(pos):
							clicked_sprites.append(x)

				if clicked_sprites:
					clickeada = clicked_sprites[-1]
					if clickeada.estado == ARRIBA:
						clickea_index_pila = clickeada.pila.index(clickeada)
						for cartasacar in clickeada.pila[clickea_index_pila:]:
							#clickeada.pila.remove(cartasacar)
							dragging.append(cartasacar)
					else:
						if clickeada == clickeada.pila[-1]:
							clickeada.mostrar()
			elif evento.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				if dragging:
					piladrop_index = j.check_pila_area(pos[0], pos[1])
					# print piladrop_index
					piladrop = j.pilas[piladrop_index]
					if(piladrop_index != -1):
						for card in dragging:
							card.pila.remove(card)
							if(piladrop):
								card.settopleft(piladrop[-1].posx, piladrop[-1].posy+DISTY_PILAS)
							else:
								card.settopleft(PILAS_XINICIAL+(piladrop_index*DISTX_PILAS), PILAS_YINICIAL)
							piladrop.append(card)
							card.pila = piladrop

					else:
						for card in dragging:
							card.settopleft(card.posfx, card.posfy)


				dragging = []
				clicked_sprites = []


		pygame.display.flip()

if __name__ == "__main__":
	pygame.init()
	main()

