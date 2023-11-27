from Skill import *

WINDOW_POS_X, WINDOW_POS_Y = 1600, 700 # Position of the overlay

WINDOW_SIZE = (800, 600)
ICON_WIDTH, ICON_HEIGHT = 30, 30
SKILL_GAP, ROW_HEIGHT = 1, ICON_WIDTH + 5


SWIFTNESS = 1830
ALERT_VOLUME = 0.05 # Set to 0 to disable sound

# List of supported skills:

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
Harp_of_Rhythm           =  Skill("Harp_of_Rhythm", 24, 15)
Rhythm_Buckshot          =  Skill("Rhythm_Buckshot", 16, None)
Dissonance_Living        =  Skill("Dissonance", 8+2, 5+2)
Dissonance_No_Living     =  Skill("Dissonance", 8, 5+2)

# You can add a new skill like this:
# Example_New_Skill = Skill("Example_Skill_Name", Cooldown, Buff duration)

# Tripod level 5 for CD is assumed


# Edit your Loadout & Keybinds here:
SKILLS = {
    'q': Sound_Shock,
    'w': Sonic_Vibration,
    'e': Prelude_of_Storm,
    'r': Soundholic,
    'a': Heavenly_Tune,
    's': Guardian_Tune_Agile,
    'd': Rhapsody_of_Light,
    'f': Wind_of_Music,
}


# Edit your gem levels here:
GEMS = {
    0 : [],
    1 : [],
    2 : [],
    3 : [],
    4 : [],
    5 : [],
    6 : [],
    7 : [],
    8 : [],
    9 : [],
    10 : [
    Sound_Shock,
    Sonic_Vibration,
    Prelude_of_Storm,
    Soundholic,
    Heavenly_Tune,
    Guardian_Tune_Agile,
    Rhapsody_of_Light,
    Wind_of_Music,
    ],
}

# These skills will flash red when its cooldowns are below 2 seconds
FLASH_COOLDOWN = [Sonic_Vibration, Heavenly_Tune] 




# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------




for i in FLASH_COOLDOWN:
    i.flash_cd = True
    
for key in SKILLS:
    SKILLS[key].assign_key(key)
    SKILLS[key].swiftness = SWIFTNESS
    
for level in GEMS:
    for skill in GEMS[level]:
        skill.set_gem(1 - level*0.02)


for key in SKILLS:
    SKILLS[key].add_image(ICON_WIDTH, ICON_HEIGHT)
    
    
pygame.mixer.init()
Sonic_Vibration_Sound = pygame.mixer.Sound('./Assets/alert.mp3')
Heavenly_Tune_Sound = pygame.mixer.Sound('./Assets/alert.mp3')

Sonic_Vibration_Sound.set_volume(ALERT_VOLUME)
Heavenly_Tune_Sound.set_volume(ALERT_VOLUME)

Sonic_Vibration.add_sound(Sonic_Vibration_Sound)
Heavenly_Tune.add_sound(Heavenly_Tune_Sound)
