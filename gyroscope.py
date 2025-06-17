import busio
import board
import adafruit_mpu6050 as mpu6050
from utils import dot, normalize


class Gyroscope:
    def __init__(self):
        i2c = busio.I2C(sda=board.GP14, scl=board.GP15)
        self.mpu = mpu6050.MPU6050(i2c)

    def get_velocity(self) -> tuple[int, int]:
        accel = normalize(self.mpu.acceleration)
        vectors = {
            (0, 1, 0): (0, 1),
            (0, -1, 0): (0, -1),
            (1, 0, 0): (1, 0),
            (-1, 0, 0): (-1, 0)
        }
        max_dot = float("-inf")
        max_vector = (0, 1, 0)
        for vector in vectors.keys():
            new_dot = dot(accel, vector)
            if new_dot > max_dot:
                max_dot = new_dot
                max_vector = vector
        return vectors[max_vector]
