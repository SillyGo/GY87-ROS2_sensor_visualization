import rclpy
from rclpy.node import Node
import serial
import time

from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField

PORT_NAME = "/dev/ttyUSB0"
BAUD_RATE = 115200

ser = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1) 
time.sleep(2)

class ImuPublisher(Node):
    def __init__(self):
        super().__init__('imu_sensor_publisher')
        self.imupub = self.create_publisher(Imu,'/imu_data_raw',10)
        self.magpub = self.create_publisher(MagneticField,'/mag_data_raw',10)
        self.timer = self.create_timer(0.1, self.TimerCallback)

    def TimerCallback(self):
        self.get_logger().info("PUBLICANDO DADO DA IMU")

        #1.extrai ax,ay,az, gx,gy,gz, mx,my,mz da IMU com pyserial e arduino
        
        accdata = ser.readline()
        accdata = accdata.decode('utf-8').strip()

        gyrodata = ser.readline()
        gyrodata = gyrodata.decode('utf-8').strip()

        magdata = ser.readline()
        magdata = magdata.decode('utf-8').strip()

        acc = accdata.split(" ")
        gyr = gyrodata.split(" ")
        mag = magdata.split(" ")

        ax, ay, az = float(acc[0]), float(acc[1]), float(acc[2])
        gx, gy, gz = float(gyr[0]), float(gyr[1]), float(gyr[2])
        mx, my, mz = float(mag[0]), float(mag[1]), float(mag[2])

        #2.constroi a mensagem da IMU
        msg = Imu()
    
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"

        msg.linear_acceleration.x = ax
        msg.linear_acceleration.y = ay
        msg.linear_acceleration.z = az

        msg.angular_velocity.x = gx
        msg.angular_velocity.y = gy
        msg.angular_velocity.z = gz

        msg.orientation_covariance[0] = -1
        
        #3.publica a mensagem da IMU

        self.imupub.publish(msg)
        
        #4. constroi a mensagem do mag

        msg = MagneticField()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "imu_link"
        
        msg.magnetic_field.x = mx
        msg.magnetic_field.y = my
        msg.magnetic_field.z = mz

        #5. publica a mensagem do mag

        self.magpub.publish(msg)

def main():
    rclpy.init()
    imupub = ImuPublisher()
    rclpy.spin(imupub)
    imupub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
