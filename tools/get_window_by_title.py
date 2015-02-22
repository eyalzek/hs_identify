import sys
import win32gui
import win32ui
import win32con
import win32api
from time import sleep
from datetime import datetime

def get_windows_bytitle(title_text):
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(_window_callback, windows)
    return [hwnd for hwnd, title in windows if title_text in title]

def screenshot(hwnd, filename):
    l,t,r,b = win32gui.GetClientRect(hwnd)
    fs = False
    h = b - t
    w = r - l
    if w == 0 or h == 0: # probably means the app is in fullscreen
        w, h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        fs = True
    
    hDC = win32gui.GetDC(hwnd)
    myDC = win32ui.CreateDCFromHandle(hDC)
    newDC = myDC.CreateCompatibleDC()

    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)

    newDC.SelectObject(myBitMap)

    if fs:
        win32gui.ShowWindow(hwnd, 3)
    else:
        win32gui.SetForegroundWindow(hwnd)
    sleep(.2) #lame way to allow screen to draw before taking shot
    newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
    myBitMap.Paint(newDC)
    path = "c:\\Temp\\" + filename
    try:
        myBitMap.SaveBitmapFile(newDC, path)
        print("file saved as: %s" %path)
    except IOError:
        print("file failed to save")

def main():
    try:
        hwnd = get_windows_bytitle("Hearthstone")[0]
        screenshot(hwnd, str(datetime.now().microsecond) + ".bmp")
    except IndexError:
        print("Hearthstone window not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
