import math
import time as ti
import pygame as py
import random as ra
from pygame.locals import *

nRES = (1184, 576)
ok = True
limitX = 37
limitY = 13 
celda = 32

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
    imagenes.append(Load_Image('pasto.png', False))
    imagenes.append(Load_Image('tierra.png', False))
    imagenes.append(Load_Image('agua.png', False))
    imagenes.append(Load_Image('agua.png', False))
    imagenes.append(Load_Image('leon.png', True))
    imagenes.append(Load_Image('leona.png', True))
    imagenes.append(Load_Image('cebra.png', True))
    imagenes.append(Load_Image('planta1.png', True))
    return imagenes

class Organismo:
    def __init__(self, x, y, vida, energia, velocidad, especie):
        self.x = x
        self.y = y
        self.vida = vida
        self.energia = energia
        self.velocidad = velocidad
        self.especie = especie

class Animal(Organismo):
    def __init__(self, x, y, vida, energia, velocidad, especie, genero, dieta):
        super().__init__(x, y, vida, energia, velocidad, especie)
        self.genero = genero
        self.dieta = dieta

    def moverse(self):
        self.x += ra.choice([-32, 0, 32]) * self.velocidad
        self.y += ra.choice([-32, 0, 32]) * self.velocidad

    def cazar(self):
        self.energia += 30
        self.vida += 20
        print("cazadooooooo")

    def reproducirse(self):
        cria = Animal(self.x + 32, self.y + 32, 100, 100, self.velocidad, self.especie, ra.choice(["Macho", "Hembra"]), self.dieta)
        Programa.agregar_organismo(cria)

class Planta(Organismo):
    def __init__(self, x, y, vida, energia, velocidad, especie, realiza_fotosintesis, se_reproduce):
        super().__init__(x, y, vida, energia, velocidad, especie)
        self.realiza_fotosintesis = realiza_fotosintesis
        self.se_reproduce = se_reproduce

    def reproducirse(self):

        pass

class Ambiente:
    def __init__(self, temperatura, humedad, eventos_climaticos):
        self.temperatura = temperatura
        self.humedad = humedad
        self.eventos_climaticos = eventos_climaticos

    def afectar_ecosistema(self):
        pass

class Ecosistema():
    def __init__(self):
        self.organismos = []

    def agregar_organismo(self, organismo):
        self.organismos.append(organismo)

    def gestionar_ciclo_de_vida(self):
        for i in self.organismos.copy():
            if i.vida <= 0:
                self.organismos.remove(i)
            else:
                i.energia -= 1
                if i.energia <= 0:
                    i.vida -= 2

    def gestionar_interacciones(self):
        for i in range(len(self.organismos)):
            for j in range(i + 1, len(self.organismos)):
                organismo1 = self.organismos[i]
                organismo2 = self.organismos[j]
                distancia = math.sqrt((organismo1.x - organismo2.x)**2 + (organismo1.y - organismo2.y)**2)
                if distancia < 32:
                    self.Cazadores_y_Presas(organismo1, organismo2)
                if distancia < 12:
                    self.Reproducción(organismo1, organismo2)

    def Cazadores_y_Presas(self, organismo1, organismo2):
        if isinstance(organismo1, Animal) and isinstance(organismo2, Animal):
            if organismo1.dieta == "Carnivoro" and organismo2.dieta == "Hervívoro":
                organismo1.cazar()
                organismo2.vida -= 40
            elif organismo2.dieta == "Carnivoro" and organismo1.dieta == "Hervívoro":
                organismo2.cazar()
                organismo1.vida -40

    def Reproducción(self, organismo1, organismo2):
        if isinstance(organismo1, Animal) and isinstance(organismo2, Animal):
            if organismo1.especie == organismo2.especie and organismo1.genero != organismo2.genero:
                organismo1.reproducirse()


    def mantener_equilibrio_ecologico(self):
        pass

    def Pinta_Mapa(self, sWin, aFig):
        for nF in range(0, nRES[1]//celda):
            for nC in range(0, nRES[0]//celda):
                if nF <= 448//celda and nC < 896//celda: 
                    sWin.blit(aFig[0], (nC*celda , nF*celda))  
                elif nF > 448//celda and nC < 896//celda:
                    sWin.blit(aFig[2], (nC*celda , nF*celda))
                else:
                    sWin.blit(aFig[1], (nC*celda , nF*celda))
        
    
    def Pinta_Organismos(self, sWin, aFig):
        for i in self.organismos:
            if i.especie == "León" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[4], (i.x, i.y))
            
            if i.especie == "León" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[5], (i.x, i.y))

            if i.especie == "Cebra" and i.vida > 0:
                sWin.blit(aFig[6], (i.x , i.y))

            if i.especie == "Planta" and i.vida > 0:
                sWin.blit(aFig[7], (i.x , i.y))
            
            if isinstance(i, Animal):
                i.moverse()

            if i.x < 0 : i.x += 32 * i.velocidad
            if i.y < 0 : i.y += 32 * i.velocidad 
            if i.x > 1152: i.x += -32 * i.velocidad 
            if i.x > 886 and i.y > 544: i.y += -32 * i.velocidad 
            if i.x < 886 and i.y > 448: i.y += -32 * i.velocidad
            if i.x < 886 and i.y > 448: i.x +=  32 * i.velocidad
            


Leona = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 1, "León", "Hembra", "Carnivoro")
León = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 1, "León", "Macho", "Carnivoro")
Cebra = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 1, "Cebra", "Macho", "Hervívoro")
Planta1 = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 0, "Planta", "si", "si")
Programa = Ecosistema()
Programa.agregar_organismo(León)
Programa.agregar_organismo(Leona)
Programa.agregar_organismo(Cebra)
Programa.agregar_organismo(Planta1)
sWin = Init_PyGame()
aFig = Carga_Imagenes()
reloj = py.time.Clock()

while ok:
    for e in py.event.get():
        if e.type == QUIT:
            ok = False
    Programa.Pinta_Mapa(sWin, aFig)
    Programa.gestionar_ciclo_de_vida()
    Programa.gestionar_interacciones()
    Programa.Pinta_Organismos(sWin, aFig)
    py.display.flip()
    reloj.tick(1)
    

