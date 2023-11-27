import pygame
import keyboard
import threading
from time import sleep

from overlay import update_display
from SETTINGS import SKILLS

global_cooldown_active = False

# Global cast cooldown
def global_cooldown():
    global global_cooldown_active
    sleep(1)  # This is the global cooldown period
    global_cooldown_active = False

# Skill management in a single thread
def manage_skills(skills):
    while True:
        for skill in skills:
            skills[skill].check_sound()
        sleep(1/60)
                   
# Function to handle skill activation
def handle_skill_activation(key, skills):
    global global_cooldown_active
    if global_cooldown_active:
        return
    skill = skills[key]
    if skill.current_cd <= 0:
        skill.use()
        # Start global cooldown
        global_cooldown_active = True
        threading.Thread(target=lambda: global_cooldown(), daemon=True).start()
        
# Keyboard listener
def start_keyboard_listener(skills):
    keyboard.on_press(lambda e: handle_skill_activation(e.name, skills) if e.name in skills.keys() else None)
    
def main():
    skills = SKILLS
    threading.Thread(target=manage_skills, args=(skills,), daemon=True).start()
    start_keyboard_listener(skills)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_display(skills)
        clock.tick(60) #Refresh rate in FPS, currently 60 FPSd
    pygame.quit()

if __name__ == "__main__":
    main()
