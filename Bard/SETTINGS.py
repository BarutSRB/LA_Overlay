from Skill import *

# Window position and size settings
WINDOW_POS_X, WINDOW_POS_Y = 1600, 700  # Position of the overlay
WINDOW_SIZE = (800, 600)
ICON_WIDTH, ICON_HEIGHT = 30, 30 # Skill icon size
SKILL_GAP, ROW_HEIGHT = 1, ICON_WIDTH + 5

# Volume settings
ALERT_VOLUME = 0.95  # Set to 0 to disable sound

# List of supported skills (Cooldown, Buff duration, Cast Time, Judgement Cooldown)
Sound_Shock         = Skill("Sound_Shock",         3,   4,    0,    judgement_cooldown=4)
Prelude_of_Storm    = Skill("Prelude_of_Storm",    7,   None, 0,    4)
Wind_of_Music       = Skill("Wind_of_Music",       7,   4,    0,    6)
Sonic_Vibration     = Skill("Sonic_Vibration",    12,   6,    0.9,  4)
Rhapsody_of_Light   = Skill("Rhapsody_of_Light",  10,   None, 0,    8)
Soundholic          = Skill("Soundholic",         12,   None, 0,    4)
Heavenly_Tune       = Skill("Heavenly_Tune",      90,   8,    0.5, judgement_cooldown=34)
Guardian_Tune       = Skill("Guardian_Tune",       8,  16,    0,    4)
Sonatina            = Skill("Sonatina",           21,   5,    0,    4)
Stigma              = Skill("Stigma",             16,   9,    0,    4)
Harp_of_Rhythm      = Skill("Harp_of_Rhythm",     24,  15,    0,    4)
Rhythm_Buckshot     = Skill("Rhythm_Buckshot",    16,   None, 0,    4)
Dissonance          = Skill("Dissonance",         10,   7,    0,    4)


# Skill keybinds
SKILLS = {
    "q": Sound_Shock,
    "w": Sonic_Vibration,
    "e": Prelude_of_Storm,
    "r": Soundholic,
    "a": Heavenly_Tune,
    "s": Guardian_Tune,
    "d": Rhapsody_of_Light,
    "f": Wind_of_Music,
}

# Skills that will flash red when their cooldowns are below 2 seconds
FLASH_COOLDOWN = [Sonic_Vibration, Heavenly_Tune]

# -------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------- DO NOT EDIT BELOW --------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------

# Initialize the skills
for skill in FLASH_COOLDOWN:
    skill.flash_cd = True

for key, skill in SKILLS.items():
    skill.assign_key(key)

# Adding images to skills
pygame.mixer.init()
for key, skill in SKILLS.items():
    skill.add_image(ICON_WIDTH, ICON_HEIGHT)

# Sound settings for specific skills
Sonic_Vibration_Sound = pygame.mixer.Sound("./Assets/Sounds/alert.mp3")
Heavenly_Tune_Sound = pygame.mixer.Sound("./Assets/Sounds/alert.mp3")

Sonic_Vibration_Sound.set_volume(ALERT_VOLUME)
Heavenly_Tune_Sound.set_volume(ALERT_VOLUME)

Sonic_Vibration.add_sound(Sonic_Vibration_Sound)
Heavenly_Tune.add_sound(Heavenly_Tune_Sound)
