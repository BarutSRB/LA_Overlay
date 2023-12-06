import json
import os
import threading
from time import sleep, time

import keyboard
import pyautogui
import pygame
import tkinter as tk

from overlay import update_display
from SETTINGS import SKILLS

global judgement_buff_active, judgement_start_time
global_cooldown_active = False
judgement_buff_active = False
judgement_buff_duration = 7
judgement_start_time = None


class DraggableRectangle:
    def __init__(self, canvas, x, y, width, height, tag):
        self.canvas = canvas
        self.tag = tag
        self.rect = canvas.create_rectangle(
            x, y, x + width, y + height, fill="blue", tags=tag
        )
        self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)

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
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)

    positions = {}
    saved_positions_file = "positions.json"

    if os.path.exists(saved_positions_file):
        with open(saved_positions_file, "r") as file:
            saved_positions = json.load(file)
    else:
        saved_positions = {"Bar1": [100, 100], "Bar2": [200, 100], "Bar3": [300, 100]}
        saved_positions.setdefault("Judgement", [400, 100])

    bars = {}
    for bar_name, pos in saved_positions.items():
        bars[bar_name] = DraggableRectangle(
            canvas,
            pos[0],
            pos[1],
            300 if bar_name == "Judgement" else 20,
            24 if bar_name == "Judgement" else 80,
            bar_name.lower(),
        )

    def on_key_press(event):
        if event.char == "q":
            for bar_name, bar in bars.items():
                positions[bar_name] = bar.get_position()
            with open(saved_positions_file, "w") as file:
                json.dump(positions, file)
            root.destroy()

    root.bind("<Key>", on_key_press)
    root.mainloop()
    return positions


def check_bars(positions):
    global judgement_buff_active
    gauge = 0

    def check_bar(bar_pos, bar_length, image="./Assets/OCR/bar.png"):
        try:
            if pyautogui.locateOnScreen(
                image,
                region=(int(bar_pos[0]), int(bar_pos[1]), bar_length, 80),
                confidence=0.8,
            ):
                return True
        except pyautogui.ImageNotFoundException:
            pass
        return False

    # Checking the normal bars
    if check_bar(positions["Bar1"], 20):
        gauge = 1
        if check_bar(positions["Bar2"], 20):
            gauge = 2
            if check_bar(positions["Bar3"], 20):
                gauge = 3

    # Checking for Judgement using judgment.png
    if not judgement_buff_active and positions.get("Judgement"):
        if check_bar(positions["Judgement"], 300, image="./Assets/OCR/judgement.png"):
            judgement_buff_active = True
            judgement_start_time = pygame.time.get_ticks() / 1000
            threading.Thread(target=handle_judgement_buff, daemon=True).start()

    return gauge


def handle_judgement_buff():
    global judgement_buff_active
    start_time = time()
    while time() - start_time < judgement_buff_duration:
        sleep(0.1)
    judgement_buff_active = False


def global_cooldown():
    global global_cooldown_active
    sleep(1)
    global_cooldown_active = False


def manage_skills(skills):
    while True:
        for skill in skills:
            skills[skill].check_sound()
        sleep(1 / 60)


def handle_skill_activation(key, skills):
    global global_cooldown_active, judgement_buff_active
    if global_cooldown_active:
        return
    skill = skills[key]
    skill.use(during_judgement=judgement_buff_active)
    global_cooldown_active = True
    threading.Thread(target=lambda: global_cooldown(), daemon=True).start()


def start_keyboard_listener(skills):
    keyboard.on_press(
        lambda e: handle_skill_activation(e.name, skills)
        if e.name in skills.keys()
        else None
    )


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
        update_display(skills, gauge, judgement_buff_active, judgement_start_time, judgement_buff_duration)
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
