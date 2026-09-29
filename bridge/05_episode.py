def policy(observation):

    if observation["position"] < observation["goal"]:
        return 1

    elif observation["position"] > observation["goal"]:
        return -1

    else:
        return 0


position = 1
goal = 5


for step in range(10):

    observation = {
        "position": position,
        "goal": goal
    }

    action = policy(observation)

    next_position = position + action

    reward = -abs(goal - next_position)

    # terminated 是一个判断
    terminated = next_position == goal

    print(
        "step =", step,
        "| observation =", observation,
        "| action =", action,
        "| next_position =", next_position,
        "| reward =", reward,
        "| terminated =", terminated
    )

    position = next_position

    if terminated:
        print("Goal reached. Episode finished.")
        break