# -*- coding: utf-8 -*-
import socket

class Network:
	#Class client qui s'occupe d'envoyer et de recevoir les données du serveur
    position_joueur_2_x = 0
    position_joueur_2_y = 0
    orientation2 = 0   

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.1.90" #Adresse ipv4 de la machine qui lance le jeu
        self.port = 12800
        self.data = ""
        self.reponse = []           
      

    def connect(self):#Connection Client Serveur
        self.socket.connect((self.host,self.port))
        print("Le client est connectée")

    def send(self, data):#Envoie les donnée au serveur et verifie les données renvoier par le serveur
        self.socket.sendall(str.encode(data))
        self.data = self.socket.recv(2048).decode()
        self.reponse = self.data.split(":")
        if self.data[0]=="2":
            position_joueur_2_x = ((int(float(self.reponse[1]))))
            position_joueur_2_y = ((int(float(self.reponse[2]))))
            orientation2 = ((int(float(self.reponse[3]))))
            return(str(position_joueur_2_x)+":"+str(position_joueur_2_y)+":"+str(orientation2)) 
        if self.data=="Victoire Joueur2":
            return (str("Victoire Voiture Bleu"))

            
            

            


