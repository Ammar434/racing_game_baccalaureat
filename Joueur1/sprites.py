# -*- coding: utf-8 -*-
import pygame as pg
from settings import *
from os import path
from client import *
from tilemap import*
from PIL import Image


class Player1(pg.sprite.Sprite):#On definit une class player1
	  
	def __init__(self, game, x, y,screen,map):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.network = Network()
		self.network.connect()
		self.game_folder = path.dirname(__file__)#Récupere le nom dossier dans lequel s'execute le prgm
		self.img_folder = path.join(self.game_folder, 'img')#chargement des dossiers contenant les images
		self.song_folder = path.join(self.game_folder, 'music')#chargement des dossiers contenant les fichiers audio
		self.z = ['voiture (droite).png','voiture (gauche).png','voiture (vers la droite).png','voiture (vers le bas).png','voiture (haut droite).png','voiture (haut gauche).png','voiture (bas gauche).png','voiture (bas droite).png']
		#liste qui va contenir les differentes images suivant les differentes positions de la voiture
		self.orientation=0 #variable pour definir l orientation de la voiture
		self.orientation2 = 0
		self.test=""

		
		self.screen= screen
		self.map = map
		self.vx =0 #vitesse deplacement en x
		self.vy = 0#vitesse deplacement en y
		self.x = x #position de la voiture en x sur la map
		self.y = y #position de la voiture en y sur la map
		self.x2 = 100 
		self.y2 = 100

		self.perso()
#_________________________________________________________________________________________________________
		self.vitesse_joueur=170#vitesse initial 170
		self.speed=[170,80,40] #liste pour les vitesses normal, eau, herbe
		self.v=0
		self.accelerate=1.5#coefficient acceleration
		self.max_speed=300#vitesse max
		self.r=0
		self.v = 0
		self.b = 0
		#3 variables r,v,b pour les couleurs de chaque cannaux
		self.son = pg.mixer.Sound((path.join(self.song_folder,"impact.wav")))#bruitages lors de collision
		pg.mixer.music.load((path.join(self.song_folder,"arcade.mp3")))#fond sonore de jeu
		pg.mixer.music.play()



	def perso(self):

		self.image = pg.image.load(path.join(self.img_folder,self.z[self.orientation2]))#chargement de l image souhaitee
		self.rect = self.image.get_rect()#recuperation de l image en rectangle
		self.player2 = Player2(self.game,self.x2,self.y2,self.screen)

	def get_keys(self):
		self.get_color(self.x+5, self.y-5)#recupere la couleur du pixel a la position de la voiture avec un decalage pour la consideration du rectangle
		self.def_speed()#definition de la vitesse en fonction de la couleur du pixel recuperee auparavant
		self.image = pg.image.load(path.join(self.img_folder,self.z[self.orientation]))#chargement de l image
		self.vx, self.vy = 0, 0
		keys = pg.key.get_pressed()#verification des boutons appuyes

		#self.track() #Essai fonction des traces de pneus
		if keys[pg.K_LEFT]:#bouton gauche, voiture va a gauche
			self.orientation=1#changement de l image utilisee avec l image allant vers la gauche
			self.vx = -self.vitesse_joueur

		if keys[pg.K_RIGHT]:#bouton droit, voiture va a droite
			self.orientation=2#changement de l image utilisee avec l image allant vers la droite
			self.vx = self.vitesse_joueur

		if keys[pg.K_UP]:#bouton fleche haute, voiture va en haut
			self.orientation=0#changement de l image utilisee avec l image allant vers le haut
			self.vy = -self.vitesse_joueur

		if keys[pg.K_DOWN]:#bouton fleche bas, voiture va en bas
			self.orientation=3#changement de l image utilisee avec l image allant vers le bas
			self.vy = self.vitesse_joueur

		if keys[pg.K_UP] and keys[pg.K_LEFT]:
			self.orientation=5#changement de l image utilisee avec l image allant vers le haut a gauche

		if keys[pg.K_UP] and keys[pg.K_RIGHT]:
			self.orientation=4#changement de l image utilisee avec l image allant vers le haut a droite

		if keys[pg.K_DOWN] and keys[pg.K_LEFT]:
			self.orientation = 6#changement de l image utilisee avec l image allant vers le bas a gauche

		if keys[pg.K_DOWN] and keys[pg.K_RIGHT]:
			self.orientation=7#changement de l image utilisee avec l image allant vers le bas a droite

		if keys[pg.K_SPACE] and self.vx < self.max_speed and self.vy < self.max_speed:#acceleration si la vitesse n excede pas la vitesse max
			self.vx = self.vx * self.accelerate
			self.vy = self.vy * self.accelerate
		
	
	def collide_with_walls(self,direction):#Detection de colision avec les objets du groupe game.walls
		if direction == 'x': 
			hits = pg.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				self.son.play()
				if self.vx > 0:
					self.x = hits[0].rect.left - self.rect.width
					self.vx = 0
					self.rect.x = self.x
				if self.vx < 0:
				    self.x = hits[0].rect.right
				    self.vx = 0
				    self.rect.x = self.x
		if direction == 'y':
			hits = pg.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				self.son.play()
				if self.vy > 0:
					self.y = hits[0].rect.top - self.rect.height
					self.vy = 0
					self.rect.y = self.y
	
				if self.vy < 0:
				    self.y = hits[0].rect.bottom
				    self.vy = 0
				    self.rect.y = self.y

	def get_color(self,x,y):#recuperation de la couleur du pixel a la position de la voiture sur une image
		img ='562.png'
		im1 = Image.open(path.join(self.img_folder,img))
		self.r, self.v, self.b = im1.getpixel((x, y))

	def def_speed(self):#definition de la vitesse en fonction de la couleur du pixel
		print("rouge", self.r, "vert", self.v, "bleu", self.b)
		if 0<self.r<(95) and 150<self.v<200 and 0<self.b<70:#Couleur verte herbe
			self.vitesse_joueur=self.speed[1]
			print("on est dans l'herbe")
		elif 45<self.r < 153 and self.v > 228 and 200<self.b < 255:  # Couleur bleu eau
			self.vitesse_joueur=self.speed[2]
			print("on est dans eau")
		else:
			self.vitesse_joueur=self.speed[0]

	def col(self):# essai utilisation des thread pour executer le programme en parrallele
		img = '562.png'
		im1 = Image.open(path.join(self.img_folder,img))
		with self.verrou:
			self.r, self.v, self.b = im1.getpixel((0,0))
			attente = 0.001
			time.sleep(attente)

	def update(self):#Mise à jours des differente valeurs et envoie position au client
		self.get_keys()
		self.x += self.vx * self.game.dt
		self.y += self.vy * self.game.dt
		self.data = str(1) + ":" + str(self.x) + ":" + str(self.y)+ ":" + str(self.orientation)
		self.reponse = self.network.send(str(self.data))
		if self.reponse =="Victoire Voiture Bleu":
			self.draw_text("Victoire Voiture Bleu",self.END_font,105,RED,600,360,align="center")
			self.game.vict = True
			self.game.joueur = 2
		self.liste = self.reponse.split(":")
		self.position_joueur_2_x = ((int(float(self.liste[0]))))
		self.position_joueur_2_y = ((int(float(self.liste[1]))))
		self.orientation2 = ((int(float(self.liste[2]))))
		self.x2 = self.position_joueur_2_x
		self.y2 = self.position_joueur_2_y
		self.player2.x = self.x2
		self.player2.y = self.y2
		self.player2.get_keys(self.orientation2)
		print(self.orientation2)
		self.rect.x = self.x
		self.collide_with_walls('x')
		self.collision_arrivee("x")
		self.rect.y = self.y
		self.collide_with_walls('y')

        
	def collision_arrivee(self,direction):#Verifie si la ligne d'arrivée est atteinte  
		if direction == 'x': 
			hits = pg.sprite.spritecollide(self, self.game.victoire, False)
			if hits:
				self.data_fin = "Victoire Joueur1"
				self.reponse = self.network.send(str(self.data_fin))
				print(self.reponse)
				self.game.vict = True
				self.game.joueur = 1
				
		
		


	


