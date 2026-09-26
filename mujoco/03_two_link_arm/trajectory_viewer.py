from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np


xml_path = Path(__file__).with_name("arm.xml")

model = mujoco.MjModel.from_xml_path(
    str(xml_path)
)

def solve_ik(
    target_pos,
    prev_q=None,
    position_tolerance=0.01,
):
    ik_data = mujoco.MjData(model)

    best_error = float("inf")
    best_q = None
    best_pos = None

    candidates = []

    q1_values = np.linspace(-1.5, 1.5, 121)
    q2_values = np.linspace(-1.5, 1.5, 121)

    for q1 in q1_values:
        for q2 in q2_values:
            ik_data.qpos[:] = [q1, q2]

            mujoco.mj_forward(
                model,
                ik_data,
            )

            ee_pos = (
                ik_data
                .site("end_effector")
                .xpos
                .copy()
            )

            error = np.linalg.norm(
                ee_pos - target_pos
            )

            # 仍然记录纯 position error 最小的解
            if error < best_error:
                best_error = error
                best_q = np.array([q1, q2])
                best_pos = ee_pos.copy()

            # 所有“已经够准”的解都先留下来
            if error < position_tolerance:
                candidates.append(
                    (
                        np.array([q1, q2]),
                        ee_pos.copy(),
                        error,
                    )
                )

    # 如果有上一帧，就优先选择离上一帧最近的 IK 解
    if prev_q is not None and candidates:
        best_candidate = min(
            candidates,
            key=lambda item: np.linalg.norm(
                item[0] - prev_q
            ),
        )

        return best_candidate

    return best_q, best_pos, best_error

data = mujoco.MjData(model)

start_pos = np.array([
    0.0,
    0.0,
    0.3,
])

goal_pos = np.array([
    -0.8,
    0.0,
    0.7,
])

alphas = np.linspace(0.0, 1.0, 51)

# Joint Space Trajectory Generation
joint_trajectory = []

prev_q = np.array([0.0, 0.0])

for alpha in alphas:
    target_pos = (
        (1.0 - alpha) * start_pos
        + alpha * goal_pos
    )

    best_q, reached_pos, error = solve_ik(
        target_pos,
        prev_q,
    )

    joint_trajectory.append(
        best_q.copy()
    )

    prev_q = best_q


# joint_trajectory = [
#     np.array([0.0, 0.0]),
#     np.array([-0.2, 0.675]),
#     np.array([-0.125, 0.85]),
#     np.array([0.0, 0.925]),
#     np.array([0.175, 0.9]),
#     np.array([0.425, 0.725]),
# ]


trajectory_duration = 6.0


with mujoco.viewer.launch_passive(
    model,
    data,
) as viewer:

    while viewer.is_running():

        progress = min(
            data.time / trajectory_duration,
            1.0,
        )

        trajectory_pos = (
            progress
            * (len(joint_trajectory) - 1)
        )

        index0 = int(trajectory_pos)

        index1 = min(
            index0 + 1,
            len(joint_trajectory) - 1,
        )

        fraction = (
            trajectory_pos - index0
        )

        target_q = (
            (1.0 - fraction)
            * joint_trajectory[index0]
            + fraction
            * joint_trajectory[index1]
        )

        data.ctrl[:] = target_q

        mujoco.mj_step(
            model,
            data,
        )

        joint_error = np.linalg.norm(
            data.qpos - target_q
        )

        print(
            f"time={data.time:.2f}, "
            f"progress={progress:.2f}, "
            f"target={target_q}, "
            f"q={data.qpos.copy()}, "
            f"error={joint_error:.4f}"
        )

        viewer.sync()

        time.sleep(
            model.opt.timestep
        )