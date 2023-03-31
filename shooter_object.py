import pygame
from data import *
import random

class Shooter(pygame.Rect):
    def __init__(self, x, y, width, height, speed, image):
        super().__init__(x, y, width, height)
        self.IMAGE = image[0]
        self.IMAGE_LIST = image
        self.SPEED = speed
        self.IMAGE_MOVE = 0
    
    def move_image(self):
        self.IMAGE = self.IMAGE_LIST[self.IMAGE_MOVE // 10]
        self.IMAGE_MOVE += 1
        if self.IMAGE_MOVE == 20:
            self.IMAGE_MOVE = 0

class Hero(Shooter):
    def __init__(self, x, y, width, height, speed, image):
        super().__init__(x, y, width, height, speed, image)
        self.MOVE = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False}
        self.HP = 3
        self.POINT = 0
        self.ALL_POINT = 0
        self.BULLETS = []
        self.BULLET_COUNTER = 0
        self.GUN = 0


    def move(self):
        if self.MOVE["UP"] and self.y > 0:
            self.y -= self.SPEED
        elif self.MOVE["DOWN"] and self.y < setting_win["HEIGHT"] - self.height:
            self.y += self.SPEED
        if self.MOVE["LEFT"] and self.x > 0:
            self.x -= self.SPEED
        elif self.MOVE["RIGHT"] and self.x < setting_win["WIDTH"] - self.width:
            self.x += self.SPEED
        #if self.IMAGE_MOVE == 0 or self.IMAGE_MOVE == 10:
        self.move_image()

class Bot(Shooter):
    def __init__(self, x, y, width, height, speed, image):
        super().__init__(x, y, width, height, speed, image)
        self.MAKE_SHOT = True

    def move(self, find_bot, hero):
        self.y += self.SPEED
        self.move_image()
        if self.y > setting_win["HEIGHT"] + self.height:
            bots_list.remove(find_bot)
        elif self.colliderect(hero):
            hero.HP -= 1
            hero.POINT += 10
            bots_list.remove(find_bot)

class Boss(Shooter):
    def __init__(self, x, y, width, height, speed, image):
        super().__init__(x, y, width, height, speed, image)
        self.HP = 10
        self.VISIBILITY = False
    
    def move(self):
        self.move_image()
        if self.y < 50:
            self.y += self.SPEED
        elif self.x < 100 or self.x > setting_win["WIDTH"] - 100 - setting_boss["WIDTH"]:
            self.SPEED *= -1
            self.x += self.SPEED
        else:
            self.x += self.SPEED

class Buff(pygame.Rect):
    def __init__(self, x, y, width= 50, height= 50, buff = None, image = None):
        super().__init__(x, y, width, height)
        self.BUFF = buff
        self.IMAGE = image
    

class Shot(pygame.Rect):
    def __init__(self, x, y, width, height, image, speed, bot = None):
        super().__init__(x, y, width, height)
        self.IMAGE = image
        self.SPEED = speed
        self.BOT = bot

    def move_bullet(self, hero, boss, find_bullet, who_shot = False, number_bullets= 0):
        self.y += self.SPEED
        tmp_key = False
        if who_shot == "hero":
            for bot in bots_list:
                if self.colliderect(bot):
                    hero.POINT += 10
                    r = random.randint(1, 100)
                    if  1 <= r  and  r <= 100: 
                        if r <= 10:
                            buff_list.append(Buff(bot.x, bot.y, image= heal_image, buff= "heal"))
                        if r < 100:
                            buff_list.append(Buff(bot.x, bot.y, image= gun_image, buff= "gun"))
                            print(1)
                    bots_list.remove(bot)
                    hero.BULLETS[number_bullets].remove(find_bullet)
                    tmp_key = True
            if tmp_key:
                pass
            elif self.y < 0:
                print(2, find_bullet)
                hero.BULLETS[number_bullets].remove(find_bullet)
            elif self.colliderect(boss):
                print(find_bullet)
                print(hero.BULLETS)
                boss.HP -= 1
                hero.BULLETS[number_bullets].remove(find_bullet)
        #влучання пулі в героя
        elif who_shot == "bot":
            if self.BOT != False:
                if self.colliderect(hero):
                    hero.HP -= 1
                    bots_shot_list.remove(find_bullet)
                    self.BOT.MAKE_SHOT = True
                elif self.y > setting_win["HEIGHT"]:
                    bots_shot_list.remove(find_bullet)
                    self.BOT.MAKE_SHOT = True
            else:
                if self.colliderect(hero):
                    hero.HP -= 1
                    bots_shot_list.remove(find_bullet)
                elif self.y > setting_win["HEIGHT"]:
                    bots_shot_list.remove(find_bullet)
        elif who_shot == "boss":
            if self.colliderect(hero):
                hero.HP -= 1
                boss_shot_list[number_bullets].remove(find_bullet)
            elif self.y > setting_win["HEIGHT"]:
                boss_shot_list[number_bullets].remove(find_bullet)

    
