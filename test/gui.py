#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import wx

class MainWindow(wx.Dialog):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title)
        # wx.Dialog.__init__(self, parent, title=title)
        self.database = self.fetch_data()
        self.initial_ui(self.database)
        self.Centre()
        self.Show()

    def fetch_data(self):
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        result = json.load(open(database_path))
        return result

    def initial_ui(self, database):
        sizer1 = wx.GridBagSizer(5, 5)

        line = wx.StaticLine(self)
        sizer1.Add(line, pos=(0, 0), span=(1, 5), flag=wx.EXPAND | wx.ALIGN_CENTER, border=5)

        # 路徑設置區
        text1 = wx.StaticText(self, label="資料夾路徑：")
        sizer1.Add(text1, pos=(1, 0), span=(1, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text2 = wx.StaticText(self, label=database['path'])
        sizer1.Add(self.text2, pos=(1, 1), span=(1, 3), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        button1 = wx.Button(self, label="設置路徑")
        button1.Bind(wx.EVT_BUTTON, self.on_select_dir)
        sizer1.Add(button1, pos=(1, 4), flag=wx.EXPAND | wx.RIGHT, border=5)

        # 運行設置區
        text3 = wx.StaticText(self, label="幾秒後開始運行程式：")
        sizer1.Add(text3, pos=(2, 0), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text4 = wx.StaticText(self, label=str(database['start-time']))
        sizer1.Add(self.text4, pos=(2, 2), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        button2 = wx.Button(self, label="設置時間")
        button2.Bind(wx.EVT_BUTTON, self.on_set_start_time)
        sizer1.Add(button2, pos=(2, 4), flag=wx.EXPAND | wx.RIGHT, border=5)

        # 播放設置區
        text5 = wx.StaticText(self, label="每隔幾秒後播放下一張投影片：")
        sizer1.Add(text5, pos=(3, 0), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        text6 = wx.StaticText(self, label=str(database['duration']))
        sizer1.Add(text6, pos=(3, 2), span=(1, 2), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        button3 = wx.Button(self, label="設置時間")
        button3.Bind(wx.EVT_BUTTON, self.on_set_duration)
        sizer1.Add(button3, pos=(3, 4), flag=wx.EXPAND | wx.RIGHT, border=5)

        # 其他選項區
        sb1 = wx.StaticBox(self, label="其他功能", style=wx.ALIGN_CENTER)
        boxsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, label="開啟程式後，自動播放投影片。")
        if database['auto-run']:
            checkbox1.SetValue(True)
        checkbox1.Bind(wx.EVT_CHECKBOX, self.autorun_on_checked)
        boxsizer1.Add(checkbox1, flag=wx.LEFT, border=5)

        checkbox2 = wx.CheckBox(self, label="啟用清理功能。（播放投影片前，先清理過期的檔案。）")
        if database['clean-run']:
            checkbox2.SetValue(True)
        checkbox2.Bind(wx.EVT_CHECKBOX, self.clean_on_checked)
        boxsizer1.Add(checkbox2, flag=wx.LEFT, border=5)

        sizer1.Add(boxsizer1, pos=(4, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        # 清理選項區
        sb2 = wx.StaticBox(self, label="清理功能", style=wx.ALIGN_CENTER)
        boxsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)

        sizer2 = wx.GridBagSizer(2, 5)
        boxsizer2.Add(sizer2)

        text7 = wx.StaticText(self, label="刪除超過幾天的檔案：")
        sizer2.Add(text7, pos=(0, 0), span=(1, 2), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        text8 = wx.StaticText(self, label=str(database['expiration-date']))
        sizer2.Add(text8, pos=(0, 2), span=(1, 1), flag=wx.LEFT | wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.button4 = wx.Button(self, label="設置時間")
        self.button4.Bind(wx.EVT_BUTTON, self.on_set_expiration_date)
        if not database['clean-run']:
            self.button4.Disable()
        sizer2.Add(self.button4, pos=(0, 4), flag=wx.EXPAND | wx.BOTTOM, border=5)

        text9 = wx.StaticText(self, label="如果全部檔案已過期，保留幾個最近建立的檔案：")
        sizer2.Add(text9, pos=(1, 0), span=(1, 2), flag=wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        text10 = wx.StaticText(self, label=str(database['keep-file']))
        sizer2.Add(text10, pos=(1, 2), span=(1, 2), flag=wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.button5 = wx.Button(self, label="設置數量")
        self.button5.Bind(wx.EVT_BUTTON, self.on_set_amount_of_keep_file)
        if not database['clean-run']:
            self.button5.Disable()
        sizer2.Add(self.button5, pos=(1, 4), flag=wx.EXPAND | wx.BOTTOM, border=5)

        sizer1.Add(boxsizer2, pos=(5, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        self.button6 = wx.Button(self, label="開始運行")
        sizer1.Add(self.button6, pos=(6, 0), flag=wx.ALL | wx.EXPAND, border=5)
        self.button6.Bind(wx.EVT_BUTTON, self.on_run)

        self.button7 = wx.Button(self, label="停止運行")
        sizer1.Add(self.button7, pos=(6, 1), flag=wx.ALL | wx.EXPAND, border=5)
        self.button7.Disable()
        self.button7.Bind(wx.EVT_BUTTON, self.on_stop)

        button8 = wx.Button(self, label="關閉程式")
        button8.Bind(wx.EVT_BUTTON, self.on_quit)
        sizer1.Add(button8, pos=(6, 4), flag=wx.ALL | wx.EXPAND, border=5)

        sizer1.Fit(self)
        self.SetSizer(sizer1)

    def on_select_dir(self, event):
        dlg = wx.DirDialog(None, "選擇目標資料夾", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            self.database['path'] = filepath
            self.text2.Label = self.database['path']
            self.update_and_save_database()
        else:
            return

    def on_set_start_time(self, event):
        SettingWindow(self, title="幾秒後開始運行程式", min_range=5, max_range=600, unit="秒", key="start-time")

    def on_set_duration(self, event):
        SettingWindow(self, title="每隔幾秒後播放下一張投影片", min_range=5, max_range=600, unit="秒", key="duration")

    def on_set_expiration_date(self, event):
        SettingWindow(self, title="刪除超過幾天的檔案", min_range=1, max_range=180, unit="天", key="expiration-date")

    def on_set_amount_of_keep_file(self, event):
        SettingWindow(self, title="保留幾個最近建立的檔案", min_range=0, max_range=100, unit="個", key="keep-file")

    def autorun_on_checked(self, event):
        result = event.GetEventObject()
        if result.GetValue():
            self.database['auto-run'] = True
        else:
            self.database['auto-run'] = False
        self.update_and_save_database()

    def clean_on_checked(self, event):
        result = event.GetEventObject()
        if result.GetValue():
            self.database['clean-run'] = True
            self.button4.Enable()
            self.button5.Enable()
        else:
            self.database['clean-run'] = False
            self.button4.Disable()
            self.button5.Disable()
        self.update_and_save_database()

    def on_quit(self, event):
        self.Destroy()

    def on_run(self, event):
        self.button6.Disable()
        self.button7.Enable()
    
    def on_stop(self, event):
        self.button6.Enable()
        self.button7.Disable()

    def update_and_save_database(self):
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        with open(database_path, 'w') as outfile:
            json.dump(self.database, outfile)

class SettingWindow(wx.Dialog):
    def __init__(self, parent, key, title="設定", min_range=5, max_range=100, unit=None):
        super(SettingWindow, self).__init__(parent, title=title)
        # wx.Dialog.__init__(self, parent, title=title)
        self.key = key
        self.database = self.fetch_data()
        self.initial_ui(min_range=min_range, max_range=max_range, unit=unit)
        self.Centre()
        self.Show()
    
    def fetch_data(self):
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        result = json.load(open(database_path))
        return result

    def initial_ui(self, min_range, max_range, unit):
        sizer1 = wx.GridBagSizer(2, 3)

        text = "設定數值： (%d~%d %s)" %  (min_range, max_range, unit)
        text1 = wx.StaticText(self, label=text)
        sizer1.Add(text1, pos=(0, 0), span=(1, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.textctrl1 = wx.TextCtrl(self)
        sizer1.Add(self.textctrl1, pos=(0, 1), span=(1, 2), flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=5)

        button1 = wx.Button(self, label="提交")
        button1.Bind(wx.EVT_BUTTON, self.on_submit)
        sizer1.Add(button1, pos=(1, 0), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=5)

        button2 = wx.Button(self, label="取消")
        button2.Bind(wx.EVT_BUTTON, self.on_cancel)
        sizer1.Add(button2, pos=(1, 2), span=(1, 1), flag=wx.ALL | wx.EXPAND, border=5)

        sizer1.Fit(self)
        self.SetSizer(sizer1)

    def on_submit(self, event):
        key = self.key
        value = int(self.textctrl1.GetValue())
        self.database[key] = value
        self.update_and_save_database()
        self.Destroy()

    def on_cancel(self, event):
        self.Destroy()
    
    def update_and_save_database(self):
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        with open(database_path, 'w') as outfile:
            json.dump(self.database, outfile)

if __name__ == '__main__':
    app = wx.App()
    MainWindow(None, title="電視牆輪播程式")
    app.MainLoop()
