from pathlib import Path
import time

import mujoco
import mujoco.viewer

import numpy as np

xml_path = Path(__file__).with_name("arm.xml")

model = mujoco.MjModel.from_xml_path(str(xml_path))
data = mujoco.MjData(model)

# IK测试
ik_data = mujoco.MjData(model)

target_pos = np.array([-0.8, 0.0, 0.7])

best_error = float("inf")
best_q = None
best_pos = None

q1_values = np.linspace(-1.5, 1.5, 121)
q2_values = np.linspace(-1.5, 1.5, 121) 

for q1 in q1_values:
    for q2 in q2_values:
        ik_data.qpos[:] = [q1, q2]
        mujoco.mj_forward(model, ik_data)

        ee_pos = ik_data.site("end_effector").xpos.copy()
        error = np.linalg.norm(ee_pos - target_pos)

        if error < best_error:
            best_error = error
            best_q = [q1, q2]
            best_pos = ee_pos

print("Target position:", target_pos)
print("Best joint angles:", best_q)
print("Best end-effector position:", best_pos)
print("Position error:", best_error)

test_data = mujoco.MjData(model)

# 测试xmat
configs = [
    [0.0, 0.0],
    [0.7, 0.0],
    [0.7, 0.5],
]

for q in configs:
    test_data.qpos[:] = q

    mujoco.mj_forward(model, test_data)

    link1 = test_data.body("link1")
    link2 = test_data.body("link2")
    ee = test_data.site("end_effector")

    print("\n====================")
    print("qpos =", test_data.qpos.copy())

    print("\nlink1 position:")
    print(link1.xpos.copy())
    print("link1 orientation:")
    print(link1.xmat.reshape(3, 3))

    print("\nlink2 position:")
    print(link2.xpos.copy())
    print("link2 orientation:")
    print(link2.xmat.reshape(3, 3))

    print("\nEE position:")
    print(ee.xpos.copy())
    print("EE orientation:")
    print(ee.xmat.reshape(3, 3))

    # print()
    # print("qpos =", test_data.qpos.copy())
    # print("position =", ee.xpos.copy())
    # print("orientation =")
    # print(ee.xmat.reshape(3, 3))

test_data.qpos[:] = [0.7, 0.0]
mujoco.mj_forward(model, test_data)

site = test_data.site("end_effector")

p = site.xpos.copy()
R = site.xmat.reshape(3, 3).copy()

local_point = np.array([0.1, 0.0, 0.0])
world_point = p + R @ local_point
recovered_local_point = R.T @ (world_point - p)

print("EE origin in world =", p)
print("local point =", local_point)
print("world point =", world_point)
print("recovered local point =", recovered_local_point)


print("nq =", model.nq)
print("nv =", model.nv)
print("nu =", model.nu)

# data.qpos[0] = 0.0
# data.qpos[1] = -0.8

data.ctrl[0] = 0.6
data.ctrl[1] = -0.8
# data.ctrl[:] = [0.6, -0.8]

mujoco.mj_forward(model, data)

playback_speed = 0.3

trail = []

step_count = 0

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.perf_counter()

        # 决定控制命令 控制信号在前 0.5 秒为 [0.6, -0.8]，之后为 [-0.6, 0.8]
        # if data.time < 0.5:
        #     data.ctrl[:] = [0.6, -0.8]
        # else:
        #     data.ctrl[:] = [-0.6, 0.8]

        data.ctrl[:] = best_q

        mujoco.mj_step(model, data)

        # 获取末端执行器位置并记录轨迹 这里的"end_effector"是xml中定义的site名称 .xpos是末端执行器在世界坐标系下的位置如(x,y,z)
        end_effector_pos = data.site("end_effector").xpos.copy()

        cartesian_error = np.linalg.norm(end_effector_pos - target_pos)

        step_count += 1

        if step_count % 50 == 0:
            print(
                f"time={data.time:.2f}, "
                f"q={data.qpos.copy()}, "
                f"qvel={data.qvel.copy()}, "
                f"error={cartesian_error:.4f}"
            )

        trail.append(end_effector_pos)

        if len(trail) > 200:
            trail.pop(0)    # 弹出最老的那一个

        # print(
        #     f"time={data.time:.2f}, "
        #     f"joint1={data.qpos[0]:.3f}, "
        #     f"joint2={data.qpos[1]:.3f}, "
        #     f"ee={end_effector_pos}, "
        #     f"target={target_pos}, "
        #     f"error={cartesian_error:.4f}"
        #     f"qvel1={data.qvel[0]:.3f}, "
        #     f"qvel2={data.qvel[1]:.3f}, "
        #     f"target1={data.ctrl[0]:.3f}, "
        #     f"target2={data.ctrl[1]:.3f}"
        # )

        # 开始画轨迹
        viewer.user_scn.ngeom = 0

        # enumerate(trail)返回一个迭代器，返回值是一个元组，元组的第一个元素是索引，第二个元素是trail中的元素
        for i, point in enumerate(trail):
            # user_scn 能存的 visualization geometry 数量不是无限的
            if i >= viewer.user_scn.maxgeom:
                break

            # 真正在points里创建绿色小球
            mujoco.mjv_initGeom(
                viewer.user_scn.geoms[i],
                type=mujoco.mjtGeom.mjGEOM_SPHERE,
                size=[0.015, 0, 0],
                pos=point,
                mat=np.eye(3).flatten(),
                rgba=[0.2, 1.0, 0.3, 0.8],
            )

        # 告诉 Viewer 到底画几个
        viewer.user_scn.ngeom = min(
            len(trail),
            viewer.user_scn.maxgeom,
        )

        # 更新viewer
        viewer.sync()

        target_wall_step = model.opt.timestep / playback_speed

        time_until_next_step = (
            target_wall_step - (time.perf_counter() - step_start)
        )

        if time_until_next_step > 0:
            time.sleep(time_until_next_step)