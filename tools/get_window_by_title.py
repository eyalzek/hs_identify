import sys
import win32gui
import win32ui
import win32con
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
    h = b - t
    w = r - l
    hDC = win32gui.GetDC(hwnd)
    myDC = win32ui.CreateDCFromHandle(hDC)
    newDC = myDC.CreateCompatibleDC()

    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)

    newDC.SelectObject(myBitMap)

    win32gui.SetForegroundWindow(hwnd)
    sleep(.2) #lame way to allow screen to draw before taking shot
    newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
    myBitMap.Paint(newDC)
    myBitMap.SaveBitmapFile(newDC, "c:\\" + filename)

def main():
    try:
        hwnd = get_windows_bytitle("Hearthstone")[0]
    except IndexError:
        print("Hearthstone window not found")
        sys.exit(1)

    screenshot(hwnd, str(datetime.now().microsecond) + ".bmp")


if __name__ == "__main__":
    main()
