# Policy = 根据 observation 决定 action 的规则

def policy(observation):

    if observation["position"] < observation["goal"]:
        return 1

    elif observation["position"] > observation["goal"]:
        return -1

    else:
        return 0

position = 1
goal = 5

for step in range(6):

    observation = {
        "position": position,
        "goal": goal
    }

    print("observation:", observation)

    action = policy(observation)

    next_position = position + action

    print(
        "action =", action,
        "| next_position =", next_position
    )

    position = next_position