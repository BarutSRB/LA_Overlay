from Skill import *

# Window position and size settings
WINDOW_POS_X, WINDOW_POS_Y = 1500, 10  # Position of the overlay
WINDOW_SIZE = (600, 101)
ICON_WIDTH, ICON_HEIGHT = 48, 48 # Skill icon size
SKILL_GAP, ROW_HEIGHT = 2, ICON_WIDTH + 5

# Volume settings
ALERT_VOLUME = 0.95  # Set to 0 to disable sound

# Swiftness of your Character
SWIFTNESS = 1794

# Skill cooldown reductions ([ Tripods, CD-Gem (e.g. Lv. 10 -> 20) ])
SKILL_COOLDOWN_REDUCTIONS = {
    "DrawingOrchids": [0, 10],
    "Hopper": [0, 10],
    "IllusionDoor": [0, 10],
    "StarryNight": [0, 10],
    "Sunsketch": [0, 10],
    "SunWell": [5.2, 12],
    "PouncingTiger": [9.7, 10],
    "UpwardStroke": [0, 10],
    
    # Ultimate Skill -50% from Awakening Engraving
    "Efflorescence": [0, 50]
}

# (skill cd - tripods) * (1-swift cdr) * (1-cd gem)
def calcCooldown(skillName, skillCD):
    baseCD = 2.147027027
    skillTripodCD = skillCD - SKILL_COOLDOWN_REDUCTIONS.get(skillName, [0,0])[0]
    cdrSwiftness = (round((SWIFTNESS * baseCD) / 100, 2) / 100.0)
    cdrGem = (SKILL_COOLDOWN_REDUCTIONS.get(skillName, [0,0])[1] / 100.0)
    calculatedCD = skillTripodCD * (1-cdrSwiftness) * (1-cdrGem)
    # print(skillName, calculatedCD, ' | ', skillTripodCD, cdrSwiftness, cdrGem)
    return calculatedCD


# List of supported skills (Cooldown, Buff duration, Cast Time, Judgement Cooldown)
DrawingOrchids      = Skill("DrawingOrchids", calcCooldown("DrawingOrchids", 24), 13.5, 0.5, 0)
Efflorescence       = Skill("Efflorescence", calcCooldown("Efflorescence", 300), 12, 0, 0)
Hopper              = Skill("Hopper", calcCooldown("Hopper", 16), 3, 0, 0)
IllusionDoor        = Skill("IllusionDoor", calcCooldown("IllusionDoor", 36), 10, 0, 0)
StarryNight         = Skill("StarryNight", calcCooldown("StarryNight", 24), None, 2.3, 0)
Moonfall            = Skill("Moonfall", 0, 10, 0, 0)
Sunrise             = Skill("Sunrise", 0, None, 0, 0)
Sunsketch           = Skill("Sunsketch", calcCooldown("Sunsketch", 27), 8, 0, 0)
SunWell             = Skill("SunWell", calcCooldown("SunWell", 30), 6, 0, 0)
PouncingTiger       = Skill("PouncingTiger", calcCooldown("PouncingTiger", 30), None, 0, 0)
UpwardStroke        = Skill("UpwardStroke", calcCooldown("UpwardStroke", 16), None, 0, 0)


# Skill keybinds
SKILLS = {
    "q": DrawingOrchids,
    "w": Sunsketch,
    "e": SunWell,
    "r": IllusionDoor,
    "a": Hopper,
    "s": PouncingTiger,
    "d": StarryNight,
    "f": UpwardStroke,
#    "x": Sunrise,
    "y": Moonfall,
    "v": Efflorescence,
}

# Skills that will flash red when their cooldowns are below 2 seconds
FLASH_COOLDOWN = [DrawingOrchids, Sunsketch, SunWell, Efflorescence]

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
# DrawingOrchids_Sound = pygame.mixer.Sound("./Assets/Sounds/alert.mp3")
# Sunsketch_Sound = pygame.mixer.Sound("./Assets/Sounds/alert.mp3")
# SunWell_Sound = pygame.mixer.Sound("./Assets/Sounds/alert.mp3")
# Efflorescence_Sound = pygame.mixer.Sound("./Assets/Sounds/alert.mp3")

# DrawingOrchids_Sound.set_volume(ALERT_VOLUME)
# Sunsketch_Sound.set_volume(ALERT_VOLUME)
# SunWell_Sound.set_volume(ALERT_VOLUME)
# Efflorescence_Sound.set_volume(ALERT_VOLUME)

# DrawingOrchids.add_sound(DrawingOrchids_Sound)
# Sunsketch.add_sound(Sunsketch_Sound)
# SunWell.add_sound(SunWell_Sound)
# Efflorescence.add_sound(Efflorescence_Sound)