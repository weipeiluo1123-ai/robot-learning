import gymnasium as gym
import mani_skill.envs

# 创建 PickCube environment
env = gym.make(
    "PickCube-v1",
    num_envs=1,
    obs_mode="state_dict",
    sim_backend="physx_cpu",
    render_backend="none",
)

obs, info = env.reset(seed=0)

print("reset success!")
print("observation type:", type(obs))
print("observation keys:", obs.keys())
print("info:", info)

env.close()