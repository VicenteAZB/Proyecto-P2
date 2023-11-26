import math
import time as ti
import pygame as py
import random as ra
from pygame.locals import *

nRES = (1184, 576)
ok = True
limitX = 36
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
    imagenes.append(Load_Image('pasto.png', False))         #0
    imagenes.append(Load_Image('tierra.png', False))        #1  
    imagenes.append(Load_Image('agua.png', False))          #2
    imagenes.append(Load_Image('agua.png', False))          #3
    imagenes.append(Load_Image('leon.png', True))           #4
    imagenes.append(Load_Image('leona.png', True))          #5
    imagenes.append(Load_Image('cebra.png', True))          #6  
    imagenes.append(Load_Image('planta1.png', True))        #7
    imagenes.append(Load_Image('abeja.png', True))          #8
    imagenes.append(Load_Image('abeja2.png', True))         #9
    imagenes.append(Load_Image('cebra2.png', True))         #10
    imagenes.append(Load_Image('pastonieve.png', False))    #11
    imagenes.append(Load_Image('aguanieve.png', False))     #12
    imagenes.append(Load_Image('tierranieve.png', False))   #13
    imagenes.append(Load_Image('pastolluvia.png', False))   #14
    imagenes.append(Load_Image('agualluvia.png', False))    #15
    imagenes.append(Load_Image('tierralluvia.png', False))  #16
    imagenes.append(Load_Image('lluvia.png', False))  #17
    return imagenes

class Organismo:
    def __init__(self, x, y, vida, energia, agua, velocidad, especie):
        self.x = x
        self.y = y
        self.vida = vida
        self.energia = energia
        self.agua = agua 
        self.velocidad = velocidad
        self.especie = especie

class Animal(Organismo):
    def __init__(self, x, y, vida, energia, agua, velocidad, especie, genero, dieta):
        super().__init__(x, y, vida, energia, agua, velocidad, especie)
        self.genero = genero
        self.dieta = dieta

    def moverse(self):
        self.x += ra.choice([-32, 0, 32]) * self.velocidad
        self.y += ra.choice([-32, 0, 32]) * self.velocidad

    def cazar(self):
        self.energia += 30
        self.vida += 20

    def reproducirse(self):
        cria = Animal(self.x + 32, self.y + 32, 100, 100, self.velocidad, self.especie, ra.choice(["Macho", "Hembra"]), self.dieta)
        Programa.agregar_organismo(cria)

class Planta(Organismo):
    def __init__(self, x, y, vida, energia, agua, velocidad, especie, realiza_fotosintesis, se_reproduce):
        super().__init__(x, y, vida, energia, agua, velocidad, especie)
        self.realiza_fotosintesis = realiza_fotosintesis
        self.se_reproduce = se_reproduce

    def reproducirse(self):
        Planta(self, self.x + ra.choice([-32, 32]), self.x + ra.choice([-32, 32]), 100, 100, 0, self.especie, self.realiza_fotosintesis, self.se_reproduce)
        

