#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(600, 340))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        sizer1 = wx.GridBagSizer(5, 5)

        line = wx.StaticLine(panel)
        sizer1.Add(line, pos=(0, 0), span=(1, 5), flag=wx.EXPAND | wx.ALIGN_CENTER, border=5)

        # 路徑設置區
        text1 = wx.StaticText(panel, label="資料夾路徑：")
        sizer1.Add(text1, pos=(1, 0), span=(1, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        text2 = wx.StaticText(panel, label="未設置")
        sizer1.Add(text2, pos=(1, 1), span=(1, 3), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        button1 = wx.Button(panel, label="設置路徑")
        sizer1.Add(button1, pos=(1, 4), flag=wx.EXPAND | wx.RIGHT, border=5)

        # 運行設置區
        text3 = wx.StaticText(panel, label="幾秒後開始運行程式：")
        sizer1.Add(text3, pos=(2, 0), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        text4 = wx.StaticText(panel, label="未設置")
        sizer1.Add(text4, pos=(2, 2), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        button2 = wx.Button(panel, label="設置時間")
        sizer1.Add(button2, pos=(2, 4), flag=wx.EXPAND | wx.RIGHT, border=5)

        # 播放設置區
        text5 = wx.StaticText(panel, label="幾秒後播放下一張投影片：")
        sizer1.Add(text5, pos=(3, 0), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        text6 = wx.StaticText(panel, label="未設置")
        sizer1.Add(text6, pos=(3, 2), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        button3 = wx.Button(panel, label="設置時間")
        sizer1.Add(button3, pos=(3, 4), flag=wx.EXPAND | wx.RIGHT, border=5)

        # 其他選項區
        sb1 = wx.StaticBox(panel, label="其他功能", style=wx.ALIGN_CENTER)
        boxsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)
        boxsizer1.Add(wx.CheckBox(panel, label="開啟程式後，自動播放投影片。"), flag=wx.LEFT, border=5)
        boxsizer1.Add(wx.CheckBox(panel, label="啟用清理功能。（播放投影片前，先清理過期的檔案。）"), flag=wx.LEFT, border=5)
        sizer1.Add(boxsizer1, pos=(4, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        # 清理選項區
        sb2 = wx.StaticBox(panel, label="清理功能", style=wx.ALIGN_CENTER)
        boxsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)

        sizer2 = wx.GridBagSizer(2, 5)
        boxsizer2.Add(sizer2)

        text7 = wx.StaticText(panel, label="刪除超過幾天的檔案：")
        sizer2.Add(text7, pos=(0, 0), span=(1, 2), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        text8 = wx.StaticText(panel, label="未設置")
        sizer2.Add(text8, pos=(0, 2), span=(1, 2), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        button4 = wx.Button(panel, label="設置時間")
        sizer2.Add(button4, pos=(0, 4), flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, border=5)

        text9 = wx.StaticText(panel, label="保留幾個最近建立的檔案：")
        sizer2.Add(text9, pos=(1, 0), span=(1, 2), flag=wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        text10 = wx.StaticText(panel, label="未設置")
        sizer2.Add(text10, pos=(1, 2), span=(1, 2), flag=wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        button5 = wx.Button(panel, label="設置數量")
        sizer2.Add(button5, pos=(1, 4), flag=wx.EXPAND | wx.BOTTOM | wx.RIGHT, border=5)
        
        sizer2.AddGrowableCol(2)

        sizer1.Add(boxsizer2, pos=(5, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        button6 = wx.Button(panel, label="開始運行")
        sizer1.Add(button6, pos=(6, 0), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=5)

        button7 = wx.Button(panel, label="停止運行")
        sizer1.Add(button7, pos=(6, 1), flag=wx.EXPAND | wx.TOP, border=5)

        button8 = wx.Button(panel, label="關閉程式")
        sizer1.Add(button8, pos=(6, 4), flag=wx.EXPAND | wx.TOP | wx.RIGHT, border=5)

        sizer1.AddGrowableCol(2, 1)
        panel.SetSizer(sizer1)

if __name__ == '__main__':
    app = wx.App()
    Example(None, title="電視牆輪播程式")
    app.MainLoop()
