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
		# self.screen = pyg.display.set_mode(self.size, FULLSCREEN)
		# pygame.display.toggle_fullscreen()
		pyg.display.set_caption("Un solitario mas.")
		self.background = load_image('bg.png')
		self.pilas = []
		self.pilasareas = []
		self.pilas_subir = []
		self.mostradas = []
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
		#dibujar mazo
		self.screen.blit(self.maz.image, self.maz.rect)
		#dibujar subidas
		for pinta in self.pilas_subir:
			self.screen.blit(pinta.image, pinta.rect)
			for carta_p in pinta.cartas:
				self.screen.blit(carta_p.image, pinta.rect)
		for area in self.pilasareas:
			self.screen.blit(area.image, area.rect)
		#dibujar pilas
		for pila in self.pilas:
			for card in pila:
				if not card in self.dragging:
					self.screen.blit(card.image, card.rect)
		#dibujar mostradas
		for card in self.mostradas:
			if not card in self.dragging:
				self.screen.blit(card.image, card.rect)
		#dibujar arrastrando, al final para que no se tapen
		for card in self.dragging:
			self.screen.blit(card.image, card.rect)
		pyg.display.flip()
	def on_cleanup(self):
		pyg.quit()

	def on_event(self, evento):
		if evento.type == QUIT:
			self._running = False
		elif evento.type == pyg.KEYDOWN:
			if evento.key == pyg.K_ESCAPE:
				self.on_init()
		elif evento.type == pyg.MOUSEBUTTONDOWN:
			pos = pyg.mouse.get_pos()
			#juntar todos los sprites y guardar los clickeados.
			tipo = None
			for i in self.pilas:
				for x in i:
					if x.rect.collidepoint(pos):
						tipo = PILA
						self.clicked_sprites.append(x)

			for i in self.mostradas:
				if i.rect.collidepoint(pos):
					tipo = MOSTRADAS
					self.clicked_sprites.append(i)

			if self.clicked_sprites:
				clickeada = self.clicked_sprites[-1]
				if tipo == MOSTRADAS:
					self.dragging.append(clickeada)
				elif tipo == PILA:
					if clickeada.estado == ARRIBA:
						clickea_index_pila = clickeada.pila.index(clickeada) #obtener el indice de la ultima carta clickeada
						for cartasacar in clickeada.pila[clickea_index_pila:]: #arrastrar desde la ultima hacia abajo
							self.dragging.append(cartasacar)
					else: #si esta hacia abajo y se clickea voltearla
						if clickeada == clickeada.pila[-1]:
							clickeada.mostrar()
		elif evento.type == pyg.MOUSEBUTTONUP:
			pos = pyg.mouse.get_pos()
			tipo_drop, piladrop_index = self.check_pila_area(pos[0], pos[1])
			if(tipo_drop == PILA):
				if self.dragging:
					piladrop = self.pilas[piladrop_index]
					if(piladrop):
						if(piladrop_index != -1 and self.matchable(self.dragging[0], piladrop[-1])):
							for card in self.dragging:
								if card.pila:
									card.pila.remove(card)
								else:
									self.mostradas.remove(card)
								card.settopleft(piladrop[-1].posx, piladrop[-1].posy+DISTY_PILAS)
								piladrop.append(card)
								card.pila = piladrop
					else: #Si esta vacia, revisar que sea K 
						if piladrop_index!=-1 and self.dragging[0].numero == 12:
							for card in self.dragging:
								if card.pila:
									card.pila.remove(card)
								else:
									self.mostradas.remove(card)
								if(card == self.dragging[0]):
									self.dragging[0].settopleft(PILAS_XINICIAL+(piladrop_index*DISTX_PILAS), PILAS_YINICIAL)
								else:
									card.settopleft(piladrop[-1].posx, piladrop[-1].posy+DISTY_PILAS)
								piladrop.append(card)
								card.pila = piladrop


			elif(tipo_drop == PILASUBIR and len(self.dragging)==1):
				if self.dragging:
					card = self.dragging[0]
					if(card.pinta == piladrop_index.pinta):
						if card.numero == 0:
							self.subir(card, piladrop_index)
						if piladrop_index.cartas:
							if card.numero == piladrop_index.cartas[-1].numero+1:
								self.subir(card, piladrop_index)
			elif(tipo_drop == MAZO):
				if self.maz.cartas:
					card = self.maz.cartas[-1]
					self.maz.cartas.remove(card)
					card.settopleft(MOSTRADA_POSX, MOSTRADA_POSY)
					card.mostrar()
					self.mostradas.append(card)
				else:
					for card in self.mostradas:
						self.mostradas.remove(card)
						self.maz.cartas.append(card)
			#elif(tipo_drop == MOSTRADAS):


			for card in self.dragging:
				card.settopleft(card.posfx, card.posfy)
			self.dragging = []
			self.clicked_sprites = []

# ----- FUNCIONES DEL JUEGO ----
	def subir(self, card, piladrop_index):
		if card.pila:
			card.pila.remove(card)
		else:
			self.mostradas.remove(card)
		card.settopleft(piladrop_index.posx, piladrop_index.posy)
		piladrop_index.cartas.append(card)
		card.pila = piladrop_index

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

		#Crear pilas donde se suben las cartas
		deltax = 0
		for pinta in PINTAS:
			p = PilaSubir(pinta)
			p.settopleft(PILASUBIR_XINICIAL+deltax, PILASUBIR_YINICIAL)
			self.pilas_subir.append(p)
			deltax+= DISTX_PILAS


	#Retorna en que pila esta la posicion pos
	def check_pila_area(self, posx, posy):
		#revisar si el click es en el mazo
		p_xi = self.maz.posx
		p_xf = p_xi + TAMX_CARTA
		p_yi = self.maz.posy
		p_yf = p_yi + TAMY_CARTA
		if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
			return MAZO, self.maz
		#revisar si el click es en las cartas mostradas
		p_xi = MOSTRADA_POSX
		p_xf = p_xi + TAMX_CARTA
		p_yi = MOSTRADA_POSY
		p_yf = p_yi + TAMY_CARTA
		if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
			return MOSTRADAS, None

		for pilaact in range(7):
			carta = -1
			p_xi = PILAS_XINICIAL + (pilaact*DISTX_PILAS)
			p_xf = p_xi + TAMX_CARTA
			p_yi = PILAS_YINICIAL
			p_yf = p_yi + TAMY_CARTA + (DISTY_PILAS*pilaact)
			if(posx > p_xi and posx < p_xf and posy > p_yi):
				return PILA, pilaact
		for pila_subir in self.pilas_subir:
			p_xi = pila_subir.posx
			p_xf = p_xi + TAMX_CARTA
			p_yi = pila_subir.posy
			p_yf = p_yi + TAMY_CARTA
			if(posx > p_xi and posx < p_xf and posy > p_yi and posy < p_yf):
				return PILASUBIR, pila_subir
		return -1, -1
	#Recibe 2 cartas y retorna si c2 se puede poner sobre c1
	def matchable(self, c1, c2):
		if(c1.color != c2.color and c1.numero+1 == c2.numero):
			return True
		else:
			return False

if __name__ == "__main__":
	juego = Juego()
	juego.on_execute()

