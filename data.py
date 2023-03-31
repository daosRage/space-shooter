import pygame
import os

setting_win = {
    "WIDTH": 1200,
    "HEIGHT": 800,
    "FPS": 60,
    "NAME_GAME": "Space Shooter"
}
setting_hero = {
    "WIDTH": 265,
    "HEIGHT": 175,
    "SPEED": 5
}

setting_boss = {
    "WIDTH": 600,
    "HEIGHT": 200,
    "HP": 10
}
setting_game = {
    
}

hero_destroy_coord = {
    "RECT1": [setting_hero["WIDTH"] // 2 - 62]
}

time_list = []

bots_list = []
bots_shot_list = []
boss_shot_list = []
buff_list = []


abs_path = os.path.abspath(__file__ + "/..") + "\\image\\"

bg_image = pygame.transform.scale(pygame.image.load(abs_path + "background.jpg"), (setting_win["WIDTH"], setting_win["HEIGHT"]))
hero_fly_1_image = pygame.image.load(abs_path + "hero_fly_1.png")
hero_fly_2_image = pygame.image.load(abs_path + "hero_fly_2.png")
hero_down_image = pygame.image.load(abs_path + "hero_down.png")
hero_up_1_image = pygame.image.load(abs_path + "hero_up_1.png")
hero_up_2_image = pygame.image.load(abs_path + "hero_up_2.png")
hero_left_1_image = pygame.image.load(abs_path + "hero_left_1.png")
hero_left_2_image = pygame.image.load(abs_path + "hero_left_2.png")
hero_right_1_image = pygame.image.load(abs_path + "hero_right_1.png")
hero_right_2_image = pygame.image.load(abs_path + "hero_right_2.png")
bullet_image = pygame.image.load(abs_path + "bullet.png")
gun_image = pygame.image.load(abs_path + "gun.png")
heal_image = pygame.image.load(abs_path + "heal.png")

boss_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(abs_path + "hero.png"), (setting_boss["WIDTH"], setting_boss["HEIGHT"])), 180)

hero_fly_list_image = [hero_fly_1_image, hero_fly_2_image]
hero_left_list_image = [hero_left_1_image, hero_left_2_image]
hero_right_list_image = [hero_right_1_image, hero_right_2_image]
hero_up_list_image = [hero_up_1_image, hero_up_2_image]
hero_down_list_image = [hero_down_image, hero_down_image]
bot_list_image = [pygame.transform.rotate(hero_up_1_image, 180), pygame.transform.rotate(hero_up_2_image, 180)]

boss_image_list = [boss_image, boss_image]