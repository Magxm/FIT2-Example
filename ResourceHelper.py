from tkinter import Y
from Vector2 import Vector2
import pyxel
import Config
import random

cellsPerRow = int(255 // 16)
floorCellCount = 3
wallCellsIndexStart = cellsPerRow
corridorCellIndexStart = cellsPerRow * 2
corridorCellCount = 1


def DrawCell(index, x, y, color=None):
    screenX = x
    screenY = y
    spriteX = (index % cellsPerRow) * 16
    spriteY = (index // cellsPerRow) * 16
    pyxel.blt(screenX, screenY, 0, spriteX, spriteY, 16, 16, color)


def DrawFloorTile(screenPos: Vector2, index=0):
    rX = screenPos.X
    rY = screenPos.Y
    DrawCell(index % floorCellCount, rX, rY)


def DrawDecoration(screenPos: Vector2, index=0):
    rX = screenPos.X
    rY = screenPos.Y
    DrawCell(floorCellCount + index, rX, rY, 3)


def DrawCorridorTile(screenPos: Vector2, index=0):
    rX = screenPos.X
    rY = screenPos.Y
    DrawCell(corridorCellIndexStart + (index % 1), rX, rY)


def DrawWallTile(screenPos: Vector2, index=0):
    rX = screenPos.X
    rY = screenPos.Y
    DrawCell(wallCellsIndexStart + index, rX, rY)


def DrawPlayer(screenPos: Vector2, forward):
    if forward:
        pyxel.blt(screenPos.X, screenPos.Y, 0, 0,
                  240, 16, 16, 3)
    else:
        pyxel.blt(screenPos.X, screenPos.Y, 0, 16,
                  240, 16, 16, 3)


def DrawMonster(screenPos: Vector2, forward):
    if forward:
        pyxel.blt(screenPos.X, screenPos.Y, 0, 0,
                  224, 16, 16, 3)
    else:
        pyxel.blt(screenPos.X, screenPos.Y, 0, 16,
                  224, 16, 16, 3)
