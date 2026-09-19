from pathlib import Path
import time

import mujoco
import mujoco.viewer

import numpy as np

xml_path = Path(__file__).with_name("arm.xml")

model = mujoco.MjModel.from_xml_path(str(xml_path))
data = mujoco.MjData(model)


print("nq =", model.nq)
print("nv =", model.nv)
print("nu =", model.nu)

# data.qpos[0] = 0.0
# data.qpos[1] = -0.8

data.ctrl[0] = 0.6
data.ctrl[1] = -0.8
# data.ctrl[:] = [0.6, -0.8]

mujoco.mj_forward(model, data)

playback_speed = 0.03

trail = []

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.perf_counter()

        if data.time < 0.5:
            data.ctrl[:] = [0.6, -0.8]
        else:
            data.ctrl[:] = [-0.6, 2.5]

        mujoco.mj_step(model, data)

        end_effector_pos = data.site("end_effector").xpos.copy()
        trail.append(end_effector_pos)

        if len(trail) > 200:
            trail.pop(0)

        print(
            f"time={data.time:.2f}, "
            f"joint1={data.qpos[0]:.3f}, "
            f"joint2={data.qpos[1]:.3f}, "
            f"ee={end_effector_pos}, "
            f"target1={data.ctrl[0]:.3f}, "
            f"target2={data.ctrl[1]:.3f}"
        )

        viewer.user_scn.ngeom = 0

        for i, point in enumerate(trail):
            if i >= viewer.user_scn.maxgeom:
                break

            mujoco.mjv_initGeom(
                viewer.user_scn.geoms[i],
                type=mujoco.mjtGeom.mjGEOM_SPHERE,
                size=[0.015, 0, 0],
                pos=point,
                mat=np.eye(3).flatten(),
                rgba=[0.2, 1.0, 0.3, 0.8],
            )

        viewer.user_scn.ngeom = min(
            len(trail),
            viewer.user_scn.maxgeom,
        )

        viewer.sync()

        target_wall_step = model.opt.timestep / playback_speed

        time_until_next_step = (
            target_wall_step - (time.perf_counter() - step_start)
        )

        if time_until_next_step > 0:
            time.sleep(time_until_next_step)