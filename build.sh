#!/bin/bash
# بناء كامل لنظام الروبوت
# Complete Build Script for Robot Control System

set -e

echo ""
echo "================================================"
echo "🔨 Building Robot Control System"
echo "================================================"
echo ""

# المسارات
CURRENT_DIR="$(pwd)"
WORKSPACE="$HOME/robot_test_ws"
SRC_PATH="$WORKSPACE/src"

# 1. إنشاء مساحة العمل
echo "📁 Creating workspace..."
mkdir -p $WORKSPACE/src
echo "✅ Workspace created at: $WORKSPACE"

# 2. نسخ الملفات
echo ""
echo "📂 Copying robot_test package..."
cp -r "$CURRENT_DIR/robot_test" "$SRC_PATH/"
echo "✅ Files copied"

# 3. تفعيل ROS2
echo ""
echo "📦 Setting up ROS2 environment..."
source /opt/ros/humble/setup.bash
echo "✅ ROS2 environment ready"

# 4. تجميع
echo ""
echo "🔨 Building packages..."
cd $WORKSPACE
colcon build --symlink-install

# 5. بناء bashrc
echo ""
echo "📝 Updating bashrc..."
if ! grep -q "robot_test_ws" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Robot Test Workspace" >> ~/.bashrc
    echo "source $WORKSPACE/install/setup.bash" >> ~/.bashrc
fi
echo "✅ bashrc updated"

echo ""
echo "================================================"
echo "✅ BUILD COMPLETED SUCCESSFULLY!"
echo "================================================"
echo ""
echo "🚀 Next steps:"
echo "   1. source $WORKSPACE/install/setup.bash"
echo "   2. ros2 run robot_test control_panel"
echo ""
