import machine
import time
import MPU6050

# Set up the I2C interface
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))

# Set up the MPU6050 class 
mpu = MPU6050.MPU6050(i2c)

# wake up the MPU6050 from sleep
mpu.wake()

# continuously print the data
while True:
    gyro = mpu.read_gyro_data()
    accel = mpu.read_accel_data()
    print("Gyro: " + str(gyro) + ", Accel: " + str(accel))
    time.sleep(0.5)