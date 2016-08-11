from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time

# Class
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

# ##############################################################################
# ########## Libraries #############
# ##################################
# standard library
import logging
from os import path
from time import sleep

# 3rd party modules
from win32api import GetModuleHandle, PostQuitMessage
from win32con import CW_USEDEFAULT, IMAGE_ICON, IDI_APPLICATION,\
                     LR_DEFAULTSIZE, LR_LOADFROMFILE,\
                     WM_DESTROY, WS_OVERLAPPED, WS_SYSMENU, WM_USER
from win32gui import CreateWindow, DestroyWindow, LoadIcon, LoadImage,\
                     NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP,\
                     NIM_ADD, NIM_DELETE, NIM_MODIFY,\
                     RegisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

# ############################################################################
# ######### Main program ###########
# ##################################


class WindowsBalloonTip:
    """Create a Windows 10 notification balloon.

    from: https://github.com/jithurjacob/Windows-10-Toast-Notifications
    """

    def __init__(self):
        message_map = { win32con.WM_DESTROY: self.OnDestroy,}
        """Initialize."""
        message_map = {WM_DESTROY: self.on_destroy, }

        # Register the window class.
        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = 'PythonTaskbar'
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        wc.lpszClassName = str("PythonTaskbar")  # must be a string
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        self.classAtom = RegisterClass(wc)

                    
    def balloon_tip(self, title="Notification", msg="Here comes the message",
                    icon_path=None, duration=5):
        """Notification settings.

        :title: notification title
        :msg: notification message
        :icon_path: path to the .ico file to custom notification
        :duration: delay in seconds before notification self-destruction
        """
        style = WS_OVERLAPPED | WS_SYSMENU
        self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                                 0, 0, CW_USEDEFAULT,
                                 CW_USEDEFAULT,
                                 0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

    def balloon_tip(self,title, msg):
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = CreateWindow(self.classAtom, "Taskbar",style, 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 0, 0, self.hinst, None)
        UpdateWindow(hwnd)

        hicon = LoadIcon(0, win32con.IDI_APPLICATION)

        flags =NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (hwnd, 0, flags, win32con.WM_USER+20, hicon, 'Tooltip')
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (hwnd, 0, NIF_INFO, win32con.WM_USER+20, hicon, 'Balloon Tooltip', msg, 200, title,NIIF_INFO))
        
        time.sleep(1)   
        return None

    
# Main
if __name__ == '__main__':
# ###############################################################################
# ###### Stand alone program ########
# ###################################
if __name__ == "__main__":
    # Example
    w=WindowsBalloonTip()
    w.balloon_tip('Isogeo', '10 nouvelles data depuis la derniere execution')
    # w.balloon_tip('Example two', 'Once you start coding in Python you will hate other languages')
