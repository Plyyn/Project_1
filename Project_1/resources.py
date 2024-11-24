
"""Модуль для загрузки ресурсов, необходимых в игре"""
import pygame

def load_image(path):
    """Функция загружает изображение"""
    return pygame.image.load(path).convert_alpha()


def load_sound(path):
    """Функция загружает звук """
    return pygame.mixer.Sound(path)


def load_resources():
    # Загрузка изображений
    bg = load_image('images/bg.jpg')
    walking = [
        load_image('images/player/5.png'),
        load_image('images/player/6.png'),
        load_image('images/player/7.png'),
        load_image('images/player/8.png')
    ]
    cactus = load_image('images/cactus.png')
    coin = load_image('images/coin.png')

    # Загрузка звуков
    bg_sound = load_sound('music/suoundtrack.mp3')
    coin_sound = load_sound('music/coins.mp3')

    return bg, walking, cactus, coin, bg_sound, coin_sound