import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import time # 加在最上面

class UARTNode(Node):
    def __init__(self):
        self.last_process_time = 0
        self.last_f_received = False
        super().__init__('uart_node')
        self.ser = None
        self.last_cmd = ''
        self.pending_send = False
        
        
        try:
            self.ser = serial.Serial('/dev/ttyUSB_arduino', 9600, timeout=1)
            self.get_logger().info("connected to Arduino")
        except serial.SerialException:
            self.get_logger().error("can not connect to Arduino，please check serial port")

            return
                
        self.subscription = self.create_subscription(
            Int32,
            '/person_zone',
            self.zone_callback,
            10
        )
        
        
        self.create_timer(0.1, self.serial_check)
        self.last_process_time = 0  # 加這行：紀錄上一次處理的時間



    def zone_callback(self, msg):
        
        now = time.time()
        if now - self.last_process_time < 5.0:
            return  # ❌ 不到 5 秒就不處理
        self.last_process_time = now  # ✅ 更新處理時間
        
        zone = msg.data
        self.get_logger().info(f"[DEBUG] zone raw value: {zone} (type: {type(zone)})")
        
        new_cmd = ''
        if zone == 0:
            new_cmd = 'L'
        elif zone == 1:
            new_cmd = 'C'
        elif zone == 2:
            new_cmd = 'R'
        
        
        
        if new_cmd:
            self.last_cmd = new_cmd
            self.pending_send = True
            self.get_logger().info(f"[zone_callback] zone: {zone}, set cmd to: {self.last_cmd}")
            
            if self.last_f_received:
               self.ser.write(self.last_cmd.encode())
               self.get_logger().info(f"[UART] (early) sent to Arduino: {self.last_cmd}")
               self.pending_send = False
               self.last_f_received = False
            
    def serial_check(self):
    
        if self.ser is None:
            return
            
        if self.ser.in_waiting > 0:
          line = self.ser.readline().decode(errors='ignore').strip()
          self.get_logger().info(f"[UART] Arduino says: {line}")

          if line == 'F':
            self.last_f_received = True
            if self.last_cmd and self.pending_send:
                self.ser.write(self.last_cmd.encode())
                self.get_logger().info(f"[UART] sent to Arduino: {self.last_cmd}")
                self.pending_send = False
                                
def main(args=None):
    rclpy.init(args=args)
    node = UARTNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
