# -*- coding: UTF-8 -*-
import wx
import signal
import time
import os
from multiprocessing import Process
from server import PythonWebServer

USE_GENERIC = 0

if USE_GENERIC:
    from wx.lib.stattext import GenStaticText as StaticText
else:
    StaticText = wx.StaticText

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 250

#---------------------------------------------------------------------------

__sWebProcess=None

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

def asyncStartWebServer(start_callback, stop_callback):
    global __sWebProcess
    if __sWebProcess and __sWebProcess.is_alive():
        print "__sWebProcess is running"
        return False
    __sWebProcess = Process(target=__asyncStartWebServer, args=(start_callback, stop_callback))
    __sWebProcess.daemon = True
    __sWebProcess.start()

def __asyncStartWebServer(start_callback, stop_callback):
    PythonWebServer.addServerStartListener(start_callback)
    PythonWebServer.addServerStopedListener(stop_callback)
    PythonWebServer.startServer()

# ---------------------------------------------------------------------------

def main():
    try:
        demoPath = os.path.dirname(__file__)
        os.chdir(demoPath)
    except:
        pass
    app = Application(False)
    app.MainLoop()

#---------------------------------------------------------------------------

class Application(wx.App):
    def OnInit(self):
        self.SetAppName("Android Log Analysis Tool")

        splash = SplashScreen()
        splash.Show()

        return True

# ---------------------------------------------------------------------------

