# -*- coding: utf-8 -*-
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITRE)
        """
        pg.display.set_mode((pg.display.Info().current_w,
                                  pg.display.Info().current_h),
                                  pg.FULLSCREEN)
"""
        self.clock = pg.time.Clock()
        self.load_data()

       

    def load_data(self):#chargement de toutes les donnes utilisees ( musique, images, cartes...)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        song_folder = path.join(game_folder, 'music')
        self.map = TiledMap(path.join(map_folder,'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.END_font = path.join(img_folder, 'Victoire.TTF')

    def new(self):
        #initialise toute les variable et met tout en place pour un nouveau jeu
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.victoire = pg.sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player1':
                self.player = Player1(self, tile_object.x, tile_object.y,self.screen,self.map_img)       
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y,tile_object.width, tile_object.height)
            if tile_object.name == 'ligne_arrivee':
                Victoire(self, tile_object.x, tile_object.y,tile_object.width,tile_object.height)
       
        

    def run(self):
        #lance le jeu et vérifie si la ligne d'arrivée est atteinte
        self.playing = True
        self.vict = False
        self.joueur=0
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            if self.vict == False:
                self.update_main()

            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()	

    def update_main(self):	
        # met a jours une partie du de la boucle
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):#Permet d'afficher un texte à l'écran en fonction d'une position
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

        

    def draw(self):#Dessine ou affiche les differents objets sur la fenetre 
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.vict == True and self.joueur==1:
            self.draw_text("Victoire Voiture Rouge",self.END_font,105,RED,600,360,align="center")
        if self.vict == True and self.joueur==2:
            self.draw_text("Victoire Voiture Bleu",self.END_font,105,Blue,600,360,align="center")
        pg.display.flip()#Actualise uniquement que cette objet et non la fenetre entiere

    def events(self):
        # récupere tous les events ici
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

# L'objet jeu et boucle infinie
g = Game()


while True:
    g.new()
    g.run()


