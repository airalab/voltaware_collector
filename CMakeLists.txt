cmake_minimum_required(VERSION 2.8.3)
project(voltaware_collector)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package()

catkin_install_python(
    PROGRAMS
        scripts/collector_node
    DESTINATION
        ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#install(
#    FILES
#    DESTINATION
#        ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
#)
