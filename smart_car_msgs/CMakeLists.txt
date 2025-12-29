cmake_minimum_required(VERSION 3.5)
project(smart_car_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/BBox2D.msg"


  "msg/BBox2DArray.msg"
   DEPENDENCIES std_msgs


  DEPENDENCIES builtin_interfaces
)

ament_package()
