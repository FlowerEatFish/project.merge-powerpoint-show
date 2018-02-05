'''Use for TV wall'''
import os
import time
import sys
import win32com.client

def run_ppt_app():
    '''main script'''
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    # create new ppt as main
    new_ppt_name = "main-slideshow"
    # set path for all ppt
    ppt_dir = os.path.dirname(os.path.abspath(__file__))
    # create new and save ppt
    new_ppt = app.Presentations.Add()
    save_new_ppt(new_ppt, ppt_dir, new_ppt_name)
    # add slides from other ppt into main ppt
    all_ppt = collect_local_ppt_files(ppt_dir, new_ppt_name)
    for _file in all_ppt:
        path = os.path.join(ppt_dir, _file)
        temp_ppt = app.Presentations.Open(path)
        count = temp_ppt.Slides.Count
        temp_ppt.Close()
        new_ppt.Slides.InsertFromFile(path, 0, 1, count)
    # set animation for slideshow
    set_slide_animation(new_ppt)
    # save and slideshow ppt
    save_new_ppt(new_ppt, ppt_dir, new_ppt_name)
    run_slideshow(new_ppt)

def collect_local_ppt_files(dirpath, main_filename):
    '''collect PowerPoint format on current local path'''
    all_files = collect_local_all_files(dirpath)
    ppt_pool = []
    for _file in all_files:
        file_name = _file.split('.')[0]
        file_format = _file.split('.')[-1]
        if is_ppt_format(file_format) and not_main_file(file_name, main_filename):
            ppt_pool.append(_file)
    return ppt_pool

def collect_local_all_files(dirpath):
    '''collect all format on current local path'''
    all_files = os.listdir(dirpath)
    return all_files

def not_main_file(file_name, main_filename):
    '''filter main filename'''
    if not file_name.find(main_filename) != -1:
        return True
    return False
        
def is_ppt_format(file_format):
    '''filter PowerPoint files'''
    ppt_format = 'ppt'
    if file_format.find(ppt_format) != -1:
        return True
    return False

def set_slide_animation(app):
    '''set animation for slideshow'''
    count = app.Slides.Count
    for index in range(count):
        app.Slides(index+1).SlideShowTransition.EntryEffect = 3895

def run_slideshow(app):
    '''slideshow first, then run loop_slideshow function for loop'''
    app.SlideShowSettings.Run()
    loop_slideshow(app)

def loop_slideshow(app):
    '''slideshow. note: this statement is loop'''
    max_slide = app.Slides.Count
    period = 5 # second
    while True:
        for index in range(max_slide):
            app.SlideShowWindow.View.GotoSlide(index+1)
            time.sleep(period)

def save_new_ppt(app, dirpath, filename):
    '''save a ppt as main'''
    file_path = os.path.join(dirpath, filename)
    del_old_ppt(file_path)
    app.SaveAs(file_path, 1)

def del_old_ppt(file_path):
    '''check and remove old same ppt'''
    if os.path.isfile(file_path):
        os.remove(file_path)

if __name__ == '__main__':
    run_ppt_app()
