# 🤖 Robot Control System

## Overview - نظرة عامة

Now: **robot-control repository** with complete testing and control system for Yahboom ROSMASTER R2 A1 with NVIDIA Jetson Orin Nano Super 8GB.

نظام تحكم وإختبار شامل لروبوت فحص أمني ذكي.

## 📋 Features - المميزات

✅ **Complete Motor Testing** - اختبار المحركات والتوجيه  
✅ **Sensor Validation** - التحقق من جميع الحساسات  
✅ **Camera Integration** - إدارة الكاميرا  
✅ **LiDAR System** - نظام الليدار  
✅ **YOLO Detection** - كشف الأشخاص والمخاطر  
✅ **Web Dashboard** - لوحة تحكم ويب حديثة  
✅ **Advanced Testing** - نظام اختبار متقدم  
✅ **Real-time Monitoring** - مراقبة مباشرة  

## 🚀 Quick Start

### Prerequisites
- Ubuntu 22.04 LTS
- ROS2 Humble
- Python 3.10+
- Jetson Orin Nano Super 8GB (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/isimobaver/robot-control.git
cd robot-control

# Run setup
chmod +x quick_start.sh
./quick_start.sh

# Or use Python setup
python3 setup_robot_system.py
```

### Running the System

#### Terminal 1 - Control Panel
```bash
source ~/robot_test_ws/install/setup.bash
ros2 run robot_test control_panel
```

#### Terminal 2 - Robot Launch
```bash
source ~/ai_robot_ws/install/setup.bash
ros2 launch ai_robot robot.launch.py
```

#### Terminal 3 - Web Dashboard (Optional)
```bash
python3 web_dashboard.py
# Open http://localhost:5000
```

## 📦 Components

### 1. Control Panel (`control_panel.py`)
- Interactive terminal interface
- Motor testing
- Sensor monitoring
- Camera control
- LiDAR testing
- YOLO detection

### 2. Motor Testing (`motor_test.py`)
- Forward/Backward motion
- Left/Right turns
- Circular motion
- Ackermann steering
- Emergency stop

### 3. Sensor Testing (`sensor_test.py`)
- IMU calibration
- Odometry validation
- LiDAR measurements
- Data synchronization

### 4. Camera Testing (`camera_test.py`)
- Camera access
- Video stream
- Properties monitoring
- Exposure adjustment

### 5. LiDAR Testing (`lidar_test.py`)
- Range accuracy
- Obstacle detection
- Performance monitoring

### 6. YOLO Testing (`yolo_test.py`)
- Model loading
- Object detection
- Webcam integration
- Real-time inference

### 7. Web Dashboard (`web_dashboard.py`)
- Real-time visualization
- Remote control
- Sensor monitoring
- Event logging

### 8. Advanced Tester (`advanced_tester.py`)
- Comprehensive testing
- Result reporting
- Performance analysis

## 🎮 Available Commands

### Direct Motor Testing
```bash
ros2 run robot_test motor_test
```

### Direct Sensor Testing
```bash
ros2 run robot_test sensor_test
```

### Direct Camera Testing
```bash
ros2 run robot_test camera_test
```

### Direct LiDAR Testing
```bash
ros2 run robot_test lidar_test
```

### Direct YOLO Testing
```bash
ros2 run robot_test yolo_test
```

### Web Dashboard
```bash
python3 web_dashboard.py
# Open http://localhost:5000
```

### Advanced System Test
```bash
python3 advanced_tester.py
```

## 📊 Testing Scenarios

### Motor Tests
1. Forward motion (3s)
2. Backward motion (3s)
3. Left turn (3s)
4. Right turn (3s)
5. Circular motion (5s)
6. Ackermann steering
7. Speed range test
8. Emergency stop

### Sensor Tests
1. IMU Accelerometer
2. IMU Gyroscope
3. Odometry accuracy
4. Odometry drift
5. LiDAR range
6. LiDAR resolution
7. Sensor fusion
8. Data synchronization

### Camera Tests
1. Camera init
2. Video quality
3. Frame rate
4. Exposure
5. White balance
6. Auto-focus
7. Low light
8. Color accuracy

### LiDAR Tests
1. Initialization
2. Range accuracy
3. Angular resolution
4. Rotation speed
5. Obstacle detection
6. Distance at 1m
7. Distance at 5m
8. Outdoor performance

## 📱 Web Dashboard Features

- 🎮 Real-time motor control
- 📊 Live sensor monitoring
- 📷 Camera feed streaming
- 📈 Performance graphs
- 📋 Event logging
- 🔔 Alert notifications
- 💾 Data recording
- 📊 Result analysis

## 🔧 Troubleshooting

### Camera not found
```bash
lsusb
v4l2-ctl --list-devices
```

### Port already in use
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Package not found
```bash
cd ~/robot_test_ws
colcon build --symlink-install
source install/setup.bash
```

### ROS2 connection failed
```bash
source /opt/ros/humble/setup.bash
source ~/ai_robot_ws/install/setup.bash
```

## 📝 System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | Ubuntu 22.04 LTS |
| ROS2 | Humble |
| Python | 3.10+ |
| RAM | 8GB |
| Storage | 50GB |
| GPU | NVIDIA Jetson Orin Nano Super |

## 🤝 Contributing

Contributions are welcome! Please create a pull request with:
- Clear description of changes
- Testing results
- Screenshots/videos if applicable

## 📄 License

MIT License - feel free to use and modify

## 🆘 Support

For issues and questions:
1. Check troubleshooting section
2. Review ROS2 documentation
3. Check system logs
4. Open an issue on GitHub

## 📚 References

- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Yahboom ROSMASTER Documentation](https://www.yahboom.com/)
- [NVIDIA Jetson Documentation](https://developer.nvidia.com/embedded/jetson-orin-nano)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)

---

**Last Updated**: June 2026  
**Version**: 1.0.0  
**Author**: Robot Development Team
