# إعداد سطح المكتب البعيد - Remote Desktop VNC Setup

## نظرة عامة
مشروع احترافي لإعداد وتشغيل سطح مكتب بعيد باستخدام VNC مع واجهة ويب noVNC.

## المتطلبات المثبتة ✅
- TigerVNC Server
- Firefox ESR
- Fluxbox Desktop Environment
- Python 3.11 + Websockify
- noVNC Web Interface

## طريقة التشغيل

### 1. التشغيل السريع
```bash
python3 start_vnc.py
```

### 2. التشغيل اليدوي
```bash
# بدء خادم VNC
vncserver :1 -geometry 1024x768

# بدء websockify
python3 websockify_config.py --port 5000 --target 5901
```

## الوصول للمشروع
- **واجهة الويب**: http://localhost:5000
- **noVNC مباشر**: http://localhost:5000/vnc.html
- **كلمة المرور الافتراضية**: vnc123

## الميزات
- 🖥️ واجهة سطح مكتب كاملة
- 🌐 وصول عبر المتصفح
- 🔒 حماية بكلمة مرور
- 📱 دعم الأجهزة المحمولة
- 🎨 واجهة مستخدم محسّنة

## إعدادات مخصصة
- **الدقة**: 1024x768 (قابلة للتعديل في vnc_config)
- **المنفذ**: 5000 (قابل للتعديل)
- **بيئة سطح المكتب**: Fluxbox

## استكشاف الأخطاء
1. تأكد من أن المنفذ 5000 غير مستخدم
2. تحقق من تشغيل خدمات VNC
3. راجع سجلات الأخطاء في الكونسول