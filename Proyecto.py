import time as ti
import pygame as py
import random as ra
from pygame.locals import *

nRES = (1184, 576)
ok = True
nT_WX = nT_HY = 32
nMAXANIMALES = 5
nMx = nMy = 0

def Init_PyGame():
    py.init()
    py.mouse.set_visible(True)
    py.display.set_caption('')
    return py.display.set_mode(nRES)

def Load_Image(sFile, transp=False):
    try:
        image = py.image.load(sFile)
    except py.error:
        raise SystemExit
    image = image.convert()
    if transp:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def Carga_Imagenes():
    imagenes = []
    imagenes.append(Load_Image('T01.png', False))
    imagenes.append(Load_Image('T02.png', False))
    imagenes.append(Load_Image('T03.png', False))
    imagenes.append(Load_Image('T04.png', False))
    imagenes.append(Load_Image('leon.png', False))
    imagenes.append(Load_Image('cebra.png', False))
    return imagenes

class Organismo:
    def __init__(self, x, y, vida, energia, velocidad):
        self.x = x
        self.y = y
        self.vida = vida
        self.energia = energia
        self.velocidad = velocidad

class Animal(Organismo):
    def __init__(self, x, y, vida, energia, velocidad, especie, dieta):
        super().__init__(x, y, vida, energia, velocidad)
        self.especie = especie
        self.dieta = dieta

    def cazar(self):
        # Implementa la lógica de caza del animal
        pass

class Planta(Organismo):
    def __init__(self, x, y, vida, energia, velocidad, realiza_fotosintesis, se_reproduce):
        super().__init__(x, y, vida, energia, velocidad)
        self.realiza_fotosintesis = realiza_fotosintesis
        self.se_reproduce = se_reproduce

    def reproducirse(self):
        # Implementa la lógica de reproducción de la planta
        pass

class Ambiente:
    def __init__(self, temperatura, humedad, eventos_climaticos):
        self.temperatura = temperatura
        self.humedad = humedad
        self.eventos_climaticos = eventos_climaticos

    def afectar_ecosistema(self):
        # Implementa cómo el ambiente afecta al ecosistema
        pass

class Ecosistema:
    def __init__(self):
        self.organismos = []

    def agregar_organismo(self, organismo):
        self.organismos.append(organismo)

    def gestionar_ciclo_de_vida(self):
        for i in self.organismos.copy():
            if i.vida <= 0:
                self.organismos.remove(i)
                del self.organismos[self.organismos.index(i)]
            else:
                ti.sleep(3)
                i.energia -= 1
                if i.energia <= 0:
                    i.vida -= 2


    def gestionar_interacciones(self):
        # Implementa la lógica para gestionar las interacciones entre organismos en el ecosistema
        pass

    def mantener_equilibrio_ecologico(self):
        # Implementa la lógica para mantener el equilibrio ecológico del ecosistema
        pass

    def Pinta_Mapa(self, sWin, aFig):
        for nF in range(0, nRES[1]):
            for nC in range(0, nRES[0]):
                sWin.blit(aFig[0], (nC , nF))  
        return 
    
    def Pinta_Organismos(self, sWin, aFig):
        for i in self.organismos:
            if i.especie == "León" and i.vida > 0:
                sWin.blit(aFig[4], (i.x, i.y))
            if i.especie == "Cebra" and i.vida > 0:
                sWin.blit(aFig[5], (i.x , i.y))


León = Animal(ra.randint(0,1184), ra.randint(0,576), 2, 4, 1, "León", "Carnivoro")
Cebra = Animal(ra.randint(0,1184), ra.randint(0,576), 6, 3, 1, "Cebra", "Hervívoro")
Programa = Ecosistema()
Programa.agregar_organismo(León)
Programa.agregar_organismo(Cebra)
sWin = Init_PyGame()
aFig = Carga_Imagenes()


while ok:
    for e in py.event.get():
        if e.type == QUIT:
            ok = False
    Programa.Pinta_Mapa(sWin, aFig)
    Programa.gestionar_ciclo_de_vida()
    Programa.Pinta_Organismos(sWin, aFig)
    py.display.flip()

