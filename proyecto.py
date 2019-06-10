#!/usr/bin/env python3


from ev3dev.ev3 import *
from os import listdir, getcwd, mkdir, rename, path, mknod
import time
import sys

def execute():
    control = Arm_control()
    control.execute()

speed_f = lambda a, v0, t: v0 + a*t

derivate = lambda e0, e1, t0, t1 : (e1 - e0) / (t1 - t0)

class Arm_control:
    max_base_position = 180
    max_arm_height = 255
    min_arm_height = 20
    claw_state = 0
    obj_dist = 150
    ## Log and configuration files
    file_init = "configuration.init"
    base_log = "base_"
    current_base_log = "base_"
    base_counter = 0
    arm_log = "arm_"
    current_arm_log = "arm_"
    arm_counter = 0
    test_number = -1
    base_cap = 300
    duty_cycle_limit = 100

    us_log  = "us.log"
    ## Hardware initialization
    arm = LargeMotor("outA")
    base = LargeMotor("outC")
    claw = MediumMotor("outB")
    us = UltrasonicSensor('in3')
   

    def __init__ (self, file_state=None, file_init=None):
        if file_init:
            self.file_init = file_init
        if file_state:
            self.file_state = file_state
        self.__setup_comps()
        

    def __create_base_file(self):
        self.current_base_log = self.base_log + str(self.base_counter)
        self.base_counter += 1
        with open(self.current_base_log, 'w+') as file: pass
    
    def __record_base_movement(self, sensor, position, speed, direction):
        with open(self.current_base_log, 'a+') as center:
            center.write('{} {} {} {}\n'.format(sensor,
                                                position,
                                                speed,
                                                direction))
    def __create_speed_file(self, obj):
        self.current_arm_log = self.arm_log + str(self.arm_counter)
        self.arm_counter += 1
        with open(self.current_arm_log, 'w+') as file:
            file.write('{}\n'.format(obj))
    
    def __record_custom_pid(self, speed, position, error, integral, derivative):
        with open(self.current_arm_log, 'a+') as file:
            file.write('{} {} {} {} {}\n'.format(speed, position, error, integral, derivative))
    

    def __setup_comps(self):
        with open(self.file_init, 'r')  as data:
            config = data.read().split()
            self.arm.position = int(config[0])
            self.base.position = int(config[1])
            self.claw_state = int(config[2])


    def save_data(self):
        with open(self.file_init, 'w') as data:
            data.write('{} {} {}'.format(self.arm.position, 
                                         self.base.position,
                                         self.claw_state))
            
    def change_claw(self):
        if self.claw_state:
            self.claw_state = 0
            self.claw.run_to_rel_pos(position_sp=150,speed_sp=65)
            time.sleep(1)
            self.claw.stop()
        else:
            self.claw_state = 1
            self.claw.run_to_rel_pos(position_sp=-50,speed_sp=40)
            time.sleep(1)
            self.claw.stop()

    def open_claw(self):
        if not self.claw_state:        
            self.change_claw()


    def move_base(self, direction = 1, step=10, speed = 40):
        self.base.run_to_rel_pos(position_sp=step*direction, speed_sp=speed)
    

    def __record_block_success(self):
        with open('a.log', 'a+') as center:
            center.write(('1' if self.us.value() > self.obj_dist else '0') + '\n') 

    def block_catch(self):
        return False if self.us.value() < self.obj_dist else True

    def execute(self):
        self.open_claw()
        self.arm_up()
        self.search_for_object()
        while True:
            self.arm_down()
            self.change_claw()
            self.arm_up()
            if self.block_catch():
                break
            self.change_claw()
        self.__record_block_success()
        self.save_data()
        self.search_for_object()
        self.arm_down()
        self.change_claw()

    def to_init_state(self):
        self.arm_up()
        self.move_base(direction=-1, step=30)
        self.arm_down()


    def search_for_object(self):
        self.base.stop_action = 'brake'
        _x0 = None
        _x1 = None
        direction = -1
        _center = 0
        speed = 40
        changed = False
        self.__create_base_file()
        while True:
            self.move_base(direction=direction, speed=speed)
            actual = self.base.position
            self.__record_base_movement(self.us.value(),
                                        actual,
                                        self.base.speed,
                                        direction)
            if (abs(actual) > self.base_cap) and not changed:
                _x0 = None
                _x1 = None
                self.base.stop()
                direction = (-1) * direction
                changed = True
            
            elif changed and (abs(actual) < self.base_cap):
                changed = False

            elif _x0 and self.us.value() > self.obj_dist:
                self.base.stop()
                _x1 = actual
                _center = int(abs(_x1 - _x0) * 0.5 + 20)
                self.move_base(direction=(-1)*direction, step=_center)
                while self.base.is_running:
                    pass
                return        
            elif not _x0 and self.us.value() < self.obj_dist:
                _x0 = actual


    def arm_up(self):
        self.move_arm_pid(-self.max_arm_height, direction=-1)
        self.arm.stop()

    def arm_down(self):
        self.move_arm_pid(-self.min_arm_height, direction=1)
        self.arm.stop()

    def move_arm_pid(self, obj, direction = 1, speed=40):
        self.arm.stop_action = 'brake'
        kp = 3
        kd = 7
        self.arm.ramp_up_sp = 888
        self.arm.ramp_down_sp = 666
        old_error = obj - self.arm.position
        self.__create_speed_file(obj)
        while True:
            actual = self.arm.position
            error = obj - actual
            derivative = (error - old_error) / self.arm.ramp_up_sp
            speed = max(-70, min(70, error*kp + (derivative)*kd))
            self.arm.run_forever(speed_sp=speed)
            old_error = error
            self.__record_custom_pid(self.arm.speed,
                                     actual,
                                     error,
                                     speed,
                                     derivative)
            if abs(error) <= 4:
                break

        self.arm.stop()    
    

if __name__ == '__main__':
    execute()
    