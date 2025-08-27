# تثبيت وتشغيل مشروع سطح المكتب البعيد
# VNC Desktop Remote Access - Installation Guide

## التثبيت السريع / Quick Install

### 1. استنساخ المشروع / Clone Repository
```bash
git clone [your-repo-url]
cd [repo-name]
```

### 2. التشغيل التلقائي / Automatic Setup & Run
```bash
python3 run.py
```
أو
```bash
python3 setup.py  # للإعداد فقط
python3 start_vnc.py  # للتشغيل
```

## المتطلبات / Requirements

### متطلبات النظام / System Requirements
- Linux/Unix system
- Python 3.7+
- TigerVNC Server
- Firefox ESR
- Fluxbox Window Manager

### تثبيت المتطلبات في Replit / Install in Replit
المشروع مُعد للعمل التلقائي في Replit. فقط:
1. استورد المشروع
2. شغل `python3 run.py`

### تثبيت المتطلبات في أنظمة أخرى / Install on Other Systems

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install tigervnc-standalone-server firefox-esr fluxbox python3-pip
pip3 install websockify
```

#### CentOS/RHEL:
```bash
sudo yum install tigervnc-server firefox fluxbox python3-pip
pip3 install websockify
```

## الاستخدام / Usage

### بدء التشغيل / Start Service
```bash
python3 run.py
```

### الوصول للواجهة / Access Interface
- **الموقع**: http://localhost:5000
- **كلمة المرور**: vnc123
- **دقة الشاشة**: 1024x768

### إيقاف التشغيل / Stop Service
- اضغط `Ctrl+C` في Terminal
- أو أغلق نافذة المتصفح

## الميزات / Features

✅ **سطح مكتب كامل** - Full desktop environment
✅ **حفظ تلقائي للجلسات** - Automatic session save
✅ **نسخ احتياطي ذكي** - Smart backup system
✅ **استعادة تلقائية** - Auto restore
✅ **أمان محسّن** - Enhanced security
✅ **واجهة عربية** - Arabic interface support

## استكشاف الأخطاء / Troubleshooting

### مشكلة الاتصال / Connection Issues
```bash
# تنظيف الملفات المؤقتة
rm -f /tmp/.X*-lock
pkill -f Xvnc
python3 start_vnc.py
```

### مشكلة كلمة المرور / Password Issues
كلمة المرور الافتراضية: `vnc123`

### إعادة إعداد البيانات / Reset Data
```bash
rm -rf ~/.vnc ~/firefox_profile ~/firefox_backups
python3 setup.py
```

## ملفات المشروع / Project Files

- `run.py` - نقطة البدء الرئيسية
- `start_vnc.py` - خادم VNC الرئيسي
- `setup.py` - سكريبت الإعداد
- `firefox_backup.sh` - نسخ احتياطي يدوي
- `firefox_restore.sh` - استعادة يدوية
- `desktop_setup.sh` - إعداد سطح المكتب

## الدعم / Support

إذا واجهت أي مشاكل، تأكد من:
1. تثبيت جميع المتطلبات
2. تشغيل `python3 setup.py` أولاً
3. التأكد من المنفذ 5000 غير مستخدم