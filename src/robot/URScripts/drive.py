import pybullet as pb
from robot.URScripts.constants import *
from robot.URScripts.urlib import *
from robot.URScripts.control import *

def ur_drive(time, id, kind, target_speed, max_acceleration, force_low_bound, force_high_bound, contact_handling, target_position, max_speed):
    target_speed = ur_get_target_speed(time, 
                                        id, 
                                        kind, 
                                        target_speed, 
                                        max_acceleration, 
                                        force_low_bound, 
                                        force_high_bound, 
                                        contact_handling, 
                                        target_position, 
                                        max_speed)
    speedj(target_speed, max_acceleration)
    


