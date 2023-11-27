import os
import pygame
import win32gui
import win32con
import win32api

from SETTINGS import (WINDOW_POS_X, 
                      WINDOW_POS_Y, 
                      ICON_HEIGHT,
                      ICON_WIDTH, 
                      SKILL_GAP, 
                      WINDOW_SIZE, 
                      ROW_HEIGHT)


# Set the window position and initialize Pygameaqd
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{WINDOW_POS_X},{WINDOW_POS_Y}'
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
pygame.display.set_caption('Skill Cooldown Tracker')

# Make window transparent and always on topra
hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)



# Function to update display
def update_display(skills, gauge):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36) #Change Font or Size of Font
    current_time = pygame.time.get_ticks()

    for i, (key, skill) in enumerate(skills.items()):
        x, y = calculate_position(i)
        handle_skill_flash(skill, key, x, y, current_time)
        draw_cooldown_and_buff_bars(skill, key, x, y, font)

    draw_gauge_circles(gauge, 80, 30)  # Set your desired position for gauge circles

    pygame.display.flip()

def calculate_position(index):
    x = 50 + (index % 4) * (ICON_WIDTH + SKILL_GAP)
    y = 50 + (index // 4) * ROW_HEIGHT
    return x, y

def handle_skill_flash(skill, key, x, y, current_time):
    if skill.flash_cd and 0 < skill.current_buff <= 2 and (current_time // 200) % 2: #Flashing speed 200ms per second
        red_icon = pygame.Surface((ICON_WIDTH, ICON_HEIGHT), pygame.SRCALPHA)
        red_icon.fill((255, 0, 0)) #Color of flashing image, currently red
        red_icon.blit(skill.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(red_icon, (x, y))
    else:
        screen.blit(skill.image, (x, y))

def draw_cooldown_and_buff_bars(skill, key, x, y, font):

    if skill.current_cd > 0:
        draw_cooldown_overlay(skill, x, y)
        draw_cooldown_text(skill.current_cd, x, y, font, skill)
    if  skill.buff is not None and skill.current_buff > 0:
        draw_buff_bar(skill, x, y)

def draw_cooldown_overlay(skill, x, y):
    overlay = pygame.Surface((ICON_WIDTH, ICON_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((128, 128, 128))
    screen.blit(overlay, (x, y))

def draw_cooldown_text(cooldown, x, y, font, skill):
    if cooldown < 1:
        # Display with one decimal place if cooldown is less than 1 second
        rounded = round(cooldown, 1)
    else:
        # Display as an integer if cooldown is 1 second or more
        rounded = int(cooldown)

    text = font.render(str(rounded), True, (255, 255, 255))  # Countdown font color currently white
    text_rect = text.get_rect(center=(x + ICON_WIDTH / 2, y + ICON_HEIGHT / 2))
    screen.blit(text, text_rect.topleft)

def draw_buff_bar(skill,  x, y):
    buff_bar_width = int((skill.current_buff / skill.buff) * ICON_WIDTH)
    buff_bar = pygame.Surface((buff_bar_width, 5))
    buff_bar.fill((0, 255, 0))
    screen.blit(buff_bar, (x, y + ICON_HEIGHT))

def draw_gauge_circles(gauge, x, y):
    circle_radius = 10
    circle_gap = 5
    for i in range(gauge):
        pygame.draw.circle(screen, (0, 0, 255), (x + i * (circle_radius * 2 + circle_gap), y), circle_radius)

# # Function to block key events
# def block_key_event(skill_states, key):
#     def on_key_event(e):
#         #other_key = 'w' if key == 'a' else 'a' #Key blocking
#         #if skill_states[other_key]['buff'] > 0: #Key blocking
#             #return False #Key blocking
#         return True
#     return on_key_event