#!/bin/bash
# نظام التحكم بالروبوت - سكريبت البدء السريع
# Robot Control System - Quick Start Script

set -e

echo ""
echo "========================================"
echo "🤖 Robot Control System - Quick Start"
echo "========================================"
echo ""

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 found${NC}"

# التحقق من ROS2
if [ ! -d "/opt/ros/humble" ]; then
    echo -e "${RED}❌ ROS2 Humble not found${NC}"
    echo "Please install ROS2 Humble first"
    exit 1
fi

echo -e "${GREEN}✅ ROS2 Humble found${NC}"

# تشغيل الإعداد
echo ""
echo -e "${BLUE}🔧 Running setup...${NC}"
echo ""

python3 setup_robot_system.py

echo ""
echo -e "${GREEN}✅ Setup completed!${NC}"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Open terminal 1: source ~/robot_test_ws/install/setup.bash && ros2 run robot_test control_panel"
echo "2. Open terminal 2: source ~/ai_robot_ws/install/setup.bash && ros2 launch ai_robot robot.launch.py"
echo ""
