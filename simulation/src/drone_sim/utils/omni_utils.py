#!/usr/bin/env python3
import omni.graph.core as og
def setup_ros2_clock_graph():
        """
        Method that creates an OmniGraph that publishes the simulation time to the
        ROS2 /clock topic on every physics step.
        """

        graph_settings = {
            "graph_path": "/World/ROS2ClockGraph",
            "evaluator_name": "execution",
            "pipeline_stage": og.GraphPipelineStage.GRAPH_PIPELINE_STAGE_ONDEMAND,
        }

        keys = og.Controller.Keys
        og.Controller.edit(
            graph_settings,
            {
                keys.CREATE_NODES: [
                    ("OnPhysicsStep", "isaacsim.core.nodes.OnPhysicsStep"),
                    ("ReadSimTime", "isaacsim.core.nodes.IsaacReadSimulationTime"),
                    ("PublishClock", "isaacsim.ros2.bridge.ROS2PublishClock"),
                ],
                keys.CONNECT: [
                    ("OnPhysicsStep.outputs:step", "PublishClock.inputs:execIn"),
                    ("ReadSimTime.outputs:simulationTime", "PublishClock.inputs:timeStamp"),
                ],
            },
        )
