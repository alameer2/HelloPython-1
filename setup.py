#!/usr/bin/env python3
"""
Setup script for VNC Desktop Remote Access
تسكريبت إعداد نظام سطح المكتب البعيد
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_command(cmd):
    """Check if command is available"""
    return shutil.which(cmd) is not None

def install_dependencies():
    """Install required system dependencies"""
    print("🔧 تثبيت المتطلبات...")
    
    # Check if dependencies are already installed
    required_commands = ['firefox-esr', 'Xvnc', 'python3']
    missing_commands = [cmd for cmd in required_commands if not check_command(cmd)]
    
    if missing_commands:
        print(f"⚠️  المتطلبات المفقودة: {', '.join(missing_commands)}")
        print("📋 يرجى تثبيت المتطلبات التالية:")
        print("- TigerVNC Server")
        print("- Firefox ESR")
        print("- Fluxbox Window Manager")
        print("- Python 3 + websockify")
        return False
    
    # Install Python dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "websockify"], 
                      check=True, capture_output=True)
        print("✅ تم تثبيت websockify")
    except subprocess.CalledProcessError:
        print("⚠️  فشل في تثبيت websockify")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print("📁 إنشاء المجلدات...")
    
    directories = [
        Path.home() / ".vnc",
        Path.home() / "firefox_profile", 
        Path.home() / "firefox_backups"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✅ {directory}")

def setup_permissions():
    """Set up file permissions"""
    print("🔐 إعداد الصلاحيات...")
    
    executable_files = [
        "start_vnc.py",
        "setup.py",
        "firefox_backup.sh",
        "firefox_restore.sh",
        "desktop_setup.sh"
    ]
    
    for file in executable_files:
        if Path(file).exists():
            Path(file).chmod(0o755)
            print(f"✅ {file}")

def main():
    """Main setup function"""
    print("🚀 بدء إعداد مشروع سطح المكتب البعيد...")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ فشل في تثبيت المتطلبات")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Setup permissions
    setup_permissions()
    
    # Run desktop setup
    if Path("desktop_setup.sh").exists():
        subprocess.run(["./desktop_setup.sh"], capture_output=True)
        print("✅ تم إعداد بيئة سطح المكتب")
    
    print("\n" + "=" * 50)
    print("🎉 تم الإعداد بنجاح!")
    print("=" * 50)
    print("للتشغيل: python3 start_vnc.py")
    print("الواجهة: http://localhost:5000")
    print("كلمة المرور: vnc123")
    print("=" * 50)

if __name__ == "__main__":
    main()