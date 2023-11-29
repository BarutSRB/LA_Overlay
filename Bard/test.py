def calculate_cooldown(base_cooldown, swiftness, gem_multiplier):
    swiftness_reduction = 1 - swiftness * 0.0002146
    adjusted_cooldown = base_cooldown * swiftness_reduction * gem_multiplier
    return adjusted_cooldown

def main():
    try:
        # Asking user for input
        base_cooldown = float(input("Enter Base Cooldown of the skill (in seconds): "))
        swiftness = float(input("Enter Swiftness value: "))
        gem_multiplier = float(input("Enter Gem multiplier (e.g., 0.9 for 10% reduction): "))

        # Calculating the true cooldown
        true_cooldown = calculate_cooldown(base_cooldown, swiftness, gem_multiplier)
        print(f"The true cooldown of the skill is: {true_cooldown:.2f} seconds")

    except ValueError:
        print("Please enter valid numbers for Base Cooldown, Swiftness, and Gem Multiplier.")

if __name__ == "__main__":
    main()
