# coding: utf8

import win32api, win32con, win32gui

import os
import pathlib
from ctypes import *
from ctypes.wintypes import *

WM_PLAY = win32con.WM_USER + 100
WM_STOP = win32con.WM_USER + 101


def pwd():
    return pathlib.Path(__file__).parent.absolute()

thedll = cdll.LoadLibrary(os.path.join(pwd(), 'dhnetsdk.dll'))

################################
CLIENT_Init = thedll.CLIENT_Init
CLIENT_Init.argtypes = [c_void_p, c_longlong]
CLIENT_Init.restype = c_bool

################################
CLIENT_Cleanup = thedll.CLIENT_Cleanup
CLIENT_Cleanup.argtypes = []


################################
CLIENT_GetSDKVersion = thedll.CLIENT_GetSDKVersion
CLIENT_GetSDKVersion.argtypes = []
CLIENT_GetSDKVersion.restype = c_uint


################################
CLIENT_LoginWithHighLevelSecurity = thedll.CLIENT_LoginWithHighLevelSecurity

class NET_IN_LOGIN(Structure):
    _fields_ = [
        ('dwSize', DWORD),          #DWORD                      dwSize;             // 结构体大小
        ('szIP', c_char * 64),      #char                        szIP[64];           // IP
        ('nPort', c_int),           #int                         nPort;              // 端口
        ('szUserName', c_char*64),  #char                        szUserName[64];     // 用户名
        ('szPassword', c_char*64),  #char                        szPassword[64];     // 密码
        ('emSpecCap', c_int),       #EM_LOGIN_SPAC_CAP_TYPE      emSpecCap;          // 登录模式
        ('byReserved', c_char*4),   #BYTE                        byReserved[4];      // 字节对齐
        ('pCapParam', c_void_p),    #void*                       pCapParam;          // 见 CLIENT_LoginEx 接口 pCapParam 与 nSpecCap 关系
    ]

class NET_OUT_LOGIN(Structure):
    _fields_ = [
        ('dwSize', DWORD),          #DWORD                       dwSize;             // 结构体大小
        ('_ig', c_char*108),        #NET_DEVICEINFO_Ex           stuDeviceInfo;      // 设备信息
        ('nError', c_int),          #int                         nError;             // 错误码，见 CLIENT_Login 接口错误码
        ('byReserved', c_char*132),        #BYTE                        byReserved[132];    // 预留字段
    ]

CLIENT_LoginWithHighLevelSecurity.argtypes = [POINTER(NET_IN_LOGIN), POINTER(NET_OUT_LOGIN)]
CLIENT_LoginWithHighLevelSecurity.restype = c_longlong


################################
CLIENT_Logout = thedll.CLIENT_Logout
CLIENT_Logout.argtypes = [c_longlong]
CLIENT_Logout.restype = c_bool

################################
CLIENT_RealPlayEx = thedll.CLIENT_RealPlayEx
CLIENT_RealPlayEx.argtypes = [c_longlong, c_int, HWND, c_int]
CLIENT_RealPlayEx.restype = c_longlong


################################
CLIENT_StopRealPlayEx = thedll.CLIENT_StopRealPlayEx
CLIENT_StopRealPlayEx.argtypes = [c_longlong]
CLIENT_StopRealPlayEx.restype = c_bool


################################
CLIENT_AdjustFluency = thedll.CLIENT_AdjustFluency
CLIENT_AdjustFluency.argtypes = [c_longlong, c_int]
CLIENT_AdjustFluency.restype = c_bool


################################
CLIENT_SetMaxFlux = thedll.CLIENT_SetMaxFlux
CLIENT_SetMaxFlux.argtypes = [c_longlong, WORD]
CLIENT_SetMaxFlux.restype = c_bool


class VideoPlayer:
    def __init__(self):
        self.loginID = None
        self.playID = None
        
    def init(self):
        if self.loginID:
            return True
            
        ret = CLIENT_Init(None, 0)
        if not ret:
            print('Init error')
            return False

        inParam = NET_IN_LOGIN()
        inParam.dwSize = ctypes.sizeof(NET_IN_LOGIN)
        inParam.szIP = b'10.0.110.253'
        inParam.nPort = 37777
        inParam.szUserName = b'ax'
        inParam.szPassword = b'koalax@001'
        inParam.emSpecCap = 0


        outParam = NET_OUT_LOGIN()
        outParam.dwSize = ctypes.sizeof(NET_OUT_LOGIN)

        self.loginID = CLIENT_LoginWithHighLevelSecurity(byref(inParam), byref(outParam))
        if not self.loginID:
            print('login err', outParam.nError)
            return False
        return True
        
    def clear(self):
        if self.playID:
            self.stop()
        if self.loginID:
            CLIENT_Logout(self.loginID)
            self.loginID = None
            
        CLIENT_Cleanup()
        
    def play(self, hwnd):
        if not self.loginID:
            if not self.init():
                return
            
        #~ CLIENT_SetMaxFlux(self.loginID, 10)
        self.playID = CLIENT_RealPlayEx(self.loginID, 0, hwnd, 3)
        if not self.playID:
            print("CLIENT_RealPlayEx err")
            self.clear()
            # quit
            win32gui.PostMessage(hwnd, win32con.WM_QUIT, 0, 0)
            return
            
            
        if self.playID:
            CLIENT_AdjustFluency(self.playID, 0)
        
    def stop(self):
        if self.playID:
            CLIENT_StopRealPlayEx(self.playID)
            self.playID = None


class MyWindow:
    def __init__(self):
        win32gui.InitCommonControls()
        self.hinst = win32api.GetModuleHandle(None)
        className = 'VideoEyeWndClass'
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
            
            WM_PLAY: self.OnPlay,
            WM_STOP: self.OnStop,
            
            # test
            win32con.WM_LBUTTONDOWN: self.OnPlay,
            win32con.WM_RBUTTONDOWN: self.OnStop,
        }
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_map
        wc.lpszClassName = className
        win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPEDWINDOW
        self.hwnd = win32gui.CreateWindow(
            className,
            'VideoStream',
            style,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            640,
            480,
            0,
            0,
            self.hinst,
            None
        )
        win32gui.UpdateWindow(self.hwnd)
        win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)
        
        self.player = VideoPlayer()

    def OnDestroy(self, hwnd, message, wparam, lparam):
        print('OnDestroy')
        
        self.player.clear()

        win32gui.PostQuitMessage(0)
        return True

    def OnPlay(self, hwnd, message, wparam, lparam):
        self.player.play(self.hwnd)

        return True
        
    def OnStop(self, hwnd, message, wparam, lparam):
        self.player.stop()

        return True


if __name__ == '__main__':
    w = MyWindow()
    win32gui.PumpMessages()

