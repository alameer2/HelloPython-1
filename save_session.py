#!/usr/bin/env python3
"""
أمر سريع لحفظ جلسة Firefox والحسابات يدوياً
"""
import subprocess
from pathlib import Path

def save_firefox_session():
    """حفظ جلسة Firefox الحالية"""
    backup_script = Path.home() / "smart_backup.py"
    
    if backup_script.exists():
        print("🔄 جاري حفظ جلسة Firefox...")
        result = subprocess.run([
            "python3", str(backup_script)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ تم حفظ الجلسة والحسابات بنجاح!")
            print("💡 عند إعادة تشغيل المشروع، ستتم استعادة الجلسة تلقائياً")
        else:
            print("❌ فشل في حفظ الجلسة")
            print(f"خطأ: {result.stderr}")
    else:
        print("❌ نظام النسخ الاحتياطي غير متاح")

if __name__ == "__main__":
    save_firefox_session()