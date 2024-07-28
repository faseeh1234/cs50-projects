import cs50

# Check if height within range
while True:
    height = cs50.get_int("Height: ")
    if height > 0 and height < 9:
        break
# Initiate two counters
counter = 0
counter2 = 0
# Loop to print out spaces or #s
for counter in range(height):
    for counter2 in range(height):
        if height - counter2 > counter + 1:
            print(" ", end="")
        else:
            print("#", end="")

    print()
