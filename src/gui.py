'''Construction of UI and events'''
import json
import os
import threading
import time
import wx
from cleaner import Cleaner
from slideshow import SlideShow


class MainWindow(wx.Frame):
    '''Render main window and control center'''
    thread_state = True

    def __init__(self, parent=None, title="電視牆輪播程式"):
        # super(MainWindow, self).__init__(parent, title=title)
        wx.Frame.__init__(self, parent, title=title,
                          style=wx.SYSTEM_MENU | wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX)
        self.set_icon()
        self.database = self.fetch_data()
        self.initial_ui(self.database)
        self.Centre()
        self.Show()
        if self.is_autorun():
            self.start_to_run_thread()

    @staticmethod
    def fetch_data():
        '''Load config data from external file config.json'''
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        result = json.load(open(database_path))
        return result

    def set_icon(self):
        '''Set icon for GUI'''
        icon_path = os.path.dirname(os.path.abspath(__file__))
        icon_name = "icon.ico"
        path = os.path.join(icon_path, icon_name)
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

    def initial_ui(self, database):
        '''Render all UI and events such as buttons, texts, etc'''
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        sizer1 = wx.GridBagSizer(5, 7)

        line = wx.StaticLine(self)
        sizer1.Add(line, pos=(0, 0), span=(1, 5),
                   flag=wx.EXPAND | wx.ALIGN_CENTER, border=5)

        # 路徑設置區
        text1 = wx.StaticText(self, label="資料夾路徑：")
        sizer1.Add(text1, pos=(1, 0), span=(1, 1),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.button1 = wx.Button(self, label="設置路徑")
        self.button1.Bind(wx.EVT_BUTTON, self.on_select_dir)
        sizer1.Add(self.button1, pos=(1, 4),
                   flag=wx.EXPAND | wx.RIGHT, border=5)
        
        self.text2 = wx.StaticText(self, label=database['path'])
        sizer1.Add(self.text2, pos=(2, 0), span=(1, 4),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        # 運行設置區
        text3 = wx.StaticText(self, label="幾秒後開始運行程式：")
        sizer1.Add(text3, pos=(3, 0), span=(1, 2),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text4 = wx.StaticText(self, label=str(database['start-time']))
        sizer1.Add(self.text4, pos=(3, 2), span=(1, 2),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.button2 = wx.Button(self, label="設置時間")
        self.button2.Bind(wx.EVT_BUTTON, self.on_set_start_time)
        sizer1.Add(self.button2, pos=(3, 4),
                   flag=wx.EXPAND | wx.RIGHT, border=5)

        # 播放設置區
        text5 = wx.StaticText(self, label="每隔幾秒後播放下一張投影片：")
        sizer1.Add(text5, pos=(4, 0), span=(1, 2),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text6 = wx.StaticText(self, label=str(database['duration']))
        sizer1.Add(self.text6, pos=(4, 2), span=(1, 2),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.button3 = wx.Button(self, label="設置時間")
        self.button3.Bind(wx.EVT_BUTTON, self.on_set_duration)
        sizer1.Add(self.button3, pos=(4, 4),
                   flag=wx.EXPAND | wx.RIGHT, border=5)

        # 其他選項區
        sb1 = wx.StaticBox(self, label="其他功能", style=wx.ALIGN_CENTER)
        boxsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, label="開啟程式後，自動播放投影片。")
        if database['auto-run']:
            checkbox1.SetValue(True)
        checkbox1.Bind(wx.EVT_CHECKBOX, self.autorun_on_checked)
        boxsizer1.Add(checkbox1, flag=wx.LEFT, border=5)

        self.checkbox2 = wx.CheckBox(self, label="啟用清理功能。（播放投影片前，先清理過期的檔案。）")
        if database['clean-run']:
            self.checkbox2.SetValue(True)
        self.checkbox2.Bind(wx.EVT_CHECKBOX, self.clean_on_checked)
        boxsizer1.Add(self.checkbox2, flag=wx.LEFT, border=5)

        sizer1.Add(boxsizer1, pos=(5, 0), span=(1, 5),
                   flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        # 清理選項區
        sb2 = wx.StaticBox(self, label="清理功能", style=wx.ALIGN_CENTER)
        boxsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)

        sizer2 = wx.GridBagSizer(2, 5)
        boxsizer2.Add(sizer2)

        text7 = wx.StaticText(self, label="刪除超過幾天的檔案：")
        sizer2.Add(text7, pos=(0, 0), span=(1, 2),
                   flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.text8 = wx.StaticText(self,
                                   label=str(database['expiration-date']))
        sizer2.Add(self.text8, pos=(0, 2), span=(1, 1),
                   flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.button4 = wx.Button(self, label="設置時間")
        self.button4.Bind(wx.EVT_BUTTON, self.on_set_expiration_date)
        if not database['clean-run']:
            self.button4.Disable()
        sizer2.Add(self.button4, pos=(0, 4),
                   flag=wx.EXPAND | wx.BOTTOM, border=5)

        text9 = wx.StaticText(self, label="如果全部檔案已過期，保留幾個最近建立的檔案：")
        sizer2.Add(text9, pos=(1, 0), span=(1, 2),
                   flag=wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL,
                   border=5)
        self.text10 = wx.StaticText(self, label=str(database['keep-file']))
        sizer2.Add(self.text10, pos=(1, 2), span=(1, 2),
                   flag=wx.LEFT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL,
                   border=5)
        self.button5 = wx.Button(self, label="設置數量")
        self.button5.Bind(wx.EVT_BUTTON, self.on_set_amount_of_keep_file)
        if not database['clean-run']:
            self.button5.Disable()
        sizer2.Add(self.button5, pos=(1, 4),
                   flag=wx.EXPAND | wx.BOTTOM, border=5)

        sizer1.Add(boxsizer2, pos=(6, 0), span=(1, 5),
                   flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)

        self.button6 = wx.Button(self, label="開始運行")
        sizer1.Add(self.button6, pos=(7, 0), flag=wx.ALL | wx.EXPAND, border=5)
        self.button6.Bind(wx.EVT_BUTTON, self.on_run)

        self.button7 = wx.Button(self, label="停止運行")
        sizer1.Add(self.button7, pos=(7, 1), flag=wx.ALL | wx.EXPAND, border=5)
        self.button7.Disable()
        self.button7.Bind(wx.EVT_BUTTON, self.on_stop)

        button8 = wx.Button(self, label="關閉程式")
        button8.Bind(wx.EVT_BUTTON, self.on_quit)
        sizer1.Add(button8, pos=(7, 4), flag=wx.ALL | wx.EXPAND, border=5)

        text10 = wx.StaticText(
            self, label="[ Repositoy ] https://github.com/FlowerEatFish/project.tv-wall")
        sizer1.Add(text10, pos=(8, 0), span=(1, 4),
                   flag=wx.ALIGN_LEFT | wx.ALL, border=5)

        text11 = wx.StaticText(
            self, label="[ Version ] 1.0")
        sizer1.Add(text11, pos=(8, 4), span=(1, 1),
                   flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        sizer1.Fit(self)
        self.SetSizer(sizer1)

    def is_autorun(self):
        '''Return bool for autorun'''
        if self.database['auto-run']:
            return True
        return False

    def on_select_dir(self, event):
        '''An event for setting directory of loading PowerPoints'''
        dlg = wx.DirDialog(None, "選擇目標資料夾", "",
                           style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            self.database['path'] = filepath
            self.text2.Label = self.database['path']
            self.update_and_save_database()
        else:
            return

    def on_set_start_time(self, event):
        '''An event for setting delay before run sldieshow'''
        min_range = 5
        max_range = 3600
        dlg = SettingWindow(self, title="幾秒後開始運行程式",
                            min_range=min_range, max_range=max_range, unit="秒")
        setting = dlg.ShowModal()
        if setting == wx.ID_OK:
            value = dlg.textctrl1.GetValue()
            if self.num_is_valid(value=value, min_range=min_range,
                                 max_range=max_range):
                self.database['start-time'] = int(dlg.textctrl1.GetValue())
                self.text4.Label = str(self.database['start-time'])
                self.update_and_save_database()
        dlg.Destroy()

    def on_set_duration(self, event):
        '''An event for setting duration of sldieshow'''
        min_range = 5
        max_range = 3600
        dlg = SettingWindow(self, title="每隔幾秒後播放下一張投影片",
                            min_range=min_range, max_range=max_range, unit="秒")
        setting = dlg.ShowModal()
        if setting == wx.ID_OK:
            value = dlg.textctrl1.GetValue()
            if self.num_is_valid(value=value, min_range=min_range,
                                 max_range=max_range):
                int(dlg.textctrl1.GetValue())
                self.database['duration'] = int(dlg.textctrl1.GetValue())
                self.text6.Label = str(self.database['duration'])
                self.update_and_save_database()
        dlg.Destroy()

    def on_set_expiration_date(self, event):
        '''An event for setting when will files be deleted after thry are
           created'''
        min_range = 1
        max_range = 365
        dlg = SettingWindow(self, title="刪除超過幾天的檔案",
                            min_range=min_range, max_range=max_range, unit="天")
        setting = dlg.ShowModal()
        if setting == wx.ID_OK:
            value = dlg.textctrl1.GetValue()
            if self.num_is_valid(value=value, min_range=min_range,
                                 max_range=max_range):
                self.database['expiration-date'] = int(value)
                self.text8.Label = str(self.database['expiration-date'])
                self.update_and_save_database()
        dlg.Destroy()

    def on_set_amount_of_keep_file(self, event):
        '''An event for setting how many files to keep'''
        min_range = 0
        max_range = 100
        dlg = SettingWindow(self, title="保留幾個最近建立的檔案",
                            min_range=min_range, max_range=max_range, unit="個")
        setting = dlg.ShowModal()
        if setting == wx.ID_OK:
            value = dlg.textctrl1.GetValue()
            if self.num_is_valid(value=value, min_range=min_range,
                                 max_range=max_range):
                self.database['keep-file'] = int(value)
                self.text10.Label = str(self.database['keep-file'])
                self.update_and_save_database()
        dlg.Destroy()

    def num_is_valid(self, value, min_range, max_range):
        '''Check whether the value user entered is valid'''
        if not self.is_int(value):
            self.warn_dialog("無效數字")
            return False
        if min_range > int(value):
            self.warn_dialog("數字過小")
            return False
        if max_range < int(value):
            self.warn_dialog("數字過大")
            return False
        return True

    def is_int(self, value):
        '''Use exception method to check whether value is int'''
        try:
            int(value)
            return True
        except:
            return False

    def warn_dialog(self, text):
        wx.MessageBox(text, '錯誤', wx.OK | wx.ICON_ERROR)

    def autorun_on_checked(self, event):
        '''An event for setting whether the program immediately run
           slideshow after run it'''
        self.database['auto-run'] = False
        result = event.GetEventObject()
        if result.GetValue():
            self.database['auto-run'] = True
        self.update_and_save_database()

    def clean_on_checked(self, event):
        '''An event for setting whether clean mode is available'''
        self.database['clean-run'] = False
        self.button4.Disable()
        self.button5.Disable()
        result = event.GetEventObject()
        if result.GetValue():
            self.database['clean-run'] = True
            self.button4.Enable()
            self.button5.Enable()
        self.update_and_save_database()

    def on_quit(self, event):
        '''An event for exiting program when it is closed'''
        self.Destroy()

    def on_run(self, event):
        '''An event it the program is ready to run slideshow'''
        self.start_to_run_thread()

    def set_button_on_run(self):
        '''Set the states of buttons when program is running'''
        self.button1.Disable()
        self.button2.Disable()
        self.button3.Disable()
        self.checkbox2.Disable()
        self.button4.Disable()
        self.button5.Disable()
        self.button6.Disable()
        self.button7.Enable()

    def set_button_on_stop(self):
        '''Set the states of buttons when program stop'''
        self.button1.Enable()
        self.button2.Enable()
        self.button3.Enable()
        self.checkbox2.Enable()
        if self.database['clean-run']:
            self.button4.Enable()
            self.button5.Enable()
        self.button6.Enable()
        self.button7.Disable()

    def start_to_run_thread(self):
        '''Create a thread for activating stop button'''
        self.set_button_on_run()
        thread = threading.Thread(target=self.run_in_thread)
        thread.start()

    def run_in_thread(self):
        '''A flow during running'''
        run_on_once = True
        count = self.database['start-time']
        self.thread_state = True
        while self.thread_state:
            if count > 0:
                self.button6.Label = "%s %s" % (str(count), "秒後開始")
                count = count - 1
                time.sleep(1)
            else:
                self.button6.Label = "運行中"
                if run_on_once:
                    thread = threading.Thread(target=self.run_slide)
                    thread.start()
                    run_on_once = False
        self.button6.Label = "開始運行"
        self.set_button_on_stop()

    def run_slide(self):
        '''Run slideshow by slideshow.py'''
        try:
            if self.database['clean-run']:
                Cleaner()
            SlideShow()
        except:
            self.warn_dialog(text="請先關閉 PowerPoint 再運行程式。")
        finally:
            self.thread_state = False

    def on_stop(self, event):
        '''An event it the program stop slideshow'''
        self.thread_state = False

    def update_and_save_database(self):
        '''Save config data to external file config.json'''
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        with open(database_path, 'w') as outfile:
            json.dump(self.database, outfile)


class SettingWindow(wx.Dialog):
    '''A pop-up window for setting parameter'''
    def __init__(self, parent, title="設定",
                 min_range=5, max_range=100, unit=None):
        # super(SettingWindow, self).__init__(parent, title=title)
        wx.Dialog.__init__(self, parent, title=title)
        self.initial_ui(min_range=min_range, max_range=max_range, unit=unit)
        self.Centre()
        self.Show()

    def initial_ui(self, min_range, max_range, unit):
        '''Render all UI such as buttons, texts, etc, but no event is setted'''
        sizer1 = wx.GridBagSizer(2, 3)

        text = "設定數值： (%d~%d %s)" % (min_range, max_range, unit)
        text1 = wx.StaticText(self, label=text)
        sizer1.Add(text1, pos=(0, 0), span=(1, 1),
                   flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.textctrl1 = wx.TextCtrl(self)
        sizer1.Add(self.textctrl1, pos=(0, 1), span=(1, 2),
                   flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
                   border=5)

        button1 = wx.Button(self, id=wx.ID_OK, label="提交")
        sizer1.Add(button1, pos=(1, 0), span=(1, 1),
                   flag=wx.ALL | wx.EXPAND, border=5)

        button2 = wx.Button(self, id=wx.ID_CANCEL, label="取消")
        sizer1.Add(button2, pos=(1, 2), span=(1, 1),
                   flag=wx.ALL | wx.EXPAND, border=5)

        sizer1.Fit(self)
        self.SetSizer(sizer1)

if __name__ == '__main__':
    APP = wx.App()
    MainWindow(None, title="電視牆輪播程式")
    APP.MainLoop()
