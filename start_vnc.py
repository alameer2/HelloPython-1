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
                stdout=subprocess.PIPE,
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
        """Start window manager in the VNC session"""
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
        except Exception as e:
            print(f"⚠ Window manager failed to start: {e}")
            
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
            
    def cleanup(self):
        """Clean up processes"""
        print("\nCleaning up...")
        
        # Kill websockify processes
        for process in self.processes:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except:
                pass
                
        # Kill VNC server
        try:
            subprocess.run(["vncserver", "-kill", self.vnc_display], 
                         capture_output=True)
        except:
            pass
            
        print("✓ Cleanup completed")
        
    def run(self):
        """Main execution function"""
        print("🚀 Starting Professional VNC Setup...")
        print("=" * 50)
        
        # Register cleanup function
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
        
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