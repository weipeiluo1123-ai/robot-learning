from pathlib import Path
import time

import mujoco
import mujoco.viewer

xml_path = Path(__file__).with_name("pendulum.xml")

model = mujoco.MjModel.from_xml_path(str(xml_path))
data = mujoco.MjData(model)

print("nq =", model.nq)
print("nv =", model.nv)
print("qpos =", data.qpos)
print("qvel =", data.qvel)

data.qpos[0] = 3
mujoco.mj_forward(model, data)

with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()

        mujoco.mj_step(model, data)
        
        print(
            f"time={data.time:.2f}, "
            f"qpos={data.qpos[0]:.2f}, "
            f"qvel={data.qvel[0]:.2f}"
        )

        viewer.sync()

        time_until_next_step = (
            model.opt.timestep - (time.time() - step_start)
        )

        if time_until_next_step > 0:
            time.sleep(time_until_next_step)