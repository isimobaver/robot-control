#!/usr/bin/env python3
"""
🤖 Robot Control - All in One Setup & Run
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """تنفيذ أمر"""
    if description:
        print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🤖 ROBOT CONTROL SYSTEM - SETUP & BUILD")
    print("="*60)
    
    home = Path.home()
    workspace = home / "robot_test_ws"
    current_dir = Path.cwd()
    
    # 1. Create workspace
    print("\n📁 Creating workspace...")
    (workspace / "src").mkdir(parents=True, exist_ok=True)
    print("✅ Workspace created")
    
    # 2. Copy robot_test package
    print("\n📂 Copying robot_test package...")
    robot_test_src = current_dir / "robot_test"
    robot_test_dst = workspace / "src" / "robot_test"
    
    if robot_test_src.exists():
        os.system(f"cp -r {robot_test_src} {robot_test_dst.parent}/")
        print("✅ Package copied")
    else:
        print(f"❌ robot_test not found at {robot_test_src}")
        return False
    
    # 3. Build
    print("\n🔨 Building workspace...")
    os.chdir(workspace)
    
    result = subprocess.run(
        "source /opt/ros/humble/setup.bash && colcon build --symlink-install",
        shell=True
    )
    
    if result.returncode != 0:
        print("❌ Build failed")
        return False
    
    print("✅ Build completed")
    
    # 4. Update bashrc
    print("\n📝 Updating bashrc...")
    bashrc = home / ".bashrc"
    source_line = f"source {workspace}/install/setup.bash"
    
    if bashrc.exists():
        with open(bashrc, 'r') as f:
            content = f.read()
        
        if source_line not in content:
            with open(bashrc, 'a') as f:
                f.write(f"\n# Robot Test Workspace\n{source_line}\n")
    
    print("✅ bashrc updated")
    
    # 5. Print instructions
    print("\n" + "="*60)
    print("✅ SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\n🚀 Next steps:")
    print("\n📌 Apply changes to current shell:")
    print(f"   source {workspace}/install/setup.bash")
    print("\n📌 Then run (in separate terminals):")
    print("\n   Terminal 1 - Control Panel:")
    print("   ros2 run robot_test control_panel")
    print("\n   Terminal 2 - Robot:")
    print("   source ~/ai_robot_ws/install/setup.bash")
    print("   ros2 launch ai_robot robot.launch.py")
    print("\n" + "="*60 + "\n")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
