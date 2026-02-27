import rclpy
from rclpy.node import Node
import serial
import time

from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField

PORT_NAME = "/dev/ttyUSB0"
BAUD_RATE = 115200

ser = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1) 
time.sleep(1) #deixa o serial ir printando para não ter problema possível de ler linha vazia

class ImuPublisher(Node):
    def __init__(self):
        super().__init__('imu_sensor_publisher')
        self.imupub = self.create_publisher(Imu,'/imu_data_raw',10)
        self.magpub = self.create_publisher(MagneticField,'/mag_data_raw',10)
        self.timer = self.create_timer(0.01, self.TimerCallback)

    def TimerCallback(self):
        self.get_logger().info("PUBLICANDO DADO DA IMU")
        PUB = True

        #1.extrai ax,ay,az, gx,gy,gz, mx,my,mz da IMU com pyserial e arduino
        
        try:
            data = ser.readline()
            data = data.decode('utf-8').strip()

            data = data.split(" ")

            ax, ay, az = float(data[0]), float(data[1]), float(data[2])
            gx, gy, gz = float(data[3]), float(data[4]), float(data[5])
            mx, my, mz = float(data[6]), float(data[7]), float(data[8])

            print(f"a: {ax,ay,az}")
            print(f"g: {gx,gy,gz}")
            print(f"m: {mx,my,mz}")
            
        except:
            print("não recebi dados")
            PUB = False

        if PUB:
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
