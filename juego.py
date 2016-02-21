import random
import pygame as pyg
import pygame.locals as pygl
import sys
from common import *

from cartas import *


class Juego:
	def __init__(self):
		self._running = True
		self.screen = None
		self.size = self.width, self.height = WIDTH, HEIGHT
	#reparte las cartas en las 7 pilas
	def on_init(self):
		pyg.init()
		self.screen = pyg.display.set_mode(self.size)
		pyg.display.set_caption("Un solitario mas.")
		self.background = load_image('bg.png')
		self.pilas = []
		self.pilasareas = []
		self.subir = [[], [], [], []]
		self.maz = Mazo()
		self.deal()
	def on_execute(self):
		self.dragging = []
		self.clicked_sprites = []
		if self.on_init() == False:
			self._running = False
		while self._running:
			for event in pyg.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()
	def on_loop(self):
		if self.dragging:
			desp = 0
			for card in self.dragging:
				card.arrastrar(pyg.mouse.get_pos()[0], pyg.mouse.get_pos()[1]+desp)
				desp += 20
	def on_render(self):
		self.screen.blit(self.background, (0, 0))
		for x in self.pilasareas:
			self.screen.blit(x.image, x.rect)
		#dibujar pilas
		for p in self.pilas:
			for c in p:
				self.screen.blit(c.image, c.rect)
		pyg.display.flip()
	def on_cleanup(self):
		pyg.quit()

	def on_event(self, evento):
		if evento.type == QUIT:
			self._running = False
		elif evento.type == pyg.KEYDOWN:
		        if evento.key == pyg.K_ESCAPE:
		        	#TODO: resetear juego
		            print "TODO"
		elif evento.type == pyg.MOUSEBUTTONDOWN:
			pos = pyg.mouse.get_pos()
			#juntar todos los sprites y guardar los clickeados.
			for i in self.pilas:
				for x in i:
					if x.rect.collidepoint(pos):
						self.clicked_sprites.append(x)

			if self.clicked_sprites:
				clickeada = self.clicked_sprites[-1]
				if clickeada.estado == ARRIBA:
					clickea_index_pila = clickeada.pila.index(clickeada) #obtener el indice de la ultima carta clickeada
					for cartasacar in clickeada.pila[clickea_index_pila:]: #arrastrar desde la ultima hacia abajo
						self.dragging.append(cartasacar)
				else: #si esta hacia abajo y se clickea voltearla
					if clickeada == clickeada.pila[-1]:
						clickeada.mostrar()
		elif evento.type == pyg.MOUSEBUTTONUP:
			pos = pyg.mouse.get_pos()
			if self.dragging:
				piladrop_index = self.check_pila_area(pos[0], pos[1]) 
				piladrop = self.pilas[piladrop_index]
				if(piladrop):
					if(piladrop_index != -1 and self.matchable(self.dragging[0], piladrop[-1])):
						for card in self.dragging:
							card.pila.remove(card)
							card.settopleft(piladrop[-1].posx, piladrop[-1].posy+DISTY_PILAS)
							piladrop.append(card)
							card.pila = piladrop
					else:
						for card in self.dragging:
							card.settopleft(card.posfx, card.posfy)
				else: #Si esta vacia, revisar que sea K 
					if piladrop_index!=-1 and self.dragging[0].numero == 12:
						for card in self.dragging:
							card.pila.remove(card)
							if(card == self.dragging[0]):
								self.dragging[0].settopleft(PILAS_XINICIAL+(piladrop_index*DISTX_PILAS), PILAS_YINICIAL)
							else:
								card.settopleft(piladrop[-1].posx, piladrop[-1].posy+DISTY_PILAS)
							piladrop.append(card)
							card.pila = piladrop

					else:
						for card in self.dragging:
							card.settopleft(card.posfx, card.posfy)


			self.dragging = []
			self.clicked_sprites = []
			
# ----- FUNCIONES DEL JUEGO ----
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
	#Recibe 2 cartas y retorna si c2 se puede poner sobre c1
	def matchable(self, c1, c2):
		if(c1.color != c2.color and c1.numero+1 == c2.numero):
			return True
		else:
			return False

if __name__ == "__main__":
	juego = Juego()
	juego.on_execute()

