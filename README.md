# Drone Navstack
Drone Navstack is my first initiative to build a project in public, with the ultimate goal of developing an autonomous drone.

Prior to deploying on physical hardware, the strategy is to establish a simulation environment for rigorous testing. The architecture will utilize PX4 to handle low-level flight control and a custom ROS 2 stack to manage high-level autonomous commands.

This project allows me to leverage my experience in mobile ground robotics and adapt it to aerial autonomy. The initial phases focus on mapping out the core requirements needed to develop to a fully or semi-autonomous 3D flight stack. An early milestone includes integrating camera perception to enable vision-based flight control, such as commanding the drone to trace shapes based on detected hand gestures.

The final objective is to deliver a realistic simulation environment with robustly tested code, including building a custom communication bridge between PX4 and ROS 2. By mirroring these real-world integration steps in simulation, the eventual transition to physical hardware will be significantly streamlined.
