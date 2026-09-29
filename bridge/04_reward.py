# Reward 是 environment 对当前 transition / 状态结果给出的评价信号。
# 越大越好
# RL 通常 maximize reward

# Loss / Cost
# 越小越好
# 训练通常 minimize loss

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

    action = policy(observation)

    next_position = position + action

    reward = -abs(goal - next_position)

    print(
        "observation =", observation,
        "| action =", action,
        "| next_position =", next_position,
        "| reward =", reward
    )

    position = next_position