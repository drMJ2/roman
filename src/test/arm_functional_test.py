import sys
import numpy as np
import math 
import time
import random
import os
import time
rootdir = os.path.dirname(os.path.dirname(__file__))
os.sys.path.insert(0, rootdir)
from roman import ur
from roman.sim.ur_rq3 import SimEnv 

#############################################################
# Arm unit tests that bypass the manipulator server.
# These tests can run on either sim or real arm.
#############################################################
def read_test(con):
    print(f"Running {__file__}::{read_test.__name__}()")
    con.connect()
    arm_ctrl = ur.BasicController(con)
    cmd = ur.Command()
    state = ur.State()
    arm_ctrl.execute(cmd, state)
    print("Tool pose:" + str(state.tool_pose()))
    print("Joint positions:" + str(state.joint_positions()))
    con.disconnect()
    print("Passed.")   
    
def move_test(con):
    print(f"Running {__file__}::{move_test.__name__}()")
    con.connect()
    arm_ctrl = ur.BasicController(con)

    arm = ur.Arm(arm_ctrl)
    arm.move(target_position=ur.Joints(0, -math.pi/2, math.pi/2, -math.pi/2, -math.pi/2, 0), max_speed=0.5, max_acc=0.5)
    assert arm.state.is_goal_reached()
    arm.move(target_position=ur.Tool(-0.4, -0.4, 0.2, 0, math.pi, 0), max_speed=1, max_acc=1)
    assert arm.state.is_goal_reached()
    arm.move(target_position=ur.Joints(0, -math.pi/2, math.pi/2, -math.pi/2, -math.pi/2, 0), max_speed=0.5, max_acc=0.5)
    assert arm.state.is_goal_reached()

    print("Tool pose:" + str(arm.state.tool_pose()))
    print("Joint positions:" + str(arm.state.joint_positions()))
    con.disconnect()
    print("Passed.")    

def move_linear_test(con):
    print(f"Running {__file__}::{move_test.__name__}()")
    con.connect()
    arm_ctrl = ur.LinearTCPMotionController(ur.BasicController(con))

    arm = ur.Arm(arm_ctrl)
    arm.move(target_position=ur.Joints(0, -math.pi/2, math.pi/2, -math.pi/2, -math.pi/2, 0))
    assert arm.state.is_goal_reached()

    home = arm.state.tool_pose() + 0
    arm.move(target_position=home)
    assert arm.state.is_goal_reached()

    next = home + [0.1, 0.1, 0, 0, 0, 0]
    arm.move(target_position=next, max_speed=1, max_acc=1)
    assert arm.state.is_goal_reached()

    down = next + [0, 0, -0.2, 0, 0, 0]
    arm.move(target_position=down, max_speed=1, max_acc=1)
    assert arm.state.is_goal_reached()
    
    arm.move(target_position=next, max_speed=1, max_acc=1)
    assert arm.state.is_goal_reached()

    arm.move(target_position=down, max_speed=1, max_acc=1)
    assert arm.state.is_goal_reached()

    arm.move(target_position=home, max_speed=1, max_acc=1)
    assert arm.state.is_goal_reached()

    print("Tool pose:" + str(arm.state.tool_pose()))
    print("Joint positions:" + str(arm.state.joint_positions()))
    con.disconnect()
    print("Passed.")  

#############################################################
# Runner
#############################################################
def run(use_sim):
    if not use_sim:
        #read_test(ur.Connection())
        #move_test(ur.Connection())
        move_linear_test(ur.Connection())
    else:
        env = SimEnv()
        env.reset()
        # read_test(ur.SimConnection(env))
        #move_test(ur.SimConnection(env))
        move_linear_test(ur.SimConnection(env))
        env.disconnect()

if __name__ == '__main__':
    run(True)