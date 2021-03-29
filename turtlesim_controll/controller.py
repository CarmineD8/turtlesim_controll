# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import Kill
from turtlesim.srv import Spawn


class MyController(Node):

    def __init__(self):
        super().__init__('my_controller')
        self.cli1 = self.create_client(Kill, '/kill')
        while not self.cli1.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req1= Kill.Request()
        
        self.cli2 = self.create_client(Spawn, '/spawn')
        while not self.cli2.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req2= Spawn.Request()
        
        self.publisher_ = self.create_publisher(Twist, '/myturtle/cmd_vel', 1)
        self.subscription = self.create_subscription(
            Pose,
            '/myturtle/pose',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
    def send_request(self):
        self.req1.name = "turtle1"
        self.future = self.cli1.call_async(self.req1)
        
    def send_request2(self):
        self.req2.name = "myturtle"
        self.req2.x=2.0
        self.req2.y=1.0
        self.req2.theta=0.0
        self.future = self.cli2.call_async(self.req2)
        

    def listener_callback(self, msg):
        #self.get_logger().info('Pos x:'+ str(msg.x) + ' Pos y: '+ str(msg.y))
        msg_p = Twist()
        if(msg.x>9.0):
            msg_p.linear.x=1.0
            msg_p.angular.z=1.0
        elif(msg.x<1.5):
            msg_p.linear.x=1.0
            msg_p.angular.z=-1.0
        else:
            msg_p.linear.x=1.0
            msg_p.angular.z=0.0
        self.publisher_.publish(msg_p)


def main(args=None):
    rclpy.init(args=args)

    my_controller = MyController()
    my_controller.send_request()
    my_controller.send_request2()
    rclpy.spin(my_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
