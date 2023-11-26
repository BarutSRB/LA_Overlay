
import pygame
from time import time

class Skill():
    def __init__(self, name, cooldown, buff):
        self.last_used = -1
        self.name = name
        self.default_cooldown = cooldown
        self.buff = buff
        self.sound_played = True
        self.gem_multiplier = 1
        self.swiftness = 0 
        self.flash_cd = False
        self.sound = None

    @property
    def cooldown(self):
        return self.default_cooldown * (1 - self.swiftness * 0.0002146) * self.gem_multiplier
        
    def assign_key(self, key):
        self.keybind = key
        
    def set_gem(self, multiplier):
        self.gem_multiplier = multiplier
        
    @property
    def current_cd(self,):
        # Remaining cooldown duration
        return self.cooldown - (time() - self.last_used)
        # these are negative if the skill is ready / buff has ended
    @property
    def current_buff(self):
        # Remaining buff duration
        if self.buff is None:
            return None
        return self.buff - (time() - self.last_used)
    
    def use(self):
        if self.current_cd <= 0:
            self.last_used = time()
            self.sound_played = False
        
    def check_sound(self):
        if self.sound is not None and self.current_buff <= 1 and not self.sound_played:
            self.sound.play()
            self.sound_played = True
        
    def add_image(self, ICON_WIDTH, ICON_HEIGHT):
        self.image = pygame.transform.scale(pygame.image.load("./Bard/Assets/"+self.name+".png"),(ICON_WIDTH, ICON_HEIGHT) )
        self.rect = self.image.get_rect()
        
    def add_sound(self, sound):
        self.sound = sound



