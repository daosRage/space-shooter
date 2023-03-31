import pygame
from data import *
from shooter_object import *
from time import *
from random import *

pygame.init()

window = pygame.display.set_mode((setting_win["WIDTH"], setting_win["HEIGHT"]))
pygame.display.set_caption(setting_win["NAME_GAME"])

def run():
    game = True
    start_time = 0
    end_time = 0
    lvl = 1
    start_time_bot = pygame.time.get_ticks()
    end_time_botAndShot = 0
    stop_shot = -3000
    wich_window = 1
    
    font_text = pygame.font.Font(None, 40)
    font_shot_counter = pygame.font.Font(None, 30)
    
    clock = pygame.time.Clock()

    hero = Hero(setting_win["WIDTH"] // 2 - setting_hero["WIDTH"] // 2, 
                setting_win["HEIGHT"] - setting_hero["HEIGHT"], 
                setting_hero["WIDTH"], 
                setting_hero["HEIGHT"], 
                setting_hero["SPEED"], 
                hero_fly_list_image)
    boss = Boss(setting_win["WIDTH"] // 2 - setting_boss["WIDTH"] // 2,
                -setting_boss["HEIGHT"],
                setting_boss["WIDTH"],
                setting_boss["HEIGHT"],
                1,
                boss_image_list)


    while game:
        window.blit(bg_image, (0, 0))
        

        window.blit(font_text.render(f"HP: {hero.HP}", True, (255, 0, 0)), (setting_win["WIDTH"] - 100, 10))
        window.blit(font_text.render(f"Point: {hero.POINT}", True, (0, 255, 0)), (setting_win["WIDTH"] - 250, 10))

        window.blit(hero.IMAGE, (hero.x, hero.y))

        
        #start_time = time()
        hero.move()
        window.blit(font_shot_counter.render(f"{5 - hero.BULLET_COUNTER}", True, (255, 0, 0)), (hero.x + hero.width, hero.y))
        #end_time = time()
        #time_list.append(end_time - start_time)

        #hero
        print(hero.BULLETS )
        number_bullets = 0
        for bullets in hero.BULLETS:
            for bullet in bullets:
                print("bulllet =>", bullet )
                bullet.move_bullet(hero, boss, bullet, who_shot= "hero", number_bullets= number_bullets)
                window.blit(bullet.IMAGE, (bullet.x, bullet.y))
            number_bullets += 1

        for buff in buff_list:
            buff.y += 1
            window.blit(buff.IMAGE, (buff.x, buff.y))
            if buff.colliderect(hero) and buff.BUFF == "heal":
                hero.HP += 1
                buff_list.remove(buff)
            if buff.colliderect(hero) and buff.BUFF == "gun":
                hero.GUN = 2
                print(hero.GUN)
                buff_list.remove(buff)
        if True:
            pass
        
        #проходимо по списку ботів, для кожного окремого бота запускаємо відображення картинки на екрані
        #також запускаємо функцію руху для кожного бота
        for bot in bots_list:
            window.blit(bot.IMAGE, (bot.x, bot.y))
            bot.move(bot, hero)
            if bot.MAKE_SHOT:
                bots_shot_list.append(Shot(bot.x + bot.width // 2 - 5, bot.y + bot.height, 10, 20, bullet_image, 3, bot= bot))
                bot.MAKE_SHOT = False
            #if not bot.MAKE_SHOT:
            #    window.blit(bot.SHOT.IMAGE, (bot.SHOT.x, bot.SHOT.y))
            #    bot.SHOT.move_bullet(hero, bot = bot, find_bullet = bot.SHOT)

        for bullet in bots_shot_list:
            window.blit(bullet.IMAGE, (bullet.x, bullet.y))
            bullet.move_bullet(hero, boss, bullet, who_shot= "bot")
        #умовний оператор для появи ботів
        end_time_botAndShot = pygame.time.get_ticks()
        if end_time_botAndShot - start_time_bot > 2000 and hero.POINT < 100:
            bots_list.append(Bot(randint(   0, 
                                            setting_win["WIDTH"] - setting_hero["WIDTH"] // 3), 
                                            -setting_hero["HEIGHT"], 
                                            setting_hero["WIDTH"], 
                                            setting_hero["HEIGHT"], 
                                            1, 
                                            bot_list_image))
            start_time_bot = end_time_botAndShot
        #BOSS
        if hero.POINT >= 100 :
            window.blit(boss_image, (boss.x, boss.y))
            boss.move()

            if end_time_botAndShot - start_time_bot > 2000:
                boss_shot_list.append([Shot(boss.x + setting_boss["WIDTH"] // 2 - 57, boss.y + setting_boss["HEIGHT"] - 15, 10, 20, bullet_image, 3),
                                       Shot(boss.x + setting_boss["WIDTH"] // 2 + 57, boss.y + setting_boss["HEIGHT"] - 15, 10, 20, bullet_image, 3)])
                start_time_bot = end_time_botAndShot
            #print(boss.x, boss.y)
            number_bullets = 0
            for bullets in boss_shot_list:
                for bullet in bullets:
                    bullet.move_bullet(hero, boss, bullet, who_shot= "boss", number_bullets= number_bullets)
                    window.blit(bullet.IMAGE, (bullet.x, bullet.y))
                    print(bullet.x, bullet.y)
                number_bullets += 1
            #boss die
            if boss.HP <= 0:
                hero.POINT += 100
                hero.ALL_POINT += hero.POINT
                hero.POINT = 0
                window.blit(pygame.font.SysFont("Comic Sans MS", 100, bold= "True").render(f"Рівень {lvl}", True, (161, 76, 179)), 
                            (setting_win["WIDTH"] // 2 - 100, setting_win["HEIGHT"] // 2 - 50))
                pygame.display.flip()
                lvl += 1
                boss.HP = 10
                boss.x = setting_win["WIDTH"] // 2 - setting_boss["WIDTH"] // 2
                boss.y = -setting_boss["HEIGHT"]
                sleep(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = True
                    hero.IMAGE_LIST = hero_up_list_image
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = True
                    hero.IMAGE_LIST = hero_down_list_image
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = True
                    hero.IMAGE_LIST = hero_left_list_image
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = True
                    hero.IMAGE_LIST = hero_right_list_image
                if event.key == pygame.K_SPACE and end_time_botAndShot - stop_shot > 3000:
                    hero.BULLETS.append([   Shot(hero.x + hero.width // 2 - 37, hero.y, 10, 20, bullet_image, -10),
                                            Shot(hero.x + hero.width // 2 + 37, hero.y, 10, 20, bullet_image, -10)])
                    if hero.GUN == 2:
                        print(hero.GUN)
                        hero.BULLETS.append([Shot(hero.x + 20, hero.y + 80, 10, 20, bullet_image, -10),
                                            Shot(hero.x + hero.width- 20, hero.y + 80, 10, 20, bullet_image, -10)])
                    hero.BULLET_COUNTER += 1
                    if hero.BULLET_COUNTER == 5:
                        stop_shot = end_time_botAndShot
                        hero.BULLET_COUNTER = 0
                if event.key == pygame.K_r:
                    hero.BULLET_COUNTER = 0
                    stop_shot = end_time_botAndShot
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.MOVE["UP"] = False
                    hero.IMAGE_LIST = hero_fly_list_image
                if event.key == pygame.K_s:
                    hero.MOVE["DOWN"] = False
                    hero.IMAGE_LIST = hero_fly_list_image
                if event.key == pygame.K_a:
                    hero.MOVE["LEFT"] = False
                    hero.IMAGE_LIST = hero_fly_list_image
                if event.key == pygame.K_d:
                    hero.MOVE["RIGHT"] = False
                    hero.IMAGE_LIST = hero_fly_list_image

        clock.tick(setting_win["FPS"])
        pygame.display.flip()

run()
#a = 0
#for t in time_list:
#        a += t
#        print(t)
#print(a/len(time_list))