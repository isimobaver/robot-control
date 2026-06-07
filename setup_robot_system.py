#!/usr/bin/env python3
"""
🤖 Robot Control System - Complete Management Interface
نظام التحكم الكامل بالروبوت الأمني
"""

import sys
import time
import subprocess
from pathlib import Path

class RobotSetupManager:
    """إدارة إعداد نظام الروبوت"""
    
    def __init__(self):
        self.workspace_path = Path.home() / "robot_test_ws"
        self.ai_robot_path = Path.home() / "ai_robot_ws"
        self.current_path = Path.cwd()
    
    def print_banner(self):
        """طباعة البنر الرئيسي"""
        print("\n" + "="*70)
        print("🤖 ROBOT CONTROL SYSTEM - نظام التحكم بالروبوت الأمني")
        print("="*70)
        print()
    
    def check_dependencies(self):
        """التحقق من المتطلبات"""
        print("\n📦 Checking Dependencies...\n")
        
        dependencies = {
            'ROS2': 'which ros2',
            'Python3': 'which python3',
            'colcon': 'which colcon',
            'pip3': 'which pip3',
        }
        
        missing = []
        for name, command in dependencies.items():
            result = subprocess.run(command, shell=True, capture_output=True)
            if result.returncode == 0:
                print(f"✅ {name} installed")
            else:
                print(f"❌ {name} NOT found")
                missing.append(name)
        
        return len(missing) == 0
    
    def setup_workspace(self):
        """إعداد مساحة العمل"""
        print("\n🏗️  Setting up Robot Test Workspace...\n")
        
        # إنشاء المجلدات
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        src_path = self.workspace_path / "src"
        src_path.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Workspace created at: {self.workspace_path}")
        
        # نسخ Package
        robot_test_src = self.current_path / "robot_test"
        robot_test_dst = src_path / "robot_test"
        
        if robot_test_src.exists():
            subprocess.run(f"cp -r {robot_test_src} {robot_test_dst}", shell=True)
            print(f"✅ Package copied to workspace")
        
        return True
    
    def build_workspace(self):
        """بناء مساحة العمل"""
        print("\n🔨 Building Workspace...\n")
        
        try:
            result = subprocess.run(
                f"cd {self.workspace_path} && colcon build --symlink-install",
                shell=True,
                capture_output=False
            )
            
            if result.returncode == 0:
                print("\n✅ Build completed successfully")
                return True
            else:
                print("\n❌ Build failed")
                return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def install_python_deps(self):
        """تثبيت متطلبات Python"""
        print("\n📚 Installing Python Dependencies...\n")
        
        packages = [
            'flask',
            'flask-socketio',
            'opencv-python',
            'numpy',
            'pillow',
            'pyserial',
            'PyYAML',
            'roslibpy',
            'ultralytics',
            'torch',
            'torchvision',
        ]
        
        for package in packages:
            print(f"📦 Installing {package}...")
            result = subprocess.run(
                f"pip3 install -q {package}",
                shell=True,
                capture_output=True
            )
            
            if result.returncode == 0:
                print(f"  ✅ {package} installed")
            else:
                print(f"  ⚠️  {package} installation skipped")
    
    def run_setup(self):
        """تشغيل الإعداد الكامل"""
        self.print_banner()
        
        # 1. التحقق من المتطلبات
        if not self.check_dependencies():
            print("\n⚠️  Some dependencies are missing")
            print("Please install them before continuing")
            return False
        
        # 2. تثبيت متطلبات Python
        self.install_python_deps()
        
        # 3. إعداد مساحة العمل
        if not self.setup_workspace():
            return False
        
        # 4. بناء مساحة العمل
        if not self.build_workspace():
            return False
        
        # 5. تعديل bashrc
        self.update_bashrc()
        
        print("\n" + "="*70)
        print("✅ SETUP COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n🚀 Next steps:")
        print(f"   1. source {self.workspace_path}/install/setup.bash")
        print(f"   2. ros2 run robot_test control_panel")
        print("\n")
        
        return True
    
    def update_bashrc(self):
        """تحديث bashrc"""
        bashrc_path = Path.home() / ".bashrc"
        
        source_line = f"source {self.workspace_path}/install/setup.bash"
        
        if bashrc_path.exists():
            with open(bashrc_path, 'r') as f:
                content = f.read()
            
            if source_line not in content:
                with open(bashrc_path, 'a') as f:
                    f.write(f"\n# Robot Test Workspace\n{source_line}\n")
                print(f"✅ Updated .bashrc")

def main():
    manager = RobotSetupManager()
    success = manager.run_setup()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
