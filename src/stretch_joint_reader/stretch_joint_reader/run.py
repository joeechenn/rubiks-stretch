import hello_helpers.hello_misc as hm
from std_srvs.srv import Trigger

class MyNode(hm.HelloNode):
    def __init__(self):
        hm.HelloNode.__init__(self)

    def main(self):
        hm.HelloNode.main(self, 'my_node', 'my_node', wait_for_first_pointcloud=False)



        self.switch_to_position_mode_service.call_async(Trigger.Request())


        # my_node's main logic goes here
        self.move_to_pose({'joint_lift': 1}, blocking=True)
        self.move_to_pose({'joint_wrist_yaw': 1.0, 'joint_wrist_pitch': 1.0, 'joint_wrist_roll': 1.0,}, blocking=True)

def main():
    node = MyNode()
    node.main()