# -*- coding: utf-8 -*-
import socket

import threading
from settings import *
#Variable correspondant à l'etat des voiture 1 et 2 
position_joueur_1_x = 0
position_joueur_1_y = 0
position_joueur_2_x = 0
position_joueur_2_y = 0
orientation = 0
orientation2 = 0

class ThreadedServer(object):
    def __init__(self, host, port, position_joueur_1_x, position_joueur_1_y,position_joueur_2_x,position_joueur_2_y,orientation,orientation2):
        self.position_joueur_1_x = position_joueur_1_x
        self.position_joueur_1_y = position_joueur_1_y
        self.position_joueur_2_x = position_joueur_2_x
        self.position_joueur_2_y = position_joueur_2_y
        self.orientation = orientation
        self.orientation2 = orientation2

        self.reponse = []
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        print("Le serveur écoute à présent sur le port 12800")

    def listen(self):#Verifie l'arrivée d'un nouveau client et lui attribue un Thread
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(5)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()
            print("Un client vient de se connecter")

    def listenToClient(self, client, address):# Envoie et recois les donnée,les réponse au client en la triant en fonction du joueur e
        taille = 2048
        while True:
        
            data = client.recv(taille)
            data = data.decode("utf8")
            self.reponse = data.split(":")
            if data:
                
                if data=="Victoire Joueur1":
                    client.sendall(str.encode(str("Victoire Joueur1")))
                    

                if data=="Victoire Joueur2":
                    client.sendall(str.encode(str("Victoire Joueur2")))
                    
                
                if data[0]=="1":
                    self.position_joueur_1_x = (int(float(self.reponse[1])))
                    self.position_joueur_1_y = (int(float(self.reponse[2])))
                    self.orientation = (int(float(self.reponse[3])))

                    print("Joueur 1 x",self.position_joueur_1_x)
                    print("Joueur 1 y",self.position_joueur_1_y)
                    self.reponse=[]
                    client.sendall(str.encode(str(2)+":"+str(self.position_joueur_2_x)+":"+str(self.position_joueur_2_y)+":"+str(self.orientation2)))
                    
                if data[0]=="2":
                    self.position_joueur_2_x=(int(float(self.reponse[1])))
                    self.position_joueur_2_y=(int(float(self.reponse[2])))
                    self.orientation2 = (int(float(self.reponse[3])))
                    print("Joueur 2 x",self.position_joueur_2_x)
                    print("Joueur 2 y",self.position_joueur_2_y)
                    self.reponse=[]
                    client.sendall(str.encode(str(1)+":"+str(self.position_joueur_1_x)+":"+str(self.position_joueur_1_y)+":"+str(self.orientation)))
            else:
                raise error('Client déconnectée')
            

ThreadedServer('',12800,position_joueur_1_x ,position_joueur_1_y ,position_joueur_2_x ,position_joueur_2_y,orientation,orientation2).listen()