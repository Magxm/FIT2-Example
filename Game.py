import pyxel
from Actor.Player import Player
import ResourceHelper
from Vector2 import Vector2
from Level import Level
from Shop import Shop
import Config
import random
import math
import os
import sys
import threading
import time

# Allow imports from all project directories
sys.path.insert(0, sys.path[0])
# sys.path.insert(1, os.path.join(sys.path[0], "Map"))
# sys.path.insert(2, os.path.join(
#       os.path.join(sys.path[0], "Map"), "TilePresets"))


class App:
    def __init__(self):
        pyxel.init(Config.SCREEN_HEIGHT, Config.SCREEN_WIDTH)
        pyxel.mouse(True)
        # We load all the resources here
        pyxel.load("Resources\\resources.pyxres")

        pyxel.image(1).load(0, 0, "Resources\\LoadingText.png")

        self.playMusic = True
        pyxel.playm(0, loop=True)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.player = Player()
        self.levelNumber = 0
        self.inShop = False
        self.shop = Shop(self.player)
        self.gold = 0
        self.loadNextLevel()

    def loadNextLevelInternal(self):
        self.loadingLevel = True
        self.level = Level(self.levelNumber, self.player)
        self.loadingLevel = False

    def loadNextLevel(self):
        self.loadingLevel = True
        self.levelNumber += 1
        loadingThread = threading.Thread(target=self.loadNextLevelInternal)
        loadingThread.start()
        pyxel.cls(7)
        imageSize = 300
        offsetX = (Config.SCREEN_WIDTH - imageSize) / 2
        offsetY = (Config.SCREEN_HEIGHT - imageSize) / 2
        pyxel.blt(offsetX, offsetY, 1, 0, 0, imageSize, imageSize)
        pyxel.flip()
        while(self.loadingLevel):
            time.sleep(0.1)

    def update(self):
        if self.inShop:
            done, self.gold = self.shop.update(self.gold)
            if done:
                self.inShop = False
                pyxel.stop(0)
                if self.playMusic:
                    pyxel.playm(0, loop=True)
                self.loadNextLevel()

            return

        status = self.level.update(self)
        if (status == 1 or pyxel.btnp(pyxel.KEY_P)):
            pyxel.stop(0)
            if self.playMusic:
                pyxel.playm(1, loop=True)
            self.inShop = True
        elif(status == 2):
            self.reset()

        if (pyxel.btnp(pyxel.KEY_O)):
            self.playMusic = not self.playMusic
            if self.playMusic:
                pyxel.playm(0, loop=True)
            else:
                pyxel.stop(0)

        if (pyxel.btnp(pyxel.KEY_I)):
            self.gold += 100

    def draw(self):
        pyxel.cls(0)
        if self.inShop:
            self.shop.draw()
        else:
            self.level.draw()

        pyxel.blt(0, 0, 0, 0, 64, 16, 16, 3)
        pyxel.text(16, 6, f"{self.gold}", 7)


App()
