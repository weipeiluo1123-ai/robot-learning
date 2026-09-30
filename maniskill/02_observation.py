import gymnasium as gym
import mani_skill.envs


env = gym.make(
    "PickCube-v1",
    num_envs=1,
    obs_mode="state_dict",
    sim_backend="physx_cpu",
    render_backend="none",
)

obs, info = env.reset(seed=0)

print("Top-level keys:")
print(obs.keys())

print("\nagent keys:")
print(obs["agent"].keys())

print("\nextra keys:")
print(obs["extra"].keys())

env.close()