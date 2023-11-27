import math
import time as ti
import pygame as py
import random as ra
from pygame.locals import *

nRES = (1920, 576)
ok = True
limitX = 36
limitY = 13 
celda = 32

def Init_PyGame():
    py.init()
    py.mouse.set_visible(True)
    py.display.set_caption('Ecosistema')
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
    imgs = [['pasto.png', False],         #0
            ['tierra.png', False],        #1  
            ['agua.png', False],          #2
            ['agua.png', False],          #3
            ['leon.png', True],           #4
            ['leona.png', True],          #5
            ['cebra.png', True],          #6  
            ['tallo.png', True],          #7
            ['abeja.png', True],          #8
            ['abeja2.png', True],         #9
            ['cebra2.png', True],         #10
            ['pastonieve.png', False],    #11
            ['aguanieve.png', False],     #12
            ['tierranieve.png', False],   #13
            ['pastolluvia.png', False],   #14
            ['agualluvia.png', False],    #15
            ['tierralluvia.png', False],  #16
            ['lluvia.png', False],        #17
            ['fondonegro.png', False],    #18
            ['trigo.png', True],          #19
            ['lavanda.png', True],        #20
            ['oregano.png', True],        #21
            ['girasol.png', True],        #22
            ['lobo.png', True],           #23
            ['lobo2.png', True],          #24
            ['conejo.png', True],         #25
            ['conejo2.png', True],        #26
            ['jirafa.png', True],         #27
            ['jirafa2.png', True],         #28
            ['meteorito.png', True]       #29
            ]
    
    for i in range(len(imgs)):
        imagenes.append(Load_Image(imgs[i][0],imgs[i][1]))

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
    
    def tomar_agua(self):
        self.agua += 40

    def reproducirse(self):
        cria = Animal(self.x + ra.choice([-64, 64]), self.y + ra.choice([-64, 64]), 100, 100, 100, self.velocidad, self.especie, ra.choice(["Macho", "Hembra"]), self.dieta)
        Programa.agregar_organismo(cria)

class Planta(Organismo):
    def __init__(self, x, y, vida, energia, agua, velocidad, especie, realiza_fotosintesis, se_reproduce):
        super().__init__(x, y, vida, energia, agua, velocidad, especie)
        self.realiza_fotosintesis = realiza_fotosintesis
        self.se_reproduce = se_reproduce
    def fotosintesis(self):
        if self.realiza_fotosintesis == "si":
            self.energia += 3
    def reproducirse(self):
        cria = Planta(self.x + ra.choice([-32, 32]), self.y + ra.choice([-32, 32]), 100, 100, 100, 0, self.especie, self.realiza_fotosintesis, self.se_reproduce)
        Programa.agregar_organismo(cria)
    def tomar_agua(self):
        self.agua += 10

class Ambiente:
    def __init__(self, temperatura, humedad, clima):
        self.temperatura = temperatura
        self.humedad = humedad
        self.clima = clima
        self.meteoritoX = ra.randint(0, 864)
        self.meteoritoY = ra.randint(0, 256)

    def meteorito(self, sWin):
        sWin.blit(aFig[29], (self.meteoritoX, self.meteoritoY))


