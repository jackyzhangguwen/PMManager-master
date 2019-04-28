#coding:utf-8
import psutil
import wx
import idDefine as gen


class SysInfo(object):
    # def __init__(self,looptime):
    #     self.looptime = looptime
    def getCPUstate(self,interval=1):
        if gen.CPU_MON is True:
            gen.CPU = str(" CPU: " + str(psutil.cpu_percent(interval)) + "%")
        else:
            gen.CPU = ""
        wx.CallLater(gen.CPU_LOOP_TIME,self.getCPUstate)

    def getMemorystate(self):
        if gen.MEMORY_MON is True:
            # phymem = psutil.phymem_usage()
            # buffers = getattr(psutil, 'phymem_buffers', lambda: 0)()
            # cached = getattr(psutil, 'cached_phymem', lambda: 0)()
            # used = phymem.total - (phymem.free + buffers + cached)
            # line = u" 内存: %5s%% %6s/%s" % (
            # phymem.percent,
            # str(int(used / 1024 / 1024)) + "M",
            # str(int(phymem.total / 1024 / 1024)) + "M"
            # )

            info = psutil.virtual_memory()
            line = u'总内存：%s 内存占比：%s' % (
            info.total,
            info.percent)

            gen.MEMORY = line
        else:
            gen.MEMORY = ""
        wx.CallLater(gen.MEMORY_LOOP_TIME,self.getMemorystate)