def policy(observation):
    if observation["position"] < observation["goal"]:
        return 1
    elif observation["position"] > observation["goal"]:
        return -1
    else:
        return 0

def env_step(position, goal, action, step, max_steps):

    # 1. environment 执行 action
    next_position = position + action

    # 2. environment 生成新的 observation
    next_observation = {
        "position": next_position,
        "goal": goal
    }

    # 3. environment 计算 reward
    reward = -abs(goal - next_position)

    # 4. environment 判断任务是否自然结束
    terminated = next_position == goal

    # 5. environment 判断是否达到时间限制
    truncated = (step == max_steps - 1) and not terminated

    # 6. 把这一步的结果全部返回
    return (
        next_position,
        next_observation,
        reward,
        terminated,
        truncated
    )


position = 1
goal = 5

max_steps = 10


observation = {
    "position": position,
    "goal": goal
}


for step in range(max_steps):

    action = policy(observation)

    (
        position,
        observation,
        reward,
        terminated,
        truncated
    ) = env_step(
        position,
        goal,
        action,
        step,
        max_steps
    )

    print(
        "step =", step,
        "| observation =", observation,
        "| action =", action,
        "| reward =", reward,
        "| terminated =", terminated,
        "| truncated =", truncated
    )

    if terminated or truncated:
        print("Episode finished.")
        break