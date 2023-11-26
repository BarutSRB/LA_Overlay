
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




Sound_Shock              =  Skill("Sound_Shock", 6, 4 )
Prelude_of_Storm         =  Skill("Prelude_of_Storm", 16-3, None )
Wind_of_Music            =  Skill("Wind_of_Music", 18-4, 4 )
Sonic_Vibration          =  Skill("Sonic_Vibration", 24, 6 )
Rhapsody_of_Light        =  Skill("Rhapsody_of_Light", 24-5, None )
Soundholic               =  Skill("Soundholic", 24, None )
Heavenly_Tune            =  Skill("Heavenly_Tune", 30-6, 8 )
Guardian_Tune_Wind       =  Skill("Guardian_Tune", 30, 8+8 )
Guardian_Tune_Agile      =  Skill("Guardian_Tune", 15, 4+4 )
Sonatina                 =  Skill("Sonatina", 21-7, 5)
Stigma_Brilliant         =  Skill("Stigma", 16, 4+2+3)
Stigma_Storm             =  Skill("Stigma", 16, None)
Harp_of_Rhythm           =  Skill("Harp_of_Rhythm", 24, None) # Not sure how long the harp lasts
Rhythm_Buckshot          =  Skill("Rhythm_Buckshot", 16, None)
Dissonance_Living        =  Skill("Dissonance", 8+2, 5+2)
Dissonance_No_Living     =  Skill("Dissonance", 8, 5+2)






