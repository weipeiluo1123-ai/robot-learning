# robot-learning-sprint
Goal: Build a minimal robot learning pipeline from simulation to imitation learning and reinforcement learning.

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

注：当前学习的第一版认知地图

一些留下来的问题：
Robot Learning 是什么？
observation 和 state 有什么区别？
action 是什么？
policy 是什么？
demonstration 是什么？
Behavior Cloning 在优化什么？
为什么 BC 会 distribution shift？
reward 是什么？
PPO 和 BC 最大的区别是什么？
simulation 为什么重要？
Sim2Real 是什么？
如果把这个程序放到真实机械臂上，还缺什么？