class Ambiente:
    def __init__(self, temperatura, humedad, clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.clima = clima

class Ecosistema():
    def __init__(self):
        self.organismos = []
        self.ambientes = []
        self.tiempo = 0

    def agregar_organismo(self, organismo):
        self.organismos.append(organismo)

    def agregar_ambientes(self, ambiente):
        self.ambientes.append(ambiente)

    def gestionar_ciclo_de_vida(self):
        for i in self.organismos.copy():
            if i.vida <= 0:
                self.organismos.remove(i)
            else:
                if i.energia > 0:
                    i.energia -= 1
                else:
                    i.vida -= 2
                if i.agua > 0:
                    i.agua -= 1
                else:
                    i.vida -= 3


    def gestionar_interacciones(self):
        for i in range(len(self.organismos)):
            for j in range(i + 1, len(self.organismos)):
                organismo1 = self.organismos[i]
                organismo2 = self.organismos[j]
                distancia = math.sqrt((organismo1.x - organismo2.x)**2 + (organismo1.y - organismo2.y)**2)
                if distancia < 32:
                    self.Cazadores_y_Presas(organismo1, organismo2)
                if distancia < 32:
                    self.Reproducción(organismo1, organismo2)

    def Cazadores_y_Presas(self, organismo1, organismo2):
        if isinstance(organismo1, Animal) and isinstance(organismo2, Animal):
            if organismo1.dieta == "Carnivoro" and organismo2.dieta == "Hervívoro":
                organismo1.cazar()
                organismo2.vida -= 40

            elif organismo2.dieta == "Carnivoro" and organismo1.dieta == "Hervívoro":
                organismo2.cazar()
                organismo1.vida -40

        if isinstance(organismo1, Animal) and isinstance(organismo2, Planta):
            if organismo2.se_reproduce == "si" and organismo1.dieta == "Polen":
                organismo2.reproducirse()
                organismo1.vida += 20
            

    def Reproducción(self, organismo1, organismo2):
        if isinstance(organismo1, Animal) and isinstance(organismo2, Animal):
            if organismo1.especie == organismo2.especie and organismo1.genero != organismo2.genero:
                organismo1.reproducirse()


    def afectar_ecosistema(self, clima):
        for i in self.organismos:
            if isinstance(i, Animal):
                if clima.clima == "Nieve":
                    i.energia -= 7
                    i.agua += 1
                if clima.clima == "Lluvia":
                    i.energia -= 4
                    i.agua += 2
            if isinstance(i, Planta):
                if clima.clima == "Nieve":
                    i.energia -= 2

                if clima.clima == "Lluvia":
                    i.energia += 2
                    i.agua += 4
                    
            if i.energia > 100: i.energia = 100
            if i.agua > 100: i.agua = 100

    def cambiar_clima(self):
        climas = len(self.ambientes)-1
        print(climas)
        if climas == 0:
            clima = self.ambientes[0]
        else:
            clima = self.ambientes[ra.randint(0, climas)]
            self.tiempo += 10
        return clima

    def Pinta_Mapa(self, sWin, aFig, clima):
        for nF in range(0, nRES[1]//celda):
            for nC in range(0, nRES[0]//celda):
                if isinstance(clima, Ambiente):
                    if clima.clima == "Sol":
                        if nF <= 448//celda and nC < 896//celda: 
                            sWin.blit(aFig[0], (nC*celda , nF*celda))  
                        elif nF > 448//celda and nC < 896//celda:
                            sWin.blit(aFig[2], (nC*celda , nF*celda))
                        else:
                            sWin.blit(aFig[1], (nC*celda , nF*celda))

                    if clima.clima == "Lluvia":
                        if nF <= 448//celda and nC < 896//celda: 
                            sWin.blit(aFig[14], (nC*celda , nF*celda))  
                        elif nF > 448//celda and nC < 896//celda:
                            sWin.blit(aFig[15], (nC*celda , nF*celda))
                        else:
                            sWin.blit(aFig[16], (nC*celda , nF*celda))
                            for i in range(0, 1100):
                                sWin.blit(aFig[17], (ra.randint(0, nRES[0]),ra.randint(0, nRES[1]))) 
        
                    if clima.clima == "Nieve":
                        if nF <= 448//celda and nC < 896//celda: 
                            sWin.blit(aFig[11], (nC*celda , nF*celda))  
                        elif nF > 448//celda and nC < 896//celda:
                            sWin.blit(aFig[12], (nC*celda , nF*celda))
                        else:
                            sWin.blit(aFig[13], (nC*celda , nF*celda))

    def Pinta_Organismos(self, sWin, aFig):
        for i in self.organismos:
            if i.especie == "León" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[4], (i.x, i.y))
            
            if i.especie == "León" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[5], (i.x, i.y))

            if i.especie == "Cebra" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[6], (i.x , i.y))

            if i.especie == "Cebra" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[10], (i.x , i.y))

            if i.especie == "Tallo" and i.vida > 0:
                sWin.blit(aFig[7], (i.x , i.y))

            if i.especie == "Abeja" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[8], (i.x , i.y))

            if i.especie == "Abeja" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[9], (i.x , i.y))

            if isinstance(i, Animal):
                i.moverse()

            if i.x < 0 : i.x += 32 * i.velocidad
            if i.y < 0 : i.y += 32 * i.velocidad 
            if i.x > 1152: i.x += -32 * i.velocidad 
            if i.x > 886 and i.y > 544: i.y += -32 * i.velocidad 
            if i.x < 886 and i.y > 448: i.y += -32 * i.velocidad
            if i.x < 886 and i.y > 448: i.x +=  32 * i.velocidad
            


Leona = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "León", "Hembra", "Carnivoro")
León = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "León", "Macho", "Carnivoro")
Cebra = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Cebra", "Macho", "Hervívoro")
Cebra2 = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Cebra", "Hembra", "Hervívoro")
Tallo = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 0, "Tallo", "si", "si")
Abeja = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Abeja", "Macho", "Polen")
Abeja2 = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Abeja", "Hembra", "Polen")
Soleado = Ambiente(30, 25, "Sol")
Lluvia = Ambiente(15, 90, "Lluvia")
Nieve = Ambiente(-15, 100, "Nieve")
Programa = Ecosistema()
Programa.agregar_organismo(León)
Programa.agregar_organismo(Leona)
Programa.agregar_organismo(Cebra)
Programa.agregar_organismo(Cebra2)
Programa.agregar_organismo(Tallo)
Programa.agregar_organismo(Abeja)
Programa.agregar_organismo(Abeja2)
Programa.agregar_ambientes(Soleado)
Programa.agregar_ambientes(Lluvia)
Programa.agregar_ambientes(Nieve)
sWin = Init_PyGame()
aFig = Carga_Imagenes()
tiempo_inicio = ti.time()
reloj = py.time.Clock()

while ok:
    tiempo_final= ti.time()
    tiempo_transcurrido = tiempo_final - tiempo_inicio
    for e in py.event.get():
        if e.type == QUIT:
            ok = False
    if tiempo_transcurrido >= Programa.tiempo:
        clima = Programa.cambiar_clima()
    Programa.Pinta_Mapa(sWin, aFig, clima)
    Programa.gestionar_ciclo_de_vida()
    Programa.Pinta_Organismos(sWin, aFig)
    Programa.gestionar_interacciones()
    Programa.afectar_ecosistema(clima)

    for organismo in Programa.organismos:
        print(f"{organismo.especie} en la posición ({organismo.x}, {organismo.y}) - Vida: {organismo.vida}, Energía: {organismo.energia}, Reservas de agua: {organismo.agua}")

    py.display.flip()
    reloj.tick(1)
py.quit()
    

