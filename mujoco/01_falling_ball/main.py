from pathlib import Path
import time

import mujoco
import mujoco.viewer

# 保持目录不变，把文件名 main.py 换成 ball.xml
xml_path = Path(__file__).with_name("ball.xml")

model = mujoco.MjModel.from_xml_path(str(xml_path))
data = mujoco.MjData(model)

# with字段内，viewer指的就是mujoco.viewer.launch_passive(model, data)
with mujoco.viewer.launch_passive(model, data) as viewer:
    while viewer.is_running():
        step_start = time.time()

        # 改变物理世界
        mujoco.mj_step(model, data)
        
        print(data.time, data.qpos[:3])

        # 同步更新
        viewer.sync()

        time_until_next_step = (
            model.opt.timestep - (time.time() - step_start)
        )

        if time_until_next_step > 0:
            time.sleep(time_until_next_step)

