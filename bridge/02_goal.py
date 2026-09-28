position = 1
goal = 5

actions = [1, 1, -1, 1]


for action in actions:

    observation = {
        "position": position,
        "goal": goal
    }

    print("observation:", observation)

    next_position = position + action

    print(
        "action =", action,
        "| next_position =", next_position
    )

    position = next_position