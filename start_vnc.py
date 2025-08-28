#!/usr/bin/env python3
"""
Professional VNC Setup and Launcher
Configures and starts VNC server with noVNC web interface
"""

import os
import sys
import subprocess
import signal
import time
import atexit
from pathlib import Path

class VNCManager:
    def __init__(self):
        self.vnc_display = ":1"
        self.vnc_port = 5901
        self.websock_port = 5000
        self.geometry = "1024x768"
        self.vnc_dir = Path.home() / ".vnc"
        self.processes = []
        
    def setup_vnc_dir(self):
        """Create and configure VNC directory"""
        self.vnc_dir.mkdir(exist_ok=True)
        
        # Create xstartup file
        xstartup_path = self.vnc_dir / "xstartup"
        xstartup_content = """#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec fluxbox &
wait
"""
        xstartup_path.write_text(xstartup_content)
        xstartup_path.chmod(0o755)
        
        print(f"✓ VNC directory configured: {self.vnc_dir}")
        
    def set_vnc_password(self):
        """Set VNC password"""
        try:
            # Create password file using vncpasswd
            passwd_file = self.vnc_dir / "passwd"
            process = subprocess.run(
                ["/nix/store/nnkd8d66viqr8xg9vbiyhpjjgk2gzpf3-tigervnc-1.14.0/bin/vncpasswd", str(passwd_file)],
                input="vnc123\nvnc123\n",
                text=True,
                capture_output=True
            )
            if process.returncode == 0:
                print("✓ VNC password set successfully")
                return True
            else:
                print("⚠ VNC password setup failed, starting without authentication")
                return False
        except Exception as e:
            print(f"⚠ VNC password setup failed: {e}")
            return False
            
    def kill_existing_sessions(self):
        """Kill any existing VNC sessions"""
        try:
            subprocess.run(["vncserver", "-kill", self.vnc_display], 
                         capture_output=True)
            print("✓ Cleaned up existing VNC sessions")
        except:
            pass
            
    def start_vnc_server(self):
        """Start VNC server using direct Xvnc"""
        try:
            # Use Xvnc directly to avoid xinit dependency
            xvnc_path = "/nix/store/nnkd8d66viqr8xg9vbiyhpjjgk2gzpf3-tigervnc-1.14.0/bin/Xvnc"
            
            cmd = [
                xvnc_path,
                self.vnc_display,
                "-geometry", self.geometry,
                "-depth", "24",
                "-desktop", "Remote Desktop",
                "-rfbauth", str(self.vnc_dir / "passwd"),
                "-SecurityTypes", "VncAuth"
            ]
            
            # Start Xvnc in background  
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            self.processes.append(process)
            
            # Wait a bit for server to start
            time.sleep(2)
            
            if process.poll() is None:
                print(f"✓ VNC server started on display {self.vnc_display}")
                print(f"  Port: {self.vnc_port}")
                print(f"  Geometry: {self.geometry}")
                
                # Start a simple window manager
                self.start_window_manager()
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"✗ VNC server failed to start: {stderr.decode()}")
                return False
        except Exception as e:
            print(f"✗ VNC server startup error: {e}")
            return False
            
    def start_window_manager(self):
        """Start window manager and Firefox with persistent profile"""
        try:
            env = os.environ.copy()
            env["DISPLAY"] = self.vnc_display
            
            # Start fluxbox window manager
            wm_process = subprocess.Popen(
                ["fluxbox"],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )
            
            self.processes.append(wm_process)
            print(f"✓ Window manager started")
            
            # Wait for window manager to initialize
            time.sleep(3)
            
            # Start Firefox with persistent profile
            self.start_firefox_with_profile(env)
            
        except Exception as e:
            print(f"⚠ Window manager failed to start: {e}")
            
    def start_firefox_with_profile(self, env):
        """Start Firefox with persistent profile for session saving"""
        try:
            firefox_profile_dir = Path.home() / "firefox_profile"
            firefox_profile_dir.mkdir(exist_ok=True)
            
            # Create Firefox prefs for session saving and stability
            prefs_file = firefox_profile_dir / "user.js"
            prefs_content = '''
// Enhanced stability settings with session preservation
user_pref("browser.sessionstore.resume_from_crash", true);
user_pref("browser.startup.page", 3); // Restore previous session
user_pref("browser.sessionstore.restore_on_demand", false);
user_pref("browser.sessionstore.restore_hidden_tabs", true);
user_pref("browser.sessionstore.max_tabs_undo", 25);
user_pref("browser.sessionstore.max_windows_undo", 3);

// Force single process mode - critical for VNC stability
user_pref("browser.tabs.remote.autostart", false);
user_pref("browser.tabs.remote.desktopbehavior", false);
user_pref("dom.ipc.processCount", 1);
user_pref("dom.ipc.processCount.extension", 1);
user_pref("dom.ipc.processCount.file", 1);
user_pref("dom.ipc.processCount.privilegedabout", 1);
user_pref("dom.ipc.processCount.privilegedmozilla", 1);
user_pref("dom.ipc.processCount.web", 1);
user_pref("dom.ipc.processCount.webIsolated", 1);

// Disable all forms of multiprocessing
user_pref("dom.ipc.plugins.enabled", false);
user_pref("dom.ipc.plugins.enabled.libflashplayer.so", false);
user_pref("extensions.webextensions.remote", false);

// Memory and performance optimizations
user_pref("browser.cache.memory.capacity", 16384);  // 16MB memory cache
user_pref("browser.cache.disk.capacity", 51200);    // 50MB disk cache
user_pref("browser.sessionhistory.max_total_viewers", 0);
user_pref("dom.max_script_run_time", 0);
user_pref("dom.max_chrome_script_run_time", 0);

// Disable hardware acceleration completely
user_pref("layers.acceleration.disabled", true);
user_pref("gfx.direct2d.disabled", true);
user_pref("webgl.disabled", true);
user_pref("gfx.canvas.azure.backends", "cairo");
user_pref("layers.acceleration.force-enabled", false);

// Disable crash reporting and error dialogs
user_pref("toolkit.crashreporter.enabled", false);
user_pref("browser.crashReports.unsubmittedCheck.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");

// Disable update and sync services
user_pref("app.update.enabled", false);
user_pref("app.update.auto", false);
user_pref("services.sync.prefs.sync.browser.startup.homepage", false);

// Session and login preservation
user_pref("browser.newtabpage.enabled", true);
user_pref("browser.sessionstore.interval", 15000); // Save every 15 seconds
user_pref("privacy.clearOnShutdown.cookies", false);
user_pref("privacy.clearOnShutdown.sessions", false);
user_pref("privacy.clearOnShutdown.formdata", false);
user_pref("privacy.clearOnShutdown.downloads", false);
user_pref("privacy.clearOnShutdown.history", false);
user_pref("signon.rememberSignons", true);
user_pref("signon.autofillForms", true);
user_pref("signon.generation.enabled", true);

// Disable potentially problematic features
user_pref("accessibility.force_disabled", 1);
user_pref("browser.safebrowsing.enabled", false);
user_pref("browser.safebrowsing.malware.enabled", false);
user_pref("network.prefetch-next", false);
'''
            prefs_file.write_text(prefs_content)
            
            # Start Firefox with the persistent profile and stability options
            firefox_process = subprocess.Popen([
                "firefox-esr",
                "--profile", str(firefox_profile_dir),
                "--new-instance",
                "--no-remote",   # Prevent interaction with other Firefox instances
                "--disable-extensions",
                "--disable-plugins",
                "--no-sandbox",   # VNC environment doesn't need sandboxing
                "--disable-dev-shm-usage",  # Prevent crashes in limited environments
                "--disable-gpu",  # Disable GPU for VNC stability
                "--single-process"  # Force single process mode
            ], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
            
            self.processes.append(firefox_process)
            print(f"✓ Firefox started with persistent profile (stable mode)")
            print(f"  Profile location: {firefox_profile_dir}")
            
            # Remove Firefox monitoring - let it run independently
            
        except Exception as e:
            print(f"⚠ Firefox startup failed: {e}")

    def start_firefox_monitor(self, env):
        """Monitor Firefox and restart it if it crashes"""
        def monitor_firefox():
            time.sleep(5)  # Initial wait
            while True:
                try:
                    # Check if Firefox is running
                    result = subprocess.run(
                        ["pgrep", "-f", "firefox-esr"],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode != 0:  # Firefox not running
                        print("🔄 Firefox crashed, restarting...")
                        
                        # Restart Firefox
                        firefox_profile_dir = Path.home() / "firefox_profile"
                        firefox_process = subprocess.Popen([
                            "firefox-esr",
                            "--profile", str(firefox_profile_dir),
                            "--new-instance",
                            "--no-remote",
                            "--disable-extensions",
                            "--disable-plugins",
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-gpu",
                            "--single-process"
                        ], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
                        
                        self.processes.append(firefox_process)
                        print("✓ Firefox restarted successfully")
                    
                    time.sleep(30)  # Check every 30 seconds
                    
                except Exception as e:
                    print(f"⚠ Firefox monitor error: {e}")
                    time.sleep(10)
        
        # Start monitor in background thread
        import threading
        monitor_thread = threading.Thread(target=monitor_firefox, daemon=True)
        monitor_thread.start()
            
    def start_websockify(self):
        """Start websockify for noVNC"""
        try:
            cmd = [
                "python3", "-m", "websockify",
                "--web", ".",
                str(self.websock_port),
                f"localhost:{self.vnc_port}"
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
            )
            
            self.processes.append(process)
            print(f"✓ Websockify started on port {self.websock_port}")
            print(f"  Web interface: http://localhost:{self.websock_port}")
            return process
        except Exception as e:
            print(f"✗ Websockify startup error: {e}")
            return None
            
    def backup_before_shutdown(self):
        """نسخ احتياطي ذكي قبل الإغلاق"""
        try:
            backup_script = Path.home() / "smart_backup.py"
            if backup_script.exists():
                result = subprocess.run([
                    "python3", str(backup_script)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✓ تم حفظ جلسة Firefox والحسابات بنجاح")
                else:
                    print("⚠ فشل في حفظ الجلسة")
        except Exception as e:
            print(f"⚠ خطأ في حفظ الجلسة: {e}")

    def cleanup_with_backup(self):
        """تنظيف مع نسخ احتياطي تلقائي"""
        print("\nبدء الإغلاق الآمن...")
        
        # نسخ احتياطي قبل الإغلاق
        self.backup_before_shutdown()
        
        # تنظيف العمليات
        for process in self.processes:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except:
                pass
                
        # إيقاف خادم VNC
        try:
            subprocess.run(["vncserver", "-kill", self.vnc_display], 
                         capture_output=True)
        except:
            pass
            
        print("✓ تم الإغلاق الآمن مع حفظ البيانات")

    def cleanup(self):
        """Clean up processes (fallback)"""
        self.cleanup_with_backup()
        
    def restore_firefox_data(self):
        """استعادة جلسة Firefox والحسابات المحفوظة"""
        try:
            backup_dir = Path.home() / "firefox_backups"
            profile_dir = Path.home() / "firefox_profile"
            
            if backup_dir.exists():
                # البحث عن جلسات Firefox المحفوظة
                session_backups = list(backup_dir.glob("firefox_session_*.tar.gz"))
                if session_backups:
                    latest_session = max(session_backups, key=lambda x: x.stat().st_mtime)
                    print(f"🔄 استعادة جلسة Firefox المحفوظة: {latest_session.name}")
                    
                    # حذف الملف الشخصي القديم إذا كان موجوداً
                    if profile_dir.exists():
                        subprocess.run(["rm", "-rf", str(profile_dir)], capture_output=True)
                    
                    # استعادة الجلسة المحفوظة
                    result = subprocess.run(
                        ["tar", "-xzf", str(latest_session), "-C", str(Path.home())],
                        capture_output=True
                    )
                    
                    if result.returncode == 0:
                        print("✓ تم استعادة جلسة Firefox والحسابات المحفوظة بنجاح")
                        return True
                    else:
                        print("⚠ فشل في استعادة الجلسة، سيتم إنشاء ملف تعريف جديد")
                else:
                    print("📁 لا توجد جلسات محفوظة، سيتم إنشاء ملف تعريف جديد")
            else:
                print("📁 مجلد الجلسات غير موجود، سيتم إنشاء ملف تعريف جديد")
                
            return False
                
        except Exception as e:
            print(f"⚠ خطأ في استعادة الجلسة: {e}")
            return False

    def setup_smart_backup(self):
        """إعداد نظام نسخ احتياطي ذكي - حفظ فقط عند الإغلاق"""
        try:
            # إنشاء script للنسخ الاحتياطي عند الحاجة فقط
            backup_script = Path.home() / "smart_backup.py"
            backup_content = '''#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path
from datetime import datetime

def backup_firefox_on_shutdown():
    """نسخ احتياطي ذكي عند الإغلاق فقط"""
    profile_dir = Path.home() / "firefox_profile"
    backup_dir = Path.home() / "firefox_backups"
    
    if not profile_dir.exists():
        return False
        
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"firefox_session_{timestamp}.tar.gz"
    
    try:
        # نسخ احتياطي للملف الشخصي بالكامل
        subprocess.run([
            "tar", "-czf", str(backup_file),
            "-C", str(Path.home()),
            "firefox_profile"
        ], capture_output=True, check=True)
        
        # الاحتفاظ بآخر 5 نسخ احتياطية فقط
        backups = sorted(backup_dir.glob("firefox_session_*.tar.gz"), 
                        key=lambda x: x.stat().st_mtime, reverse=True)
        for old_backup in backups[5:]:
            old_backup.unlink()
            
        print(f"✓ تم حفظ جلسة Firefox: {backup_file.name}")
        return True
            
    except Exception as e:
        print(f"⚠ خطأ في النسخ الاحتياطي: {e}")
        return False

if __name__ == "__main__":
    backup_firefox_on_shutdown()
'''
            backup_script.write_text(backup_content)
            backup_script.chmod(0o755)
            print("✓ تم إعداد نظام النسخ الاحتياطي الذكي")
            
        except Exception as e:
            print(f"⚠ فشل في إعداد النسخ الاحتياطي الذكي: {e}")

    def run(self):
        """Main execution function"""
        print("🚀 Starting Professional VNC Setup...")
        print("=" * 50)
        
        # Register cleanup function with auto-backup
        atexit.register(self.cleanup_with_backup)
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
        
        # استعادة بيانات فايرفوكس تلقائياً
        self.restore_firefox_data()
        
        # Setup steps
        self.setup_vnc_dir()
        self.set_vnc_password()
        self.kill_existing_sessions()
        
        # Start services
        if not self.start_vnc_server():
            return False
            
        websockify_process = self.start_websockify()
        if not websockify_process:
            return False
            
        # Add smart backup on shutdown only
        self.setup_smart_backup()
            
        print("\n" + "=" * 50)
        print("🎉 VNC Setup Complete!")
        print("=" * 50)
        print(f"VNC Display: {self.vnc_display}")
        print(f"VNC Port: {self.vnc_port}")
        print(f"Web Interface: http://localhost:{self.websock_port}")
        print(f"noVNC URL: http://localhost:{self.websock_port}/vnc.html")
        print("Password: vnc123")
        print("=" * 50)
        
        # Keep running
        try:
            while True:
                time.sleep(1)
                # Check if websockify is still running
                if websockify_process.poll() is not None:
                    print("Websockify process died, restarting...")
                    websockify_process = self.start_websockify()
                    if not websockify_process:
                        break
        except KeyboardInterrupt:
            print("\nShutting down...")
            
        return True

if __name__ == "__main__":
    manager = VNCManager()
    success = manager.run()
    sys.exit(0 if success else 1)