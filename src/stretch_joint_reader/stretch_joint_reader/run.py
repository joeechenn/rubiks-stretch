import hello_helpers.hello_misc as hm
import rclpy
from std_srvs.srv import Trigger

class MyNode(hm.HelloNode):
    def __init__(self):
        hm.HelloNode.__init__(self)

    def main(self):
        hm.HelloNode.main(self, 'my_node', 'my_node', wait_for_first_pointcloud=False)

        self.switch_to_position_mode_service.call_async(Trigger.Request())

        # my_node's main logic goes here
    
        self.move_to_pose({'joint_lift': .92}, blocking=True)
        self.move_to_pose({'wrist_extension': 0.25}, blocking=True)

        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': -1.5, 'joint_wrist_roll': 0,}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': .5}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': 0}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': -1.5, 'joint_wrist_roll': 1.5,}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': 0, 'joint_wrist_roll': 1.5,}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': 0, 'joint_wrist_roll': 0,}, blocking=True)
        self.move_to_pose({'joint_lift': .695}, blocking=True)
        self.move_to_pose({'wrist_extension': 0.0}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': 0.5}, blocking=True)
        self.move_to_pose({'joint_lift': .92}, blocking=True)
        self.move_to_pose({'wrist_extension': 0.30}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': -1.5, 'joint_wrist_roll': 0,}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': .5}, blocking=True)
        self.move_to_pose({'joint_gripper_finger_left': 0}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': -1.5, 'joint_wrist_roll': 1.5,}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 0, 'joint_wrist_pitch': 0, 'joint_wrist_roll': 1.5,}, blocking=True)


        


def main():
    node = MyNode()
    node.main()
    rclpy.shutdown()
    node.new_thread.join()

    
if __name__ == '__main__':
    main()