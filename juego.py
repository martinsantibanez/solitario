import random
import pygame, sys
from pygame.locals import *
from common import *

from cartas import *


class Juego:
	def __init__(self):
		self.maz = Mazo()
		self.pilas = []


	#reparte las cartas en las 7 pilas
		
	def deal(self):
		xact = PILAS_XINICIAL
		for pilaact in range(7): 
			yact = PILAS_YINICIAL
			pila = []
			for numcarta in range(pilaact+1): 
				carta_ins = self.maz.cartas[0]
				carta_ins.settopleft(xact, yact)
				yact += DISTY_PILAS
				pila.append(carta_ins)
				self.maz.cartas.remove(carta_ins)
				if numcarta==pilaact: # Si es la ultima carta de la pila
					carta_ins.mostrar()
			xact += DISTX_PILAS


			self.pilas.append(pila)

	#Retorna en que pila esta la posicion pos
	def check_pila_area(self, posx, posy):
		for pilaact in range(7):
			carta = -1
			p_xi = PILAS_XINICIAL + (pilaact*DISTX_PILAS)
			p_xf = p_xi + TAMX_CARTA
			p_yi = PILAS_YINICIAL
			p_yf = p_yi + TAMY_CARTA + (DISTY_PILAS*pilaact)
			if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
				# print pilaact
				#revisar cartas pequenas
				for numcarta in range(pilaact):
					c_yi = p_yi+(DISTY_PILAS*numcarta)
					c_yf = c_yi+DISTY_PILAS
					if(posy > c_yi and posy < c_yf):
						carta = numcarta
				#revisar ultima carta
				c_yi = p_yi+DISTY_PILAS*pilaact
				c_yf = c_yi + TAMY_CARTA
				if(posy > c_yi and posy < c_yf):
					carta = pilaact
				if(carta != -1):
					return (pilaact, carta)
		return (-1, -1)

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
	dragging = None
	clicked_sprites = []
	while running:
		screen.blit(background, (0, 0)) # fondo
		#eventos
		keys = pygame.key.get_pressed()
		if dragging:
			print "xdxd"
			dragging.setcenter(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
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
						dragging = clickeada
					else:
						clickeada.mostrar()
			elif evento.type == pygame.MOUSEBUTTONUP:
				if dragging:
					dragging = None
				clicked_sprites = []


		pygame.display.flip()

if __name__ == "__main__":
	pygame.init()
	main()

