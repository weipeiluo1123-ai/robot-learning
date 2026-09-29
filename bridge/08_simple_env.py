def policy(observation):

    if observation["position"] < observation["goal"]:
        return 1

    elif observation["position"] > observation["goal"]:
        return -1

    else:
        return 0


class SimpleEnv:

    def __init__(self):
        self.start_position = 1
        self.goal = 5
        self.max_steps = 10

        self.position = self.start_position
        self.step_count = 0


    def reset(self):

        self.position = self.start_position
        self.step_count = 0

        observation = {
            "position": self.position,
            "goal": self.goal
        }

        return observation


    def step(self, action):

        # 1. execute action
        self.position = self.position + action

        # 2. one more environment step
        self.step_count = self.step_count + 1

        # 3. generate new observation
        observation = {
            "position": self.position,
            "goal": self.goal
        }

        # 4. calculate reward
        reward = -abs(self.goal - self.position)

        # 5. check termination
        terminated = self.position == self.goal

        # 6. check time limit
        truncated = (
            self.step_count >= self.max_steps
            and not terminated
        )

        return observation, reward, terminated, truncated


env = SimpleEnv()

observation = env.reset()

print("reset observation:", observation)


while True:

    action = policy(observation)

    observation, reward, terminated, truncated = env.step(action)

    print(
        "observation =", observation,
        "| action =", action,
        "| reward =", reward,
        "| terminated =", terminated,
        "| truncated =", truncated
    )

    if terminated or truncated:
        print("Episode finished.")
        break