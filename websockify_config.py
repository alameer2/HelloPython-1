#!/usr/bin/env python3
"""
Websockify configuration and management
Professional websockify setup with error handling and logging
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

class WebsockifyManager:
    def __init__(self, port=5000, target_port=5901):
        self.websock_port = port
        self.target_port = target_port
        self.web_dir = "."
        
    def start_websockify(self):
        """Start websockify with proper configuration"""
        cmd = [
            sys.executable, "-m", "websockify",
            "--web", self.web_dir,
            "--heartbeat", "30",
            "--timeout", "0",
            f"{self.websock_port}",
            f"localhost:{self.target_port}"
        ]
        
        print(f"Starting websockify on port {self.websock_port}")
        print(f"Proxying to VNC server on port {self.target_port}")
        print(f"Web files served from: {self.web_dir}")
        
        try:
            subprocess.run(cmd, check=True)
        except KeyboardInterrupt:
            print("\nWebsockify stopped by user")
        except subprocess.CalledProcessError as e:
            print(f"Websockify failed: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
            
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start websockify for noVNC")
    parser.add_argument("--port", type=int, default=5000, help="Websockify port")
    parser.add_argument("--target", type=int, default=5901, help="VNC server port")
    
    args = parser.parse_args()
    
    manager = WebsockifyManager(args.port, args.target)
    manager.start_websockify()