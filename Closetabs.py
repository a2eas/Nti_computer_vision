import pygetwindow as gw
import psutil
import sys
sys.stdout.reconfigure(encoding='utf-8')
# List all window titles
def close_tabs():
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        window.minimize()
    print('delete all windows')