import pygame as py
from pygame.locals import *
import time as ti
import random as ra
import ctypes as ct

nRES = (1184, 576)
ok = True
nT_WX = nT_HY = 32

class Celdas(ct.Structure):
    _fields_ = [
        ('nT', ct.c_ubyte),  # Tipo de Tile/Baldosa
        ('nD', ct.c_ubyte),  # Tile Disponible?
        ('nS', ct.c_ubyte),  # 0 : No se pinta - # 1 : Si se pinta
        ('nF', ct.c_ubyte),  # Fila de Mapa
        ('nC', ct.c_ubyte),  # Columna de Mapa
        ('nR', ct.c_ubyte),  # Recurso a Explotar:
                            # 1:Acero
                            # 2:Cobre
                            # 3:Litio
                            # 4:Butano
        ('nQ', ct.c_ubyte)   # Cantidad del Recurso
    ]

class Accion():
    def __init__(self):
        self.aMap = [
            [Celdas() for nC in range(nRES[0]//nT_WX)] for nF in range(nRES[1]//nT_HY)
        ]

    def Init_PyGame(self):
        py.init()
        py.mouse.set_visible(True)
        py.display.set_caption('')
        return py.display.set_mode(nRES)

    def Load_Image(self, sFile, transp=False):
        try:
            image = py.image.load(sFile)
        except py.error:
            raise SystemExit
        image = image.convert()
        if transp:
            color = image.get_at((0, 0))
            image.set_colorkey(color, RLEACCEL)
        return image

    def Carga_Imagenes(self):
        imagenes = []
        imagenes.append(self.Load_Image('T01.png', False))
        imagenes.append(self.Load_Image('T02.png', False))
        imagenes.append(self.Load_Image('T03.png', False))
        return imagenes

    def Init_Mapa(self):
        for nF in range(0, nRES[1] // nT_HY):
            for nC in range(0, nRES[0] // nT_WX):
                self.aMap[nF][nC].nT = ra.randint(0,2)
                self.aMap[nF][nC].nD = 1  # 1: Disponible - 0: No Disponible
                self.aMap[nF][nC].nS = 0  # No se pinta por Defecto
                self.aMap[nF][nC].nF = nF  # Fila de la Celda
                self.aMap[nF][nC].nC = nC  # Colu de la Celda
                self.aMap[nF][nC].nR = self.aMap[nF][nC].nT
                self.aMap[nF][nC].nQ = ra.randint(100, 1000)  # Unidades de RR
        return

    def Pinta_Mapa(self, sWin, aFig):
        for nF in range(0, nRES[1] // nT_HY):
            for nC in range(0, nRES[0] // nT_WX):
                if nF <= 10 and nC <= 18:  
                    if self.aMap[nF][nC].nT == 0:
                        sWin.blit(aFig[0], (nC * nT_HY, nF * nT_WX))  
                    elif self.aMap[nF][nC].nT == 1:
                        sWin.blit(aFig[1], (nC * nT_HY, nF * nT_WX)) 
                    else:
                        sWin.blit(aFig[0], (nC * nT_HY, nF * nT_WX))                    
    
        py.display.flip()

Programa = Accion()
sWin = Programa.Init_PyGame()
aFig = Programa.Carga_Imagenes()
Programa.Init_Mapa()

while ok:
    for e in py.event.get():
        if e.type == QUIT:
            ok = False
    Programa.Pinta_Mapa(sWin, aFig)
