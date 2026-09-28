# Vacuum Cleaner - Simple Reflex Agent

def simple_reflex_agent(location, status):
    if status == "Dirty":
        return "Suck"

    if location == "A":
        return "Move Right"

    if location == "B":
        return "Move Left"


# Initial environment
rooms = {
    "A": "Dirty",
    "B": "Dirty"
}

location = "A"

print("Initial State:")
print(rooms)
print("Vacuum Location:", location)

while rooms["A"] == "Dirty" or rooms["B"] == "Dirty":

    action = simple_reflex_agent(location, rooms[location])

    print("\nLocation:", location)
    print("Status:", rooms[location])
    print("Action:", action)

    if action == "Suck":
        rooms[location] = "Clean"

    elif action == "Move Right":
        location = "B"

    elif action == "Move Left":
        location = "A"

print("\nFinal State:")
print(rooms)
print("All rooms are clean.")