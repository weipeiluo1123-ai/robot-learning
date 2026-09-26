from pathlib import Path

import mujoco
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

alphas = np.linspace(
    0.0,
    1.0,
    6,
)

prev_q = np.array([0.0, 0.0])
joint_trajectory = []

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

    print()
    print("alpha =", alpha)
    print("target =", target_pos)
    print("joint angles =", best_q)
    print("delta q =", best_q - prev_q)
    print("error =", error)

    prev_q = best_q

print("\nJoint trajectory:")

for i, q in enumerate(joint_trajectory):
    print(i, q)