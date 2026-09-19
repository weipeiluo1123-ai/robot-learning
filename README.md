# robot-learning
Goal: Build a minimal robot learning pipeline from simulation to imitation learning and reinforcement learning.

## Project Structure

```text
robot-learning/
├── README.md
├── .gitignore
├── mujoco/
│   ├── 01_falling_ball/
│   │   ├── ball.xml
│   │   └── main.py
│   ├── 02_pendulum/
│   │   ├── pendulum.xml
│   │   └── main.py
│   └── 03_robot_arm/
├── imitation_learning/
├── reinforcement_learning/
├── assets/
├── docs/
└── outputs/
```

## Robot Learning 是什么？

```text
                    Robot Learning
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     PyTorch          MuJoCo            ROS2
        │                │                │
   神经网络/训练        物理仿真         机器人软件通信
        │
        ▼
  MPS / CUDA
        │
   计算加速后端
```

## Learning Questions

- observation 和 state 有什么区别？
- action 是什么？
- policy 是什么？
- demonstration 是什么？
- Behavior Cloning 在优化什么？
- 为什么 BC 会出现 distribution shift？
- reward 是什么？
- PPO 和 BC 最大的区别是什么？
- simulation 为什么重要？
- Sim2Real 是什么？
- 如果把这个程序放到真实机械臂上，还缺什么？
