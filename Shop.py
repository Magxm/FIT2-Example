from Actor.Player import Player
import pyxel
import math


class Shop:
    def __init__(self, player):
        self.player = player
        self.attackLeveled = 0
        self.attackSpeedLeveled = 0
        self.healthLeveled = 0
        self.movementSpeedLeveled = 0

    def getCost(self, leveled):
        return math.floor(10 * (1 + leveled/3))

    def update(self, gold):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if pyxel.mouse_x >= pyxel.width-16 and pyxel.mouse_y >= pyxel.height-16:
                return True, gold

            if pyxel.mouse_x >= 50 or pyxel.mouse_x <= 66:
                if pyxel.mouse_y >= 80 and pyxel.mouse_y <= 80 + 16:
                    cost = self.getCost(self.attackLeveled)
                    if gold >= cost:
                        self.player.attackDamage += 1 * \
                            (1 + self.attackLeveled/10)
                        self.attackLeveled += 1
                        gold -= cost
                if pyxel.mouse_y >= 80 + 30 and pyxel.mouse_y <= 80 + 30 + 16:
                    cost = self.getCost(self.attackSpeedLeveled)
                    if gold >= cost:
                        self.player.attackSpeed += 0.2 * \
                            (1 + self.attackSpeedLeveled/10)
                        self.attackSpeedLeveled += 1
                        gold -= cost
                if pyxel.mouse_y >= 80 + 30 + 30 and pyxel.mouse_y <= 80 + 30 + 30 + 16:
                    cost = self.getCost(self.healthLeveled)
                    if gold >= cost:
                        self.player.maxHP += 3 * (1 + self.healthLeveled/10)
                        self.healthLeveled += 1
                        gold -= cost
                if pyxel.mouse_y >= 80 + 30 + 30 + 30 and pyxel.mouse_y <= 80 + 30 + 30 + 30 + 16:
                    cost = self.getCost(self.movementSpeedLeveled)
                    if gold >= cost:
                        self.player.movementSpeed += 0.1 * \
                            (1 + self.movementSpeedLeveled/10)
                        self.movementSpeedLeveled += 1
                        gold -= cost

        return False, gold

    def draw(self):
        pyxel.cls(pyxel.COLOR_NAVY)
        y = 50
        x = 50

        pyxel.text(x, y, "Shop", pyxel.COLOR_WHITE)
        y += 30
        pyxel.blt(x, y, 0, 0, 80, 16, 16, 3)
        pyxel.text(x + 24, y + 2,
                   f"Level: {self.attackLeveled}", pyxel.COLOR_WHITE)
        pyxel.text(x + 128, y + 2,
                   f"Attack Damage: {self.player.attackDamage}", pyxel.COLOR_WHITE)
        pyxel.text(
            x + 24, y + 9, f"Cost: {self.getCost(self.attackLeveled)}", pyxel.COLOR_WHITE)
        y += 30
        pyxel.blt(x, y, 0, 0, 96, 16, 16, 3)
        pyxel.text(x + 24, y + 2,
                   f"Level: {self.attackSpeedLeveled}", pyxel.COLOR_WHITE)
        pyxel.text(x + 128, y + 2,
                   f"Attack Speed: {self.player.attackSpeed}", pyxel.COLOR_WHITE)
        pyxel.text(
            x + 24, y + 9, f"Cost: {self.getCost(self.attackSpeedLeveled)}", pyxel.COLOR_WHITE)
        y += 30
        pyxel.blt(x, y, 0, 16, 80, 16, 16, 3)
        pyxel.text(x + 24, y + 2,
                   f"Level: {self.healthLeveled}", pyxel.COLOR_WHITE)
        pyxel.text(x + 128, y + 2,
                   f"Health: {self.player.maxHP}", pyxel.COLOR_WHITE)
        pyxel.text(
            x + 24, y + 9, f"Cost: {self.getCost(self.healthLeveled)}", pyxel.COLOR_WHITE)
        y += 30
        pyxel.blt(x, y, 0, 32, 80, 16, 16, 3)
        pyxel.text(x + 24, y + 2,
                   f"Level: {self.movementSpeedLeveled}", pyxel.COLOR_WHITE)
        pyxel.text(x + 128, y + 2,
                   f"Movement Speed: {self.player.movementSpeed}", pyxel.COLOR_WHITE)
        pyxel.text(
            x + 24, y + 9, f"Cost: {self.getCost(self.movementSpeedLeveled)}", pyxel.COLOR_WHITE)

        # Exit button
        pyxel.blt(pyxel.width-16, pyxel.height-16, 0, 16, 96, 16, 16, 3)
