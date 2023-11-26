import os
import pygame
import threading
import time
import win32gui
import win32con
import win32api
import keyboard

# GUI Constants
ICON_WIDTH, ICON_HEIGHT = 30, 30
SKILL_GAP, ROW_HEIGHT = 1, ICON_WIDTH + 5
WINDOW_POS_X, WINDOW_POS_Y = 1650, 1000
WINDOW_SIZE = (800, 600)

# Global cooldown variable
global_cooldown_active = False

# Set the window position and initialize Pygame
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{WINDOW_POS_X},{WINDOW_POS_Y}'
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
pygame.display.set_caption('Skill Cooldown Tracker')

#Sound
pygame.mixer.init()
skill_a_sound = pygame.mixer.Sound('alert.wav')
skill_w_sound = pygame.mixer.Sound('alert.wav')

# Make window transparent and always on top
hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)

# Skill Data
skills = {
    'q': {'icon': 'Sound_Shock.png', 'cooldown': 4, 'buff': 4},
    'w': {'icon': 'Sonic_Vibration.png', 'cooldown': 14, 'buff': 6},
    'e': {'icon': 'Prelude_of_Storm.png', 'cooldown': 8, 'buff': None},
    'r': {'icon': 'Soundholic.png', 'cooldown': 14, 'buff': None},
    'a': {'icon': 'Heavenly_Tune.png', 'cooldown': 14, 'buff': 8},
    's': {'icon': 'Guardian_Tune.png', 'cooldown': 9, 'buff': 8},
    'd': {'icon': 'Rhapsody_of_Light.png', 'cooldown': 11, 'buff': None},
    'f': {'icon': 'Wind_of_Music.png', 'cooldown': 8, 'buff': None}
}

# Load and resize skill icons
for skill in skills.values():
    skill['image'] = pygame.transform.scale(pygame.image.load(skill['icon']), (ICON_WIDTH, ICON_HEIGHT))
    skill['rect'] = skill['image'].get_rect()

# Global variables for skill cooldowns and buff uptimes
skill_states = {key: {'cooldown': 0, 'buff': 0} for key in skills.keys()}

# Skill management in a single thread
def manage_skills():
    buff_end_sound_played = {'a': False, 'w': False}

    while True:
        for key, state in skill_states.items():
            # Handle cooldowns
            if state['cooldown'] > 0:
                state['cooldown'] -= 1

            # Handle buffs
            if state['buff'] > 0:
                state['buff'] -= 1
                if key in buff_end_sound_played:
                    buff_end_sound_played[key] = False

            # Handle sound playback for A and W skill buffs when ended
            if key in ['a', 'w'] and state['buff'] == 2 and not buff_end_sound_played[key]:
                if key == 'a':
                    skill_a_sound.play()
                elif key == 'w':
                    skill_w_sound.play()
                buff_end_sound_played[key] = True

        time.sleep(1)

threading.Thread(target=manage_skills, daemon=True).start()

# Function to update display
def update_display():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36) #Change Font or Size of Font
    current_time = pygame.time.get_ticks()

    for i, (key, skill) in enumerate(skills.items()):
        x, y = calculate_position(i)
        handle_skill_flash(skill, key, x, y, current_time)
        draw_cooldown_and_buff_bars(skill, key, x, y, font)

    pygame.display.flip()

def calculate_position(index):
    x = 50 + (index % 4) * (ICON_WIDTH + SKILL_GAP)
    y = 50 + (index // 4) * ROW_HEIGHT
    return x, y

def handle_skill_flash(skill, key, x, y, current_time):
    if key in ['a', 'w'] and 0 < skill_states[key]['buff'] <= 2 and (current_time // 200) % 2: #Flashing speed 200ms per second
        red_icon = pygame.Surface((ICON_WIDTH, ICON_HEIGHT), pygame.SRCALPHA)
        red_icon.fill((255, 0, 0)) #Color of flashing image, currently red
        red_icon.blit(skill['image'], (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(red_icon, (x, y))
    else:
        screen.blit(skill['image'], (x, y))

def draw_cooldown_and_buff_bars(skill, key, x, y, font):
    cooldown = skill_states[key]['cooldown']
    buff = skill_states[key]['buff']
    if cooldown > 0:
        draw_cooldown_overlay(skill, x, y)
        draw_cooldown_text(cooldown, x, y, font, skill)
    if buff and skill['buff']:
        draw_buff_bar(skill, buff, x, y)

def draw_cooldown_overlay(skill, x, y):
    overlay = pygame.Surface((ICON_WIDTH, ICON_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((128, 128, 128))
    screen.blit(overlay, (x, y))

def draw_cooldown_text(cooldown, x, y, font, skill):
    text = font.render(str(cooldown), True, (255, 255, 255)) #Countdown font color currently white
    text_rect = text.get_rect(center=(x + ICON_WIDTH / 2, y + ICON_HEIGHT / 2))
    screen.blit(text, text_rect.topleft)

def draw_buff_bar(skill, buff, x, y):
    buff_bar_width = int((buff / skill['buff']) * ICON_WIDTH)
    buff_bar = pygame.Surface((buff_bar_width, 5))
    buff_bar.fill((0, 255, 0))
    screen.blit(buff_bar, (x, y + ICON_HEIGHT))

# Function to block key events
def block_key_event(skill_states, key):
    def on_key_event(e):
        #other_key = 'w' if key == 'a' else 'a' #Key blocking
        #if skill_states[other_key]['buff'] > 0: #Key blocking
            #return False #Key blocking
        return True
    return on_key_event

# Start keyboard blocker
def start_keyboard_blocker():
    for key in ['a', 'w']:
        keyboard.hook_key(key, block_key_event(skill_states, key), suppress=True)

# Function to handle skill activation
def handle_skill_activation(key):
    global global_cooldown_active
    if global_cooldown_active:
        return
    skill = skills[key]
    state = skill_states[key]
    if state['cooldown'] == 0:
        global_cooldown_active = True
        threading.Thread(target=lambda: global_cooldown(), daemon=True).start()
        state['cooldown'] = skill['cooldown']
        if skill['buff']:
            state['buff'] = skill['buff']

# Start global cooldown
def global_cooldown():
    global global_cooldown_active
    time.sleep(1)
    global_cooldown_active = False

# Keyboard listener
def start_keyboard_listener():
    keyboard.on_press(lambda e: handle_skill_activation(e.name) if e.name in skills.keys() else None)

# Main function
def main():
    start_keyboard_listener()
    start_keyboard_blocker()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_display()
        clock.tick(60) #Refresh rate in FPS, currently 60 FPS
    pygame.quit()

if __name__ == "__main__":
    main()
