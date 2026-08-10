#!/usr/bin/env python
from drone_sim.scenarios import Scenario

import carb
import omni.timeline

from isaacsim.core.utils.extensions import enable_extension
enable_extension("isaacsim.ros2.bridge")

# Import the Pegasus API for simulating drones
from pegasus.simulator.params import ROBOTS, SIMULATION_ENVIRONMENTS
from pegasus.simulator.logic.backends.px4_mavlink_backend import PX4MavlinkBackend, PX4MavlinkBackendConfig
from pegasus.simulator.logic.backends.ros2_backend import ROS2Backend
from pegasus.simulator.logic.vehicles.multirotor import Multirotor, MultirotorConfig
from pegasus.simulator.logic.interface.pegasus_interface import PegasusInterface
from pegasus.simulator.logic.graphical_sensors.monocular_camera import MonocularCamera

from rclpy.parameter import Parameter
from scipy.spatial.transform import Rotation
import numpy as np

from drone_sim.utils.omni_utils import setup_ros2_clock_graph
from drone_sim.utils.ros2_utils import publish_static_tf

class EmptySceneWithWalls(Scenario):
    def __init__(self):
        """
        Method that initializes the PegasusApp and is used to setup the simulation environment.
        """

        # Acquire the timeline that will be used to start/stop the simulation
        self.timeline = omni.timeline.get_timeline_interface()

        # Start the Pegasus Interface
        self.pg = PegasusInterface()

        # Acquire the World, .i.e, the singleton that controls that is a one stop shop for setting up physics,
        # spawning asset primitives, etc.
        self.pg.initialize_world()

        # Launch one of the worlds provided by NVIDIA
        self.pg.load_environment(SIMULATION_ENVIRONMENTS["Box Room"])

        # Create the vehicle
        # Try to spawn the selected robot in the world to the specified namespace
        config_multirotor = MultirotorConfig()

        # Create the Mavlink configuration for the multirotor
        mavlink_config = PX4MavlinkBackendConfig({
            "vehicle_id": 0,
            "px4_autolaunch": True,
            "px4_dir": self.pg.px4_path,
            "px4_vehicle_model": self.pg.px4_default_airframe # CHANGE this line to 'iris' if using PX4 version bellow v1.14
        })
        mavlink_backend = PX4MavlinkBackend(mavlink_config)

        setup_ros2_clock_graph()
        ros2_bridge_config = {
                    "namespace": 'drone',
                    "pub_sensors": False,
                    "pub_graphical_sensors": True,
                    "pub_state": True,
                    "pub_tf": True,
                    "sub_control": False
                }
        ros2_bridge_backend = ROS2Backend(vehicle_id=1, config=ros2_bridge_config)
        ros2_bridge_backend.node.set_parameters([Parameter("use_sim_time", Parameter.Type.BOOL, True)])


        config_multirotor.graphical_sensors = [MonocularCamera("camera", config={
                                                                "frequency": 60.0,
                                                                "position": np.array([0.14985, 0.0, -0.02963]),      # FLU, relative to body origin
                                                            })]

        config_multirotor.backends = [mavlink_backend, ros2_bridge_backend]

        Multirotor(
            "/World/quadrotor",
            ROBOTS['Pegasus'],
            0,
            [0.0, 0.0, 0.07],
            Rotation.from_euler("XYZ", [0.0, 0.0, 0.0], degrees=True).as_quat(),
            config=config_multirotor,
        )

        # TODO: This is a very manual way of publishing the static transform between the drone base_link and the camera. I should implement a more generic way of doing this in the ROS2 backend.
        publish_static_tf(ros2_bridge_backend.node, ros2_bridge_backend.tf_static_broadcaster, "drone_base_link", "camera_01", np.array([0.14985, 0.0, -0.02963]), np.array([0.0, 0.0, 180.0]))

    def run(self, simulation_app):
        """
        Method that implements the application main loop, where the physics steps are executed.
        """

        # Start the simulation
        self.timeline.play()

        # The "infinite" loop
        while simulation_app.is_running():

            # Update the UI of the app and perform the physics step
            simulation_app.update()

        # Cleanup and stop
        carb.log_warn("EmptySceneWithWalls scenario is closing.")
        self.timeline.stop()
