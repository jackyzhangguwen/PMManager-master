#coding:utf-8
import wx
import os
from dataList import DataHandle
import idDefine as gen
import subprocess, win32api
import win32event
import win32process
import LogOutput as LoadLog

class MonitorPro(object):
    def __init__(self, loopTime, pdata, rfobj, filename, plist):
        self.loopTime = loopTime
        self.pdata = pdata
        self.filename = filename
        self.ProgrameList = plist
        self.rf = rfobj

    def GetProcessCount(self, procName):
        procName = str(procName)
        p = os.popen('tasklist /FI "IMAGENAME eq %s"' % procName)
        return p.read().count(procName)

    def DoMonitor(self):
        if gen.IsItemChanged is True:
            rf = DataHandle(self.filename)
            self.pdata = rf.ReadData()
        gen.IsItemChanged = False
        ####获取监控中的路径列表 和 全部 kid 列表
        self.ProPathList = []
        self.ProKidList = []
        allProList = []
        monProList = []
        runProcList = []
        if self.pdata :
            for kid in self.pdata.keys():
                procPath = self.pdata[kid]["programe"]
                procNum = self.pdata[kid]["processNum"]
                proc_Argument = self.pdata[kid]["logfile"]
                Operator = gen.operatorDict[self.pdata[kid]["operator"]]
                runAs = self.pdata[kid]["runAs"]
                allProList.append(kid)
                if self.pdata[kid]["monitor"] is True:
                    monProList.append(kid)
                    procName = os.path.basename(procPath)

                    if self.GetProcessCount(procName) == 0 :
                        LoadLog.LogMsg(gen.logger.warning, u"未发现项目进程%s，启动进程%s" %(procName, procName))
                        self.StartProc(kid,procPath,proc_Argument,runAs)
                        if self.GetProcessCount(procName) == 0:
                            LoadLog.LogMsg(gen.logger.warning, u"启动进程%s失败" % procName)
                    elif self.OperatorExpress(Operator, procName, procNum):
                        runProcList.append(kid)
                        self.pdata[kid]["status"] = True
                    else:
                        LoadLog.LogMsg(gen.logger.warning, u"发现项目的%s进程不满足条件给定条件，结束%s进程" %(procName, procName))
                        self.StopProc(kid, procName)
                else:
                    self.pdata[kid]["status"] = ""

        gen.allProNum = len(allProList)
        gen.monProNum = len(monProList)
        gen.runProNum = len(runProcList)
        #self.SetStatusInformation(allProNum,monProNum,runProNum)
        list_data = self.rf.handleList(self.pdata)
        self.ProgrameList.SetObjects(list_data)

    def OperatorExpress(self, Operator, procName, procNum):
        if Operator == "=":
            return (self.GetProcessCount(procName) == procNum)
        elif Operator == "<":
            return (self.GetProcessCount(procName) < procNum)
        elif Operator == ">":
            return (self.GetProcessCount(procName) > procNum)
        elif Operator == "<=":
            return (self.GetProcessCount(procName) <= procNum)
        elif Operator == ">=":
            return (self.GetProcessCount(procName) >= procNum)
        elif Operator == "!=":
            return (self.GetProcessCount(procName) != procNum)

    def LoopDoMonitor(self):
        #print "gen.LOOP_TIME",gen.LOOP_TIME
        self.DoMonitor()
        wx.CallLater(gen.LOOP_TIME, self.LoopDoMonitor)


    def StartProc(self, kid, procPath, Arg, runAs):
        try:
            win32api.ShellExecute(0, 'open', procPath, Arg, '', runAs)
            self.pdata[kid]["status"] = True
        except:
            self.pdata[kid]["status"] = False

    def StopProc(self, kid, procName):
        try:
            subprocess.Popen("taskkill /F /im  %s" % procName , shell=True)
            self.pdata[kid]["status"] = False
        except:
            self.pdata[kid]["status"] = True

    def SetStatusInformation(self, allProcNum, monProcNum, runProcNum):
        #a = CustomStatusBar(self)
        #a.SetStatusText("aaa1",1)
        pass
