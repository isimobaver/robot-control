#!/bin/bash
# شروحات سريعة لربط الروبوت
# Quick Manual Steps

echo ""
echo "========================================"
echo "🤖 Robot Control - Manual Setup"
echo "========================================"
echo ""

echo "📋 Step 1: Create workspace and copy files"
echo "   mkdir -p ~/robot_test_ws/src"
echo "   cp -r ./robot_test ~/robot_test_ws/src/"
echo ""

echo "🔨 Step 2: Build the system"
echo "   cd ~/robot_test_ws"
echo "   source /opt/ros/humble/setup.bash"
echo "   colcon build --symlink-install"
echo ""

echo "🚀 Step 3: Run in separate terminals"
echo ""
echo "   Terminal 1:"
echo "   source ~/robot_test_ws/install/setup.bash"
echo "   ros2 run robot_test control_panel"
echo ""
echo "   Terminal 2:"
echo "   source ~/ai_robot_ws/install/setup.bash"
echo "   ros2 launch ai_robot robot.launch.py"
echo ""
echo "========================================"
echo ""
