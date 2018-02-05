'''Use for TV wall'''
import os
import time
import win32com.client

def run_ppt_app():
    '''main script'''
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    # create new ppt as main
    new_ppt_name = "main.pptx"
    # set path for all ppt
    ppt_dir = os.path.dirname(os.path.abspath(__file__))
    # create new and save ppt
    new_ppt = app.Presentations.Add()
    save_new_ppt(new_ppt, ppt_dir, new_ppt_name)
    run_slideshow(new_ppt)

def run_slideshow(app):
    app.SlideShowSettings.Run()
    loop_slideshow(app)

def loop_slideshow(app):
    '''slide show. note: this statement is loop'''
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
