import win32serviceutil
import win32service
import win32event
import servicemanager
import win32api
import win32con
import win32service

class MyPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "deepserach"
    _svc_display_name_ = "Deep Search File Monitoring "

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Service is starting...")
        self.main()

    def main(self):
        while self.running:
            # Your logic here
            time.sleep(5)

    @staticmethod
    def install_auto_start():
        # Automatically sets service to start on boot
        import win32serviceutil
        win32serviceutil.InstallService(
            PythonServiceFramework._svc_name_,
            MyPythonService._svc_display_name_,
            MyPythonService._svc_name_,
            startType=win32service.SERVICE_AUTO_START
        )

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyPythonService)