class SplashScreen(wx.SplashScreen):
    global __sWebProcess
    def __init__(self):
        bmp = wx.Image(opj("images/splash.bmp")).ConvertToBitmap()
        wx.SplashScreen.__init__(self, bmp,
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 5000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(2000, self.ShowMain)

        StaticText(
            self, -1, "Is this yellow?", (20, 70), (120, -1)
            ).SetBackgroundColour('Yellow')

        # register service callback
        asyncStartWebServer(self.__onWebServerStarted, self.__onWebServerStopped)

    def __onWebServerStarted(self):
        print "Server Started"

    def __onWebServerStopped(self, reason):
        global __sWebProcess
        print "Server stopped: ", reason
        if reason == 0x01:
            pass
        elif reason == 0x02:
            print PythonWebServer.__STOP_REASON__[reason]
            pass
        elif reason == 0x03:
            pass
        # if __sWebProcess and __sWebProcess.is_alive:
        #     print "__sWebProcess.terminate()"
        #     __sWebProcess.terminate()

    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        frame = MainWindow(None)
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()

#---------------------------------------------------------------------------

class MainWindow(wx.Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent,size=(WINDOW_WIDTH, WINDOW_HEIGHT),
                                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)#wx.CLIP_CHILDREN|wx.NO_BORDER)#wx.FRAME_NO_TASKBAR
        self.SetMinSize((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.Centre(wx.BOTH)
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)

        self.dying = False
        self.skipLoad = False

        panel = wx.Panel(self, -1, size=(100,100))
        # 基本静态的文本
        wx.StaticText(panel, wx.ID_ANY, "这是个基本的静态文本。", (100, 10))

        # 为文本指定前景色和背景色
        text = wx.StaticText(panel, wx.ID_ANY, "指定文本前景和背景色", (100, 30))
        text.SetForegroundColour("White")
        text.SetBackgroundColour("Black")

        # 指定居中对齐
        text = wx.StaticText(panel, wx.ID_ANY, "居中对齐", (100, 50), (160, -1), \
                             wx.ALIGN_CENTER)
        text.SetForegroundColour("White")
        text.SetBackgroundColour("Black")

        # 指定右对齐
        text = wx.StaticText(panel, wx.ID_ANY, "居右对齐", (100,70), (160, -1), \
                             wx.ALIGN_RIGHT)

        # 指定字体的静态文本的font
        text = wx.StaticText(panel, wx.ID_ANY, "设置文本font", (20, 100))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        text.SetFont(font)

        # 设置多行文本
        multiStr = "现在你看到\n的是多行\n文本"
        wx.StaticText(panel, wx.ID_ANY, multiStr, (20, 150))

#---------------------------------------------------------------------------
# class AppWindow(wx.Frame):
#     def __init__(self, parent):
#         super(AppWindow, self).__init__(parent,size=(WINDOW_WIDTH, WINDOW_HEIGHT),style=wx.CLIP_CHILDREN|wx.NO_BORDER)#wx.FRAME_NO_TASKBAR
#         self.__initUI()
#         self.asyncStartWebServer()
#         #self.__init_sig_handler()
#
#     # public methods
#
#     def asyncStartWebServer(self):
#         self.webProcess = Process(target=self.__asyncStartWebServer)
#         self.webProcess.daemon = True
#         self.webProcess.start()
#
#     # private methods
#
#     def __initUI(self):
#         self.Bind(wx.EVT_PAINT, self.__onPaint)
#         self.Centre()
#         self.Show(True)
#
#     def __onPaint(self, e):
#         self.Centre()
#         dc = wx.PaintDC(self)
#         bm = wx.Bitmap(WINDOW_BACKGROUND_PATH)
#         dc.DrawBitmap(bm, 0, 0, True)
#
#     def __asyncStartWebServer(self):
#         PythonWebServer.addServerStartListener(self.__onWebServerStarted)
#         PythonWebServer.addServerStopedListener(self.__onWebServerStopped)
#         PythonWebServer.startServer()
#
#     def __onWebServerStarted(self):
#         print "Server Started"
#
#     def __onWebServerStopped(self, reason):
#         print "Server stopped: ", reason
#         if reason == 0x01:
#             pass
#         elif reason == 0x02:
#             pass
#         elif reason == 0x03:
#             pass
#
#     def __init_sig_handler(self):
#         signal.signal(signal.SIGINT, self.__sig_handler)
#         signal.signal(signal.SIGABRT, self.__sig_handler)
#         signal.signal(signal.SIGALRM, self.__sig_handler)
#         signal.signal(signal.SIGBUS, self.__sig_handler)
#         signal.signal(signal.SIGCHLD, self.__sig_handler)
#         signal.signal(signal.SIGCLD, self.__sig_handler)
#         signal.signal(signal.SIGCONT, self.__sig_handler)
#         signal.signal(signal.SIGFPE, self.__sig_handler)
#         signal.signal(signal.SIGHUP, self.__sig_handler)
#         signal.signal(signal.SIGILL, self.__sig_handler)
#         signal.signal(signal.SIGIO, self.__sig_handler)
#         signal.signal(signal.SIGIOT, self.__sig_handler)
#         signal.signal(signal.SIGPIPE, self.__sig_handler)
#         signal.signal(signal.SIGPOLL, self.__sig_handler)
#         signal.signal(signal.SIGPROF, self.__sig_handler)
#         signal.signal(signal.SIGPWR, self.__sig_handler)
#         signal.signal(signal.SIGQUIT, self.__sig_handler)
#         signal.signal(signal.SIGRTMAX, self.__sig_handler)
#         signal.signal(signal.SIGRTMIN, self.__sig_handler)
#         signal.signal(signal.SIGSEGV, self.__sig_handler)
#         signal.signal(signal.SIGSYS, self.__sig_handler)
#         signal.signal(signal.SIGTERM, self.__sig_handler)
#         signal.signal(signal.SIGTRAP, self.__sig_handler)
#         signal.signal(signal.SIGTSTP, self.__sig_handler)
#         signal.signal(signal.SIGTTIN, self.__sig_handler)
#         signal.signal(signal.SIGTTOU, self.__sig_handler)
#         signal.signal(signal.SIGURG, self.__sig_handler)
#         signal.signal(signal.SIGUSR1, self.__sig_handler)
#         signal.signal(signal.SIGUSR2, self.__sig_handler)
#
#         signal.signal(signal.SIGVTALRM, self.__sig_handler)
#         signal.signal(signal.SIGWINCH, self.__sig_handler)
#         signal.signal(signal.SIGXCPU, self.__sig_handler)
#         signal.signal(signal.SIGXFSZ, self.__sig_handler)
#
#         signal.signal(signal.SIG_IGN, self.__sig_handler)
#
#     def __sig_handler(self, sig, frame):
#         try:
#             print "sig1 = ", sig, ", frame1 = ", frame
#             PythonWebServer.stopServer()
#             if sig == signal.SIGQUIT:
#                 self.webProcess.terminate()
#                 self.webProcess.join()
#         except:
#             exit(1)
#
#
if __name__ == "__main__":
    print 'current pid is %s' % os.getpid()
    main()