'''Use for TV wall'''
import json
import os
import time
import sys
import win32com.client


class SlideShow():
    '''Run slideshow'''
    def __init__(self):
        self.database = self.fetch_data()
        self.run_ppt_app()

    @staticmethod
    def fetch_data():
        '''Load config data from external file config.json'''
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        result = json.load(open(database_path))
        return result

    def run_ppt_app(self):
        '''main script'''
        app = win32com.client.Dispatch("PowerPoint.Application")
        app.Visible = True
        name = self.set_main_ppt_name("main-slide")
        path = self.set_main_ppt_path(
            os.path.dirname(os.path.abspath(__file__)))
        # create new and save ppt
        new_ppt = app.Presentations.Add()
        self.save_new_ppt(new_ppt, path, name)
        # add slides from other ppt into main ppt
        all_ppt = self.collect_local_ppt(
            self.database["path"], name)
        for _file in all_ppt:
            path = os.path.join(path, _file)
            temp_ppt = app.Presentations.Open(path)
            count = temp_ppt.Slides.Count
            temp_ppt.Close()
            new_ppt.Slides.InsertFromFile(path, 0, 1, count)
        # set animation for slideshow
        self.set_slide_animation(new_ppt)
        # save and slideshow ppt
        self.save_new_ppt(new_ppt, path, name)
        self.run_slideshow(
            new_ppt, duration=self.database["duration"])

    @staticmethod
    def set_main_ppt_name(text):
        '''Set filename for main ppt'''
        text = text + ".pptx"
        return text

    @staticmethod
    def set_main_ppt_path(path):
        '''Set path for saving main ppt'''
        return path

    def collect_local_ppt(self, path, main_filename):
        '''collect PowerPoint format on current local path'''
        all_files = self.collect_local_all_files(path)
        ppt_pool = []
        for _file in all_files:
            name = _file.split('.')[0]
            _format = _file.split('.')[-1]
            if self.is_ppt_format(_format):
                if self.not_main_file(name, main_filename):
                    ppt_pool.append(_file)
        return ppt_pool

    @staticmethod
    def collect_local_all_files(path):
        '''collect all format on current local path'''
        all_files = os.listdir(path)
        return all_files

    @staticmethod
    def not_main_file(filename, main_filename):
        '''filter main filename'''
        if not filename.find(main_filename) != -1:
            return True
        return False

    @staticmethod
    def is_ppt_format(file_format):
        '''filter PowerPoint files'''
        ppt_format = 'ppt'
        if file_format.find(ppt_format) != -1:
            return True
        return False

    @staticmethod
    def set_slide_animation(app):
        '''set animation for slideshow'''
        count = app.Slides.Count
        for index in range(count):
            app.Slides(index+1).SlideShowTransition.EntryEffect = 3895

    def run_slideshow(self, app, duration):
        '''slideshow first, then run loop_slideshow function for loop'''
        app.SlideShowSettings.Run()
        self.loop_slideshow(app, duration)

    @staticmethod
    def loop_slideshow(app, duration):
        '''slideshow. note: this statement is loop'''
        max_slide = app.Slides.Count
        period = duration
        while True:
            for index in range(max_slide):
                app.SlideShowWindow.View.GotoSlide(index+1)
                time.sleep(period)

    def save_new_ppt(self, app, path, name):
        '''save a ppt as main'''
        full_path = os.path.join(path, name)
        self.del_old_ppt(full_path)
        app.SaveAs(full_path, 1)

    @staticmethod
    def del_old_ppt(full_path):
        '''check and remove old same ppt'''
        if os.path.isfile(full_path):
            os.remove(full_path)

if __name__ == '__main__':
    SlideShow()