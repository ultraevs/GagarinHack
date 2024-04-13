def calculate_multipliers(x, y, width, height):
    x_multiplier = x / width
    y_multiplier = y / height
    return [x_multiplier, y_multiplier]

image_width = 999
image_height = 618


user_input = input()


x, y = map(int, user_input.split())


multipliers = calculate_multipliers(x, y, image_width, image_height)

print(f"[{multipliers[0]:.5f}, {multipliers[1]:.5f}]")
