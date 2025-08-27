#!/usr/bin/env python3
"""
Main entry point for VNC Desktop Remote Access
نقطة البدء الرئيسية لمشروع سطح المكتب البعيد
"""

import os
import sys
import subprocess
from pathlib import Path

def check_setup():
    """Check if setup has been run"""
    vnc_dir = Path.home() / ".vnc"
    firefox_dir = Path.home() / "firefox_profile"
    
    return vnc_dir.exists() and firefox_dir.exists()

def main():
    """Main function"""
    print("🚀 مشروع سطح المكتب البعيد - VNC Desktop Remote Access")
    print("=" * 60)
    
    # Check if setup is needed
    if not check_setup():
        print("🔧 تشغيل الإعداد الأولي...")
        try:
            subprocess.run([sys.executable, "setup.py"], check=True)
        except subprocess.CalledProcessError:
            print("❌ فشل في الإعداد الأولي")
            sys.exit(1)
    
    # Start VNC server
    print("🌟 بدء خدمة سطح المكتب البعيد...")
    try:
        subprocess.run([sys.executable, "start_vnc.py"])
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف الخدمة بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في التشغيل: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()