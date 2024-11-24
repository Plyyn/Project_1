"""Модуль для реализации основного цикла игры"""

import pygame
import random
from resources import load_resources


class Game:
    """Класс, представляющий основной игровой процесс"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 375))
        pygame.display.set_caption("The best game ever")
        self.clock = pygame.time.Clock()
        #загрузка игровых ресурсов
        self.bg, self.walking, self.cactus, self.coin, self.bg_sound, self.coin_sound = load_resources()
        self.bg_sound.play()
        #игровые переменные
        self.cactus_list = []
        self.coin_list = []
        self.anim_count = 0
        self.bg_x = 0
        self.player_y = 285
        self.is_jump = False
        self.jump_count = 8
        self.gameplay = True
        self.running = True
        self.score = 0
        #шрифты
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 45)
        self.restart_font = pygame.font.Font(None, 40)
        #переменные для генерации кактусов и монет
        self.time_to_next_cactus = random.randint(1300, 3000)
        self.last_cactus_time = pygame.time.get_ticks()
        self.time_to_next_coin = random.randint(1300, 3000)
        self.last_coin_time = pygame.time.get_ticks()

    def run(self):
        """Основной цикл игры"""
        while self.running:
            self.quit()
            self.update()
            self.draw()
            self.clock.tick(12)

    def quit(self):
        """Обрабатывает выход из игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Обновляет состояние игры"""
        keys = pygame.key.get_pressed()

        if self.gameplay:
            self.update_gameplay(keys)
        else:
            self.draw_game_over()

    def update_gameplay(self, keys):
        """Обновляет элементы во время игры"""
        self.score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 0))
        player_rect = self.walking[0].get_rect(topleft=(70, self.player_y))
#создаем анимацию персонажа
        if self.anim_count == 3:
            self.anim_count = 0
        else:
            self.anim_count += 1
#обрабатываем прыжок
        if not self.is_jump:
            if keys[pygame.K_SPACE]:
                self.is_jump = True
        else:
            self.handle_jump()

        self.handle_obstacles(player_rect)#обрабатываем столкновения
        self.update_background()#обновляем фон
        # генерируем новые кактусы и монеты
        current_time = pygame.time.get_ticks()
        self.spawn_obstacles(current_time)

    def handle_jump(self):
        """Функция обрабатывает прыжок персонажа"""
        if self.jump_count >= -8:
            if self.jump_count > 0:
                self.player_y -= (self.jump_count ** 2) / 2
            else:
                self.player_y += (self.jump_count ** 2) / 2
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 8

    def handle_obstacles(self, player_rect):
        """Функция обрабатывает столкновение с кактусом и с монетками"""
        if self.cactus_list:
            for el in self.cactus_list:
                el.x -= 8
                if el.x < -100:
                    self.cactus_list.remove(el)
                if player_rect.colliderect(el):
                    print("GAME OVER")
                    self.gameplay = False #при столкновении с кактусом игра завершается

        if self.coin_list:
            for i in range(len(self.coin_list) - 1, -1, -1):
                elem = self.coin_list[i]
                elem.x -= 8
                if elem.x < -50:
                    self.coin_list.pop(i)
                elif player_rect.colliderect(elem):
                    self.coin_list.pop(i)
                    self.score += 1
                    self.coin_sound.play() #при сборе монетки игроку начисляется 1 очко и играет звук сбора монетки

    def update_background(self):
        """Функция обновляет фон и создает эффект движения"""
        self.bg_x -= 3
        if self.bg_x <= -600:
            self.bg_x = 0

    def spawn_obstacles(self, current_time):
        """Создает кактусы и монеты в случайные моменты времени"""
        if current_time - self.last_cactus_time > self.time_to_next_cactus:
            self.cactus_list.append(self.cactus.get_rect(topleft=(620, 280)))
            self.last_cactus_time = current_time
            self.time_to_next_cactus = random.randint(1300, 3000)

        if current_time - self.last_coin_time > self.time_to_next_coin:
            self.coin_list.append(self.coin.get_rect(topleft=(620, 230)))
            self.last_coin_time = current_time
            self.time_to_next_coin = random.randint(1300, 3000)

    def draw(self):
        """Функция отображает текущий кадр игры"""
        self.screen.blit(self.bg, (self.bg_x, 0))
        self.screen.blit(self.bg, (self.bg_x + 600, 0))
        self.screen.blit(self.walking[self.anim_count], (70, self.player_y))

        if self.gameplay:
            self.screen.blit(self.score_text, (10, 10))
            for el in self.cactus_list:
                self.screen.blit(self.cactus, el)
            for elem in self.coin_list:
                self.screen.blit(self.coin, elem)
        else:
            self.draw_game_over()

        pygame.display.update()

    def draw_game_over(self):
        """Функция отображает экран завершения игры и перезапускает ее при желании пользователя"""
        self.screen.fill((255, 228, 225))
        lose_text = self.game_over_font.render("GAME OVER:(", True, (238, 130, 238))
        restart_text = self.restart_font.render("Tap to restart", True, (238, 130, 238))
        restart_text_rect = restart_text.get_rect(topleft=(210, 210))#надпись "tap to restart" является кнопкой перезапуска
        self.screen.blit(lose_text, (200, 150))
        self.screen.blit(restart_text, restart_text_rect)
# делаем так, чтобы при нажатии на кнопку перезапуска, игра перезапускалась с обнуленными параметрами
        mouse = pygame.mouse.get_pos()
        if restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            self.gameplay = True
            self.score = 0
            self.cactus_list.clear()
            self.coin_list.clear()

