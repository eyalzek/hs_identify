import os
import win32gui
import win32ui
import win32con
import win32api
from time import sleep


class Window(object):
    """Represents an application window"""    
    def __init__(self, path, window_name):
        super(Window, self).__init__()
        self.path = path
        try:
            self.hwnd = self.get_windows_by_title("%s" %window_name)[0]
        except IndexError:
            print("%s window not found" %window_name)
            raise Exception("%s window not found" %window_name)

    def get_windows_by_title(self, title_text):
        def _window_callback(hwnd, all_windows):
            all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        windows = []
        win32gui.EnumWindows(_window_callback, windows)
        return [hwnd for hwnd, title in windows if title_text in title]

    def screenshot(self):
        l,t,r,b = win32gui.GetClientRect(self.hwnd)
        fs = False
        h = b - t
        w = r - l
        if w == 0 or h == 0: # probably means the app is in fullscreen
            w, h = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
            fs = True
        
        hDC = win32gui.GetDC(self.hwnd)
        myDC = win32ui.CreateDCFromHandle(hDC)
        newDC = myDC.CreateCompatibleDC()

        myBitMap = win32ui.CreateBitmap()
        myBitMap.CreateCompatibleBitmap(myDC, w, h)

        newDC.SelectObject(myBitMap)

        if fs:
            win32gui.ShowWindow(self.hwnd, 3)
        else:
            win32gui.SetForegroundWindow(self.hwnd)
        sleep(.2) # allow time for screen to redraw
        newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
        myBitMap.Paint(newDC)
        try:
            if not os.path.exists(os.path.dirname(self.path)):
                os.makedirs(os.path.dirname(self.path))
            myBitMap.SaveBitmapFile(newDC, self.path)
            print("file saved as: %s" %self.path)
        except IOError:
            print("file failed to save")
        except OSError:
            print("failed to create folder: %s" %os.path.dirname(self.path))
