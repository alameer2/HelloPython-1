{ pkgs }: {
  deps = [
    pkgs.xfce4
    pkgs.firefox-esr
    pkgs.tigervnc
    pkgs.novnc
    pkgs.websockify
    pkgs.git
    pkgs.wget
  ];
}