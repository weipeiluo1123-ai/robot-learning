def policy(observation):

    if observation["position"] < observation["goal"]:
        return 1

    elif observation["position"] > observation["goal"]:
        return -1

    else:
        return 0


position = 1
goal = 5

max_steps = 3


for step in range(max_steps):

    observation = {
        "position": position,
        "goal": goal
    }

    action = policy(observation)

    next_position = position + action

    reward = -abs(goal - next_position)

    terminated = next_position == goal

    truncated = (step == max_steps - 1) and not terminated

    print(
        "step =", step,
        "| observation =", observation,
        "| action =", action,
        "| next_position =", next_position,
        "| reward =", reward,
        "| terminated =", terminated,
        "| truncated =", truncated
    )

    position = next_position

    # 任务完成，正常终止
    if terminated:
        print("Goal reached. Episode terminated.")
        break

    # 时间到了，任务未完成
    if truncated:
        print("Time limit reached. Episode truncated.")
        break