import pygame, sys, threading
from pygame.locals import *
from random import randint
from clases import Nave
from clases import Invasor as Enemigo

ancho  = 900
alto      = 480
listaEnemigo = []


class cargarEnemigos(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.stoprequest = threading.Event( )

	def run(self):
		posx = 100
		for x in range(1,5):
			enemigo = Enemigo(posx,100,40,'imagenes/MarcianoA.jpg','imagenes/MarcianoB.jpg')
			listaEnemigo.append(enemigo)
			posx = posx + 200

		posx = 100
		for x in range(1,5):
			enemigo = Enemigo(posx,0,40,'imagenes/Marciano2A.jpg','imagenes/Marciano2B.jpg')
			listaEnemigo.append(enemigo)
			posx = posx + 200

		posx = 100
		for x in range(1,5):
			enemigo = Enemigo(posx,-100,40,'imagenes/Marciano3A.jpg','imagenes/Marciano3B.jpg')
			listaEnemigo.append(enemigo)
			posx = posx + 200

def detenerTodo( ):
	for enemigo in listaEnemigo:
		for disparo in enemigo.listaDisparo:
			enemigo.listaDisparo.remove(disparo)
		enemigo.conquista = True

def SpaceInvader( ):
	pygame.init( )
	ventana = pygame.display.set_mode((ancho,alto))
	fondo=pygame.image.load('imagenes/Fondo.jpg')
	pygame.display.set_caption("Space Invader")


	pygame.mixer.music.load('Sonidos/intro.mp3')
	pygame.mixer.music.play(4)


	miFuenteSistema = pygame.font.SysFont("Arial",30)
	Texto = miFuenteSistema.render("Fin del Juego",0,(120,100,40))
	TextoGanador = miFuenteSistema.render("Ganaste  ",0,(200,0,200))
	TextoPausa = miFuenteSistema.render("Pausa ", 0,(200,0,200))

	jugador = Nave.naveEspacial(ancho, alto)
	c =cargarEnemigos( )
	c.start( )
	enJuego = True
	reloj = pygame.time.Clock( )

	while True:

		reloj.tick(60)
		tiempo = pygame.time.get_ticks()/1000
		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit( )
				sys.exit( )

			if enJuego == True:
				if evento.type == pygame.KEYDOWN:
					if evento.key == K_LEFT:
						jugador.movimientoIzquierda( )

					elif evento.key == K_RIGHT:
						jugador.movimientoDerecha( )

					elif evento.key == K_s:
						x,y = jugador.rect.center
						jugador.disparar(x,y)

					elif evento.key == K_p:
						ventana.blit(TextoPausa,(200,300))
						pygame.display.flip()
						while True:
							evento = pygame.event.wait()
							pygame.mixer.music.pause()
							if evento.type == KEYDOWN:
								if evento.key == K_p:
									pygame.mixer.music.unpause()
									break



		ventana.blit(fondo, (0,0))

		jugador.dibujar(ventana)

		if len(jugador.listaDisparo)>0:
			for x in jugador.listaDisparo:
				x.dibujar(ventana)
				x.trayectoria( )
				if x.rect.top < -10:
					jugador.listaDisparo.remove(x)
				else:
					for enemigo in listaEnemigo:
						if x.rect.colliderect(enemigo.rect):
							listaEnemigo.remove(enemigo)
							jugador.listaDisparo.remove(x)

		if len(listaEnemigo)>0:
			for enemigo in listaEnemigo:
				enemigo.comportamiento(tiempo)
				enemigo.dibujar(ventana)

				if enemigo.rect.colliderect(jugador.rect):
					jugador.destruccion( )
					enJuego = False
					detenerTodo( )

				if len(enemigo.listaDisparo)>0:
					for x in enemigo.listaDisparo:
						x.dibujar(ventana)
						x.trayectoria( )
						if x.rect.colliderect(jugador.rect):
							jugador.destruccion( )
							enJuego = False
							detenerTodo( )

						if x.rect.top > 900:
							enemigo.listaDisparo.remove(x)
						else:
							for disparo in jugador.listaDisparo:
								if x.rect.colliderect(disparo.rect):
									jugador.listaDisparo.remove(disparo)
									enemigo.listaDisparo.remove(x)
		else:
			ventana.blit(TextoGanador,(300,300))

		if enJuego == False:
			pygame.mixer.music.fadeout(3000)
			ventana.blit(Texto,(300,300))

		pygame.display.update( )

SpaceInvader( )
