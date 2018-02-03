'''Use for TV wall'''
import os
import win32com.client

def run_ppt_app():
    '''main script'''
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True

    # create new ppt
    new_ppt_file = 'main.pptx'
    # set path for all ppt
    ppt_dir = os.path.dirname(os.path.abspath(__file__))

    # create new and save ppt
    new_ppt = app.Presentations.Add()
    save_new_ppt(app, ppt_dir, new_ppt_file)

    app.Quit()

def save_new_ppt(app, dirpath, filename):
    '''save a ppt as main'''
    del_old_ppt(dirpath, filename)
    app.SaveAs(filename, 12)

def del_old_ppt(dirpath, filename):
    '''check and remove old same ppt'''
    file_path = os.path.join(dirpath, filename)
    print('file_path: ', file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)

if __name__ == '__main__':
    run_ppt_app()
