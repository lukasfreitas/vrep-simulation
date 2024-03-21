from object_builder.object_handler import BoxHandler, CylinderHandler
from object_builder.joint_handler import JointHandler
from rich import inspect


class CarHandler:
    objects = []
    motors = []

    def __init__(self, sim):

        self.sim = sim

    def create_chassis(self, x_dimension, y_dimension, z_dimension, pos=(0, 0, 0)):
        self.chassi = BoxHandler(self.sim, name_alias="chassi")
        self.chassi.create_object(x_dimension, y_dimension, z_dimension, pos)
        self.chassi.position = (0, 0, 1)

    def create_motor(self, pos=(0, 0, 0), alias=""):
        joint_obj = JointHandler(self.sim, alias)
        joint_obj.load_joint_object("revolute", 0.2, 0.1)
        joint_obj.bound_joint_parent(self.chassi)

        joint_obj.position = pos
        joint_obj.rotacionar_objeto(angulo_y=90)

        return joint_obj

    def create_wheel(self, motor, alias="", pos=(0, 0, 0.05)):
        wheel = CylinderHandler(self.sim, name_alias=alias)
        wheel.create_object(0.15, 0.05)
        wheel.bound_object_parent(motor)
        wheel.position = pos

    def build(self, **kargs):
        self.create_chassis(
            kargs.pop("x_dimension"),
            kargs.pop("y_dimension"),
            kargs.pop("z_dimension"),
            kargs.pop("pos"),
        )

        left_wheels_pos = (0, 0, 0.05)
        right_wheels_pos = (0, 0, -0.1)

        LFM_pos = (self.chassi.x_dimension, self.chassi.y_dimension / 4, self.chassi.z_dimension / 2)
        LBM_pos = (self.chassi.x_dimension, self.chassi.y_dimension * (3 / 4), self.chassi.z_dimension / 2)
        RFM_pos = (0, self.chassi.y_dimension / 4, self.chassi.z_dimension / 2)
        RBM_pos = (0, self.chassi.y_dimension * (3 / 4), self.chassi.z_dimension / 2)

        motor_and_wheels_data = [
            ("LF", LFM_pos, left_wheels_pos),
            ("LB", LBM_pos, left_wheels_pos),
            ("RF", RFM_pos, right_wheels_pos),
            ("RB", RBM_pos, right_wheels_pos),
        ]

        for motor_name, motor_poisiton, wheel_pos in motor_and_wheels_data:
            motor = self.create_motor(motor_poisiton, motor_name + "_motor")
            self.motors.append(motor)
            self.create_wheel(motor, motor_name + "_wheel", wheel_pos)

        print(self.sim.getObjectFloatParam(self.chassi.id, self.sim.shapefloatparam_mass))
