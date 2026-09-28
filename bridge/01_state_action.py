state = 1

actions = [1, 1, -1, 1]

print("initial state:", state)

for action in actions:
    next_state = state + action

    print(
        "state =", state,
        "| action =", action,
        "| next_state =", next_state
    )

    state = next_state