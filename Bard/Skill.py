import pygame
from time import time

class Skill:
    def __init__(self, name, cooldown, buff, cast_time=0, judgement_cooldown=None):
        self.name = name
        self.cooldown = cooldown
        self.judgement_cooldown = judgement_cooldown or cooldown
        self.buff = buff
        self.cast_time = cast_time
        self.last_used = -1
        self.sound_played = True
        self.sound = None
        self.image = None
        self.flash_cd = False
        self.rect = None
        self.used_during_judgement = False

    def assign_key(self, key):
        self.keybind = key

    @property
    def current_cd(self):
        return max(0, self.cooldown - (time() - self.last_used))

    @property
    def current_buff(self):
        if self.buff is None:
            return None
        buff_start_time = self.last_used + self.cast_time
        current_buff_value = max(0, self.buff - (time() - buff_start_time))
        return current_buff_value

    def use(self, during_judgement=False):
        if self.current_cd <= 0:
            self.last_used = time()
            if during_judgement and self.judgement_cooldown is not None:
                self.last_used -= (self.cooldown - self.judgement_cooldown)
            self.used_during_judgement = during_judgement
            self.sound_played = False

    def check_sound(self):
        if self.sound and self.current_buff is not None and self.current_buff <= 1 and not self.sound_played:
            self.sound.play()
            self.sound_played = True

    def add_image(self, icon_width, icon_height):
        self.image = pygame.transform.scale(pygame.image.load("./Assets/Skills/"+self.name+".png"), (icon_width, icon_height))
        self.rect = self.image.get_rect()

    def add_sound(self, sound):
        self.sound = sound
