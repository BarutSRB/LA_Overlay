import pygame
import keyboard
import threading
import tkinter as tk
import pyautogui
import time
import os
import json
from time import sleep
from overlay import update_display
from SETTINGS import SKILLS

global_cooldown_active = False

# Bard Gauge Code
class DraggableRectangle:
    def __init__(self, canvas, x, y, width, height, tag):
        self.canvas = canvas
        self.tag = tag
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill='blue', tags=tag)
        self.width = width
        self.height = height
        self.canvas.tag_bind(self.tag, '<ButtonPress-1>', self.on_press)
        self.canvas.tag_bind(self.tag, '<B1-Motion>', self.on_drag)

    def on_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.tag, dx, dy)
        self.x = event.x
        self.y = event.y

    def get_position(self):
        return self.canvas.coords(self.rect)

def setup_gui():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    canvas = tk.Canvas(root, cursor='cross')
    canvas.pack(fill=tk.BOTH, expand=True)

    positions = {}  # Initialize positions dictionary
    saved_positions_file = 'positions.json'

    # Load positions if file exists
    if os.path.exists(saved_positions_file):
        with open(saved_positions_file, 'r') as file:
            saved_positions = json.load(file)
    else:
        saved_positions = {'Bar1': [100, 100], 'Bar2': [200, 100], 'Bar3': [300, 100]}

    bars = {}
    for bar_name, pos in saved_positions.items():
        bars[bar_name] = DraggableRectangle(canvas, pos[0], pos[1], 20, 80, bar_name.lower())

    def on_key_press(event):
        if event.char == 'q':
            for bar_name, bar in bars.items():
                positions[bar_name] = bar.get_position()
            with open(saved_positions_file, 'w') as file:
                json.dump(positions, file)
            root.destroy()

    root.bind('<Key>', on_key_press)
    root.mainloop()
    return positions


def check_bars(positions):
    gauge = 0

    # Check Bar1
    bar1_pos = positions['Bar1']
    bar1_found = False
    if bar1_pos:
        try:
            if pyautogui.locateOnScreen('bar.png', region=(int(bar1_pos[0]), int(bar1_pos[1]), 20, 80), confidence=0.8):
                bar1_found = True
                gauge = 1
        except pyautogui.ImageNotFoundException:
            pass

    # Check Bar2
    bar2_pos = positions['Bar2']
    bar2_found = False
    if bar1_found and bar2_pos:
        try:
            if pyautogui.locateOnScreen('bar.png', region=(int(bar2_pos[0]), int(bar2_pos[1]), 20, 80), confidence=0.8):
                bar2_found = True
                gauge = 2
        except pyautogui.ImageNotFoundException:
            pass

    # Check Bar3
    bar3_pos = positions['Bar3']
    if bar1_found and bar2_found and bar3_pos:
        try:
            if pyautogui.locateOnScreen('bar.png', region=(int(bar3_pos[0]), int(bar3_pos[1]), 20, 80), confidence=0.8):
                gauge = 3
        except pyautogui.ImageNotFoundException:
            pass

    return gauge

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
    positions = setup_gui()
    skills = SKILLS
    threading.Thread(target=manage_skills, args=(skills,), daemon=True).start()
    start_keyboard_listener(skills)
    clock = pygame.time.Clock()
    running = True
    while running:
        gauge = check_bars(positions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_display(skills, gauge)  # Pass gauge to the update_display function
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
