from scipy.spatial.transform import Rotation
from geometry_msgs.msg import TransformStamped


def publish_static_tf(node, tf_static_broadcaster, parent_frame, child_frame, translation, rotation):
    """
    Publishes a static transform between two frames in ROS2.

    Args:
        node: The ROS2 node used to create the broadcaster and read the clock.
        parent_frame: The name of the parent frame.
        child_frame: The name of the child frame.
        translation: A list or tuple of three floats representing the translation (x, y, z).
        rotation: A list or tuple of three floats representing the rotation as
            Euler angles (roll, pitch, yaw) in degrees.
    """

    quaternion = Rotation.from_euler("XYZ", rotation, degrees=True).as_quat()

    static_transform_stamped = TransformStamped()
    static_transform_stamped.header.stamp = node.get_clock().now().to_msg()
    static_transform_stamped.header.frame_id = parent_frame
    static_transform_stamped.child_frame_id = child_frame
    static_transform_stamped.transform.translation.x = float(translation[0])
    static_transform_stamped.transform.translation.y = float(translation[1])
    static_transform_stamped.transform.translation.z = float(translation[2])
    static_transform_stamped.transform.rotation.x = float(quaternion[0])
    static_transform_stamped.transform.rotation.y = float(quaternion[1])
    static_transform_stamped.transform.rotation.z = float(quaternion[2])
    static_transform_stamped.transform.rotation.w = float(quaternion[3])

    tf_static_broadcaster.sendTransform(static_transform_stamped)
