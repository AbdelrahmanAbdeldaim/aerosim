# Drone Navstack

Drone Navstack is my first initiative to build a project in public, with the ultimate goal of developing an autonomous physical drone.

Prior to deploying on physical hardware, the strategy is to establish a simulation environment for rigorous testing. The architecture will utilize PX4 to handle low-level flight control and a custom ROS 2 stack to manage high-level autonomous commands.

## 🗺️ Roadmap & Milestones

[![GitHub Project](https://img.shields.io/badge/GitHub-Project_Board-blue?logo=github&style=flat-square)](https://github.com/users/AbdelrahmanAbdeldaim/projects/1)

* **Phase 1: Simulation Setup**
* **Phase 2: Manual Control with Radio Controller**
* **Phase 3: High-Level Autonomy Stack**
* **Phase 4: Hardware Integration & Physical Flight**

## Simulation Setup

The simulation environment uses the following stack:

* **NVIDIA Isaac Sim 5.1** provides the USD scene, rendering, sensors, and
  physics simulation.
* **Pegasus Simulator** adds multirotor vehicle models and connects Isaac Sim
  to PX4.

See the [simulation setup guide](simulation/README.md) for installation,
environment configuration, and standalone script usage.
