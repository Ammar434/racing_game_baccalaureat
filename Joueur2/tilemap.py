# -*- coding: utf-8 -*-
import pygame as pg
from settings import *
import pytmx


class TiledMap:#Charge le fichier correspondant à la map et permet la creation d'une map à tuile
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Camera:#Mis en place d'un second réctangle permettant d'afficher une certaine partie de la Tiledmap précedente
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):#deplacement de la camera une fois avoir atteint la moitie de la fenetre
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limite pour le mouvement de la camera
        x = min(0, x)  # limite a gauche
        y = min(0, y)  # limite en haut
        x = max(-(self.width - WIDTH), x)  # limite a droite
        y = max(-(self.height - HEIGHT), y)  # limite en bas
        self.camera = pg.Rect(x, y, self.width, self.height)
        #print(x)
        #print(y)