class Player2(pg.sprite.Sprite):#Creation du second joueur dont la position dépendra de celle renvoyé par le serveur
    def __init__(self, game, x, y,screen):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game 
        self.game_folder = path.dirname(__file__)#Récupere le nom dossier dans lequel s'execute le prgm
        self.img_folder = path.join(self.game_folder, 'img')
        self.song_folder = path.join(self.game_folder, 'music')
        self.z = ['voit (droite).png','voit (vers la gauche).png','voit (vers la droite).png','voit (vers le bas).png','voit (haut gauche).png','voit (haut droite).png','voit (bas droite).png','voit (bas gauche).png']
        
        self.orientation= 0
       	self.perso2()
        
        self.screen= screen
        self.vx =0 
        self.vy = 0
        self.x = x
        self.y = y
        
    def perso2(self):
    	self.image = pg.image.load(path.join(self.img_folder,self.z[self.orientation]))
    	self.rect = self.image.get_rect()

    def get_keys(self,orientation):
    	self.orientation=orientation
    	
    	self.image = pg.image.load(path.join(self.img_folder,self.z[orientation]))


	    




    def update(self):
        self.get_keys(self.orientation)
        print(self.x)
        print(self.y)
        self.rect.x = self.x
        self.rect.y = self.y

        



#--------------------------------------------------------------------------------------------------
class Obstacle(pg.sprite.Sprite):#Permet de crée un rectangle invisible et de rajouter un obstacle sur la map au groupe game.walss
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Victoire(pg.sprite.Sprite):#Permet de crée un rectangle invisible et de rajouter la ligne victoire sur la map au groupe game.victoire
	def __init__(self,game,x,y,w,h):
		self.groups = game.victoire
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.rect = pg.Rect(x, y, w, h)
		self.hit_rect = self.rect
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y
		