class Ecosistema():
    def __init__(self):
        self.organismos = []
        self.ambientes = []
        self.tiempo = 0
        self.tM = ra.randint(11, 12)
        self.contador = 0

    def agregar_organismo(self, organismo):
        self.organismos.append(organismo)

    def agregar_ambientes(self, ambiente):
        self.ambientes.append(ambiente)

    def gestionar_ciclo_de_vida(self):
        for i in self.organismos.copy():
            if i.energia == 0 or i.agua == 0:
                i.vida -= 2
            if i.energia == 0 and i.agua == 0:
                i.vida -= 4
            if i.vida <= 0: self.organismos.remove(i)
            if i.vida > 100: i.vida = 100

            
    def gestionar_interacciones(self):
        for i in range(len(self.organismos)):
            for j in range(i + 1, len(self.organismos)):
                organismo1 = self.organismos[i]
                organismo2 = self.organismos[j]
                distancia = math.sqrt((organismo1.x - organismo2.x)**2 + (organismo1.y - organismo2.y)**2)
                if distancia < 32:
                    self.Cazadores_y_Presas(organismo1, organismo2)
                if distancia < 32:
                    if len(self.organismos) <= 30:
                        a = ra.randint(0,2)
                        if a == 1:
                            self.Reproducción(organismo1, organismo2)
        for i in self.organismos:
            if i.y == 416 and i.x <= 928:
                i.tomar_agua() 
            if i.y > 416 and i.x == 928:
                i.tomar_agua()


    def Cazadores_y_Presas(self, organismo1, organismo2):
        if isinstance(organismo1, Animal) and isinstance(organismo2, Animal):
            if organismo1.dieta == "Carnivoro" and organismo2.dieta == "Hervívoro":
                organismo1.cazar()
                organismo2.vida -= 40
    
            elif organismo2.dieta == "Carnivoro" and organismo1.dieta == "Hervívoro":
                organismo2.cazar()
                organismo1.vida -40

            if organismo1.dieta == "Carnivoro" and organismo2.dieta == "carnivoro":
                organismo1.vida -= 30
                organismo2.vida -= 30

        if isinstance(organismo1, Animal) and isinstance(organismo2, Planta):
            if organismo1.dieta == "Hervívoro" and organismo2.realiza_fotosintesis == "si":
                organismo1.cazar()
                organismo2.vida -= 5

        if isinstance(organismo1, Planta) and isinstance(organismo2, Animal):
            if organismo2.dieta == "Hervívoro" and organismo1.realiza_fotosintesis == "si":
                organismo2.cazar()
                organismo1.vida -= 5

            

    def Reproducción(self, organismo1, organismo2):
        if isinstance(organismo1, Animal) and isinstance(organismo2, Animal):
            if organismo1.especie == organismo2.especie and organismo1.genero != organismo2.genero:
                organismo1.reproducirse()

        if isinstance(organismo1, Animal) and isinstance(organismo2, Planta):
            if organismo2.se_reproduce == "si" and organismo1.dieta == "Polen":
                organismo2.reproducirse()
                organismo1.vida += 100

        if isinstance(organismo1, Planta) and isinstance(organismo2, Animal):
            if organismo1.se_reproduce == "si" and organismo2.dieta == "Polen":
                organismo1.reproducirse()
                organismo2.vida += 100

    def afectar_ecosistema(self, clima):
        for i in self.organismos:
            if isinstance(i, Animal):
                    
                if clima.clima == "Sol" and i.especie != "Abeja":
                    i.energia -= 1
                    i.agua -= 4
                if clima.clima == "Nieve" and i.especie != "Abeja":
                    i.energia -= 4
                    i.agua -= 2
                if clima.clima == "Lluvia" and i.especie != "Abeja":
                    i.energia -= 2
                    i.agua += 1
                if clima.clima == "Sol" and i.especie == "Abeja":
                    i.energia += 6 
                    i.agua -= 4
                if clima.clima == "Nieve" and i.especie == "Abeja":
                    i.energia -= 6 
                if clima.clima == "Lluvia" and i.especie == "Abeja":
                    i.energia -= 3
                    i.agua += 8
                i.moverse()

            if isinstance(i, Planta):

                if clima.clima == "Sol":
                    i.fotosintesis()
                    i.agua -= 2

                if clima.clima == "Nieve":
                    i.energia -= 2

                if clima.clima == "Lluvia":
                    i.energia -= 2
                    i.agua += 4

            if i.energia > 100: i.energia = 100
            if i.agua > 100: i.agua = 100
            if i.energia <= 0: i.energia = 0
            if i.agua <= 0: i.agua = 0


    def cambiar_clima(self):
        climas = len(self.ambientes)-1
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
                        elif nC < 1184//celda:
                            sWin.blit(aFig[1], (nC*celda , nF*celda))

                    if clima.clima == "Lluvia":
                        if nF <= 448//celda and nC < 896//celda: 
                            sWin.blit(aFig[14], (nC*celda , nF*celda))  
                        elif nF > 448//celda and nC < 896//celda:
                            sWin.blit(aFig[15], (nC*celda , nF*celda))
                        elif nC < 1184//celda:
                            sWin.blit(aFig[16], (nC*celda , nF*celda))
                            for i in range(0, 1100):
                                sWin.blit(aFig[17], (ra.randint(0, 1184),ra.randint(0, nRES[1]))) 
        
                    if clima.clima == "Nieve":
                        if nF <= 448//celda and nC < 896//celda: 
                            sWin.blit(aFig[11], (nC*celda , nF*celda))  
                        elif nF > 448//celda and nC < 896//celda:
                            sWin.blit(aFig[12], (nC*celda , nF*celda))
                        elif nC < 1184//celda:
                            sWin.blit(aFig[13], (nC*celda , nF*celda))
                        
                    if nC >= 1184//celda:
                        sWin.blit(aFig[18], (nC*celda , nF*celda))

        if self.tiempo >= self.tM:
            if self.contador == 0:
                for organismo in self.organismos:
                    rango_impactoX = clima.meteoritoX + celda*10
                    rango_impactoY = clima.meteoritoY + celda*10

                    if clima.meteoritoX <= organismo.x <= rango_impactoX and clima.meteoritoY <= organismo.y <= rango_impactoY:
                        print(f"¡Meteorito impacta a {organismo.especie} en la posición ({organismo.x}, {organismo.y})!")
                        organismo.vida -= 100

            if self.contador <= 9:
                clima.meteorito(sWin)
                self.contador += 1
            else:
                self.contador = 0
                self.tM += ra.randint(100, 1000)                    
                       
    def Pinta_Organismos(self, sWin, aFig):
        for i in self.organismos:
            if i.x < 0 : i.x += 32 * i.velocidad
            if i.y < 0 : i.y += 32 * i.velocidad 
            if i.x > 1152: i.x += -32 * i.velocidad 
            if i.x > 896 and i.y > 544: i.y += -32 * i.velocidad 
            if i.x < 896 and i.y > 448: i.y += -32 * i.velocidad
            if i.x < 896 and i.y > 448: i.x +=  32 * i.velocidad

            if i.especie == "León" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[4], (i.x, i.y))
            
            if i.especie == "León" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[5], (i.x, i.y))

            if i.especie == "Lobo" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[23], (i.x, i.y))

            if i.especie == "Lobo" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[24], (i.x, i.y))

            if i.especie == "Conejo" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[25], (i.x, i.y))

            if i.especie == "Conejo" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[26], (i.x, i.y))

            if i.especie == "Jirafa" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[27], (i.x, i.y))

            if i.especie == "Jirafa" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[28], (i.x, i.y))
            
            if i.especie == "Cebra" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[6], (i.x , i.y))

            if i.especie == "Cebra" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[10], (i.x , i.y))

            if i.especie == "Abeja" and i.vida > 0 and i.genero == "Macho":
                sWin.blit(aFig[8], (i.x , i.y))

            if i.especie == "Abeja" and i.vida > 0 and i.genero == "Hembra":
                sWin.blit(aFig[9], (i.x , i.y))

            if i.especie == "Tallo" and i.vida > 0:
                sWin.blit(aFig[7], (i.x , i.y))

            if i.especie == "Orégano" and i.vida > 0:
                sWin.blit(aFig[21], (i.x , i.y))

            if i.especie == "Lavanda" and i.vida > 0:
                sWin.blit(aFig[20], (i.x , i.y))

            if i.especie == "Trigo" and i.vida > 0:
                sWin.blit(aFig[19], (i.x , i.y))

            if i.especie == "Girasol" and i.vida > 0:
                sWin.blit(aFig[22], (i.x , i.y))

    def mostrar_registros_pantalla(self, sWin):
        with open("registros.log", "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            fuente = py.font.Font(None, 22)
            for i, linea in enumerate(lineas):
                texto = fuente.render(linea.strip(), True, (255, 255, 255))
                sWin.blit(texto, (1224, 10 + i * 20))  

            
León = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "León", "Macho", "Carnivoro")
Leona = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "León", "Hembra", "Carnivoro")
Lobo = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Lobo", "Macho", "Carnivoro")
Loba = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Lobo", "Hembra", "Carnivoro")
Cebra = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Cebra", "Macho", "Hervívoro")
Cebra2 = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Cebra", "Hembra", "Hervívoro")
Conejo = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Conejo", "Macho", "Hervívoro")
Coneja = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Conejo", "Hembra", "Hervívoro")
jirafa = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Jirafa", "Macho", "Hervívoro")
Jirafa2 = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Jirafa", "Hembra", "Hervívoro")
Tallo = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 0, "Tallo", "si", "si")
Trigo = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 0, "Trigo", "si", "si")
Orégano = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 0, "Orégano", "si", "si")
Lavanda = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 0, "Lavanda", "si", "si")
Girasol = Planta(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 0, "Girasol", "si", "si")
Abeja = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Abeja", "Macho", "Polen")
Abeja2 = Animal(ra.randint(0,limitX)*32, ra.randint(0,limitY)*32, 100, 100, 100, 1, "Abeja", "Hembra", "Polen")
Soleado = Ambiente(30, 25, "Sol")
Lluvia = Ambiente(15, 90, "Lluvia")
Nieve = Ambiente(-15, 100, "Nieve")
Programa = Ecosistema()
Programa.agregar_organismo(León)
Programa.agregar_organismo(Leona)
Programa.agregar_organismo(Lobo)
Programa.agregar_organismo(Loba)
Programa.agregar_organismo(Conejo)
Programa.agregar_organismo(Coneja)
Programa.agregar_organismo(jirafa)
Programa.agregar_organismo(Jirafa2)
Programa.agregar_organismo(Cebra)
Programa.agregar_organismo(Cebra2)
Programa.agregar_organismo(Tallo)
Programa.agregar_organismo(Trigo)
Programa.agregar_organismo(Orégano)
Programa.agregar_organismo(Lavanda)
Programa.agregar_organismo(Girasol)
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

    with open("registros.log", "w", encoding="utf-8") as archivo:
        for organismo in Programa.organismos:
            if isinstance(organismo, Animal):
                archivo.write(f"Datos de {organismo.especie} {organismo.genero}: ")
            else:
                archivo.write(f"Datos de {organismo.especie}: ")
            archivo.write(f"Posición ({organismo.x}, {organismo.y}), Vida: {organismo.vida}, Energía: {organismo.energia}, Reservas de agua: {organismo.agua}\n")
    Programa.mostrar_registros_pantalla(sWin)
    py.display.flip()
    reloj.tick(1)
py.quit()
    

