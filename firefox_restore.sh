#!/bin/bash
# استعادة بيانات فايرفوكس - Firefox Restore Script

PROFILE_DIR="$HOME/firefox_profile"
BACKUP_DIR="$HOME/firefox_backups"

echo "🔄 استعادة بيانات فايرفوكس..."

# العثور على أحدث نسخة احتياطية
LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/firefox_backup_*.tar.gz 2>/dev/null | head -n1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ لا توجد نسخ احتياطية متاحة"
    exit 1
fi

echo "📂 استعادة من: $(basename $LATEST_BACKUP)"

# حذف المجلد الحالي إذا كان موجوداً
if [ -d "$PROFILE_DIR" ]; then
    rm -rf "$PROFILE_DIR"
    echo "✓ تم حذف البيانات القديمة"
fi

# استعادة النسخة الاحتياطية
tar -xzf "$LATEST_BACKUP" -C "$HOME"

if [ $? -eq 0 ]; then
    echo "✅ تم استعادة بيانات فايرفوكس بنجاح"
    echo "📁 موقع البيانات المستعادة: $PROFILE_DIR"
else
    echo "❌ فشل في استعادة البيانات"
    exit 1
fi