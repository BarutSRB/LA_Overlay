import os
import pygame
import win32gui
import win32con
import win32api

from SETTINGS import (
    WINDOW_POS_X,
    WINDOW_POS_Y,
    ICON_HEIGHT,
    ICON_WIDTH,
    SKILL_GAP,
    WINDOW_SIZE,
    ROW_HEIGHT,
)


# Set the window position and initialize Pygame
os.environ["SDL_VIDEO_WINDOW_POS"] = f"{WINDOW_POS_X},{WINDOW_POS_Y}"
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
pygame.display.set_caption("Skill Cooldown Tracker")

# Make window transparent and always on top
hwnd = win32gui.GetForegroundWindow()
win32gui.SetWindowPos(
    hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
)
win32gui.SetWindowLong(
    hwnd,
    win32con.GWL_EXSTYLE,
    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    | win32con.WS_EX_LAYERED
    | win32con.WS_EX_TRANSPARENT,
)
win32gui.SetLayeredWindowAttributes(
    hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
)


def update_display(skills, gauge, judgement_buff_active, judgement_start_time, judgement_buff_duration):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 36)
    current_time = pygame.time.get_ticks()

    for i, (key, skill) in enumerate(skills.items()):
        x, y = calculate_position(skill, skills)
        handle_skill_flash(skill, key, x, y, current_time)
        draw_cooldown_and_buff_bars(skill, key, x, y, font)

    draw_gauge_circles(gauge, 80, 67)  # Set your desired position for gauge circles

    # Draw rune and progress bar if judgement is active
    if judgement_buff_active:
        if judgement_start_time is not None:
            elapsed_time = pygame.time.get_ticks() / 1000 - judgement_start_time
            if elapsed_time <= judgement_buff_duration:
                draw_rune_and_progress(screen, judgement_start_time, judgement_buff_duration)
            else:
                judgement_buff_active = False

    pygame.display.flip()


def calculate_position(skill, skills):
    global_x_adjustment = 66

    if skill.name == "Efflorescence":
        # x_adjustment = -70
        # y_adjustment = -36

        # bottom_row_y = 50 + (1 * ROW_HEIGHT)
        # x = 30 + x_adjustment + global_x_adjustment
        # y = bottom_row_y + y_adjustment
        return 0, 0
    else:
        index = list(skills.keys()).index(skill.keybind)
        x = 0 + (index % 10) * (ICON_WIDTH + SKILL_GAP) + global_x_adjustment
        y = 0 + (index // 10) * ROW_HEIGHT
        return x, y


def handle_skill_flash(skill, key, x, y, current_time):
    if (
        skill.flash_cd
        and skill.current_buff is not None
        and 0 < skill.current_buff <= 2
        and (current_time // 200) % 2  # Flashing speed 200ms per second
    ):
        # Determine the size of the flashing icon
        flash_icon_width = ICON_WIDTH
        flash_icon_height = ICON_HEIGHT
        if skill.name == "Efflorescence":
            flash_icon_width = 64
            flash_icon_height = 64

        red_icon = pygame.Surface((flash_icon_width, flash_icon_height), pygame.SRCALPHA)
        red_icon.fill((255, 0, 0))  # Color of flashing image, currently red
        red_icon.blit(skill.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(red_icon, (x, y))
    else:
        screen.blit(skill.image, (x, y))


def draw_cooldown_and_buff_bars(skill, key, x, y, font):
    if skill.current_cd > 0:
        draw_cooldown_overlay(skill, x, y)
        draw_cooldown_text(skill.current_cd, x, y, font, skill)
    if (
        skill.buff is not None
        and skill.current_buff is not None
        and skill.current_buff > 0
    ):
        draw_buff_bar(skill, x, y)


def draw_cooldown_overlay(skill, x, y):
    # Determine the size of the cooldown overlay
    overlay_width = ICON_WIDTH
    overlay_height = ICON_HEIGHT
    if skill.name == "Efflorescence":
        overlay_width = 64
        overlay_height = 64

    overlay = pygame.Surface((overlay_width, overlay_height))
    overlay.set_alpha(128)
    overlay.fill((128, 128, 128))
    screen.blit(overlay, (x, y))


def draw_cooldown_text(cooldown, x, y, font, skill):
    if cooldown < 1:
        # Display with one decimal if cooldown is less than 1 second
        rounded = round(cooldown, 1)
    else:
        # Display without decimals if cooldown is 1 or more seconds
        rounded = int(cooldown)

    text = font.render(str(rounded), True, (255, 255, 255))
    text_rect = text.get_rect()

    # Adjust text position for Efflorescence
    if skill.name == "Efflorescence":
        text_x = x + (64 - text_rect.width) / 2
        text_y = y + (64 - text_rect.height) / 2
    else:
        text_x = x + (ICON_WIDTH - text_rect.width) / 2
        text_y = y + (ICON_HEIGHT - text_rect.height) / 2

    screen.blit(text, (text_x, text_y))


def draw_buff_bar(skill, x, y):
    bar_width = ICON_WIDTH
    if skill.name == "Efflorescence":
        bar_width = 64

    # Calculate the current width of the buff bar based on the buff duration
    buff_bar_width = int((skill.current_buff / skill.buff) * bar_width)

    # Ensure that the buff bar does not exceed the width of the icon
    buff_bar_width = min(buff_bar_width, bar_width)

    buff_bar = pygame.Surface((buff_bar_width, 5))
    buff_bar.fill((0, 255, 0))  # Green progress bar

    # Position the bar below the icon
    bar_y = y + ICON_HEIGHT
    if skill.name == "Efflorescence":
        bar_y = y + 64

    screen.blit(buff_bar, (x, bar_y))


def draw_gauge_circles(gauge, x, y):
    circle_radius = 10
    circle_gap = 5
    for i in range(gauge):
        pygame.draw.circle(
            screen,
            (200, 200, 0),
            (x + i * (circle_radius * 2 + circle_gap), y),
            circle_radius,
        )


def draw_rune_and_progress(screen, judgement_start_time, judgement_buff_duration):
    if judgement_start_time is None:
        return
    current_time = pygame.time.get_ticks() / 1000
    elapsed_time = current_time - judgement_start_time
    remaining_time = max(judgement_buff_duration - elapsed_time, 0)

    # Load judgment image
    rune_image = pygame.transform.scale(pygame.image.load("./Assets/Buffs/ConJud.png"), (ICON_WIDTH, ICON_HEIGHT))
    rune_x, rune_y = 80, 20  # Set position for judgment buff image
    screen.blit(rune_image, (rune_x, rune_y))

    # Draw progress bar
    progress_bar_width = int((remaining_time / judgement_buff_duration) * ICON_WIDTH)
    progress_bar = pygame.Surface((progress_bar_width, 5))
    progress_bar.fill((255, 0, 0))  # Red progress bar
    screen.blit(progress_bar, (rune_x, rune_y + ICON_HEIGHT + 5))