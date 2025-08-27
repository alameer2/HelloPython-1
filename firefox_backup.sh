#!/bin/bash
# نسخ احتياطي لبيانات فايرفوكس - Firefox Backup Script

PROFILE_DIR="$HOME/firefox_profile"
BACKUP_DIR="$HOME/firefox_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "🔄 بدء النسخ الاحتياطي لبيانات فايرفوكس..."

# إنشاء مجلد النسخ الاحتياطية
mkdir -p "$BACKUP_DIR"

# إنشاء نسخة احتياطية
if [ -d "$PROFILE_DIR" ]; then
    tar -czf "$BACKUP_DIR/firefox_backup_$TIMESTAMP.tar.gz" -C "$HOME" firefox_profile
    echo "✓ تم إنشاء نسخة احتياطية: firefox_backup_$TIMESTAMP.tar.gz"
    
    # حفظ آخر 5 نسخ احتياطية فقط
    cd "$BACKUP_DIR"
    ls -t firefox_backup_*.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm
    echo "✓ تم تنظيف النسخ الاحتياطية القديمة"
else
    echo "⚠ مجلد البيانات غير موجود: $PROFILE_DIR"
fi

echo "📁 موقع النسخ الاحتياطية: $BACKUP_DIR"