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
        vectors = [
            (0, 1, 0),
            (0, -1, 0),
            (1, 0, 0),
            (-1, 0, 0),
        ]
        dots = [dot(accel, vector[:2]) for vector in vectors]
        max_vector = max(range(len(dots)), key=lambda i: dots[i])
        return vectors[max_vector][:2]
