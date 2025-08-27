#!/bin/bash
# Desktop Environment Setup Script

echo "🖥️  Setting up desktop environment..."

# Create desktop directories
mkdir -p ~/Desktop
mkdir -p ~/Documents
mkdir -p ~/Downloads

# Set up basic desktop files
cat > ~/Desktop/Firefox.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Firefox
Comment=Web Browser
Exec=firefox-esr
Icon=firefox
Terminal=false
Categories=Network;WebBrowser;
EOF

cat > ~/Desktop/Terminal.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Terminal
Comment=Terminal Emulator
Exec=xterm
Icon=terminal
Terminal=false
Categories=System;TerminalEmulator;
EOF

# Make desktop files executable
chmod +x ~/Desktop/*.desktop

# Set up fluxbox configuration
mkdir -p ~/.fluxbox
cat > ~/.fluxbox/startup << 'EOF'
#!/bin/bash
# Fluxbox startup script

# Start desktop background
if command -v feh &> /dev/null; then
    feh --bg-scale --no-fehbg /usr/share/pixmaps/debian-logo.png &
fi

# Start panel/taskbar if available
if command -v tint2 &> /dev/null; then
    tint2 &
fi

# Start file manager daemon
if command -v pcmanfm &> /dev/null; then
    pcmanfm --desktop &
fi

# Finally start fluxbox
exec fluxbox
EOF

chmod +x ~/.fluxbox/startup

# Create basic fluxbox menu
cat > ~/.fluxbox/menu << 'EOF'
[begin] (Fluxbox Menu)
    [exec] (Firefox) {firefox-esr}
    [exec] (Terminal) {xterm}
    [submenu] (Applications)
        [exec] (Firefox) {firefox-esr}
        [exec] (Terminal) {xterm}
    [end]
    [separator]
    [submenu] (System)
        [exec] (Restart Fluxbox) {fluxbox-restart}
        [exit] (Exit)
    [end]
[end]
EOF

echo "✓ Desktop environment configured"