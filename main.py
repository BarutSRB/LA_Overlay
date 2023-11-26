import os
import subprocess

class Color:
    BRIGHT_RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    END = '\033[0m'

def main():
    classes = {
        "Warrior": ["Berserker", "Paladin", "Gunlancer", "Destroyer", "Slayer"],
        "Martial Artist": ["Striker", "Wardancer", "Scrapper", "Soulfist", "Glavier"],
        "Gunner": ["Gunslinger", "Artillerist", "Deadeye", "Sharpshooter", "Machinist"],
        "Mage": ["Bard", "Sorceress", "Arcanist", "Summoner"],
        "Assassin": ["Shadowhunter", "Deathblade", "Reaper", "Souleater"],
        "Specialist": ["Artist", "Aeromancer"]
    }

    print(f"{Color.BRIGHT_RED}Choose a class:{Color.END}")
    for index, class_name in enumerate(classes, start=1):
        print(f"{index}. {class_name}")

    class_choice = int(input(f"{Color.GREEN}Enter your choice (number): {Color.END}")) - 1
    class_name = list(classes.keys())[class_choice]

    print(f"{Color.BRIGHT_RED}Choose a subclass for {class_name}:{Color.END}")
    for index, subclass in enumerate(classes[class_name], start=1):
        print(f"{index}. {subclass}")

    subclass_choice = int(input(f"{Color.GREEN}Enter your choice (number): {Color.END}")) - 1
    subclass_name = classes[class_name][subclass_choice]

    run_overlay_script(subclass_name)

def run_overlay_script(subclass_name):
    try:
        os.chdir(subclass_name)
        subprocess.run(["python", "main.py"])
    except FileNotFoundError:
        print(f"{Color.BLUE}Currently, a profile for your chosen subclass does not exist. However, you can create one by following the instructions in the guide available at:\n\nhttps://github.com/BarutSRB/LA_Overlay/blob/main/GUIDE.md\n\nIf you do create a profile, we encourage you to contribute it to the community.{Color.END}")

if __name__ == "__main__":
    main()
