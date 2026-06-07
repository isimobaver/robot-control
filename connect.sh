#!/bin/bash
# ربط الروبوت مع النظام
# Quick Connect Script

echo ""
echo "========================================"
echo "🤖 Robot Control System - Quick Connect"
echo "========================================"
echo ""

# التحقق من robot_test_ws
if [ ! -d "$HOME/robot_test_ws" ]; then
    echo "⚠️  robot_test_ws not found!"
    echo "📁 Creating and building workspace..."
    
    mkdir -p ~/robot_test_ws/src
    cp -r ./robot_test ~/robot_test_ws/src/
    
    cd ~/robot_test_ws
    source /opt/ros/humble/setup.bash
    colcon build --symlink-install
fi

# البناء في bashrc
if ! grep -q "robot_test_ws" ~/.bashrc 2>/dev/null; then
    echo "source ~/robot_test_ws/install/setup.bash" >> ~/.bashrc
fi

echo "✅ Setup completed!"
echo ""
echo "📋 Next: Open 2 terminals:"
echo ""
echo "Terminal 1 (Control Panel):"
echo "  source ~/robot_test_ws/install/setup.bash"
echo "  ros2 run robot_test control_panel"
echo ""
echo "Terminal 2 (Robot):"
echo "  source ~/ai_robot_ws/install/setup.bash"
echo "  ros2 launch ai_robot robot.launch.py"
echo ""
