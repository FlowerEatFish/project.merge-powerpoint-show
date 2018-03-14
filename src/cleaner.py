'''Use for cleaning files'''
import datetime
import json
import os
import time


class Cleaner():
    '''Run cleaner'''
    def __init__(self):
        # fetch config.json
        self.database = self.fetch_data()
        # collect value and key for all ppt files
        file_list = self.set_file_list(path=self.database["path"])
        # run cleaner
        self.run_cleaner(file_list)

    @staticmethod
    def fetch_data():
        '''Load config data from external file config.json'''
        local_directory = os.path.dirname(os.path.abspath(__file__))
        database_name = "config.json"
        database_path = os.path.join(local_directory, database_name)
        result = json.load(open(database_path))
        return result

    def set_file_list(self, path):
        '''Set value for file dict'''
        ppt_file_pool = self.parser_local_ppt(path)
        file_list = []
        for ppt_file in ppt_file_pool:
            file_path = os.path.join(path, ppt_file)
            file_dict = {}
            file_dict["path"] = file_path
            file_dict["is_expired"] = self.is_expired(file_path)
            file_dict["mtime"] = os.path.getmtime(file_path)
            file_list.append(file_dict)
        return file_list

    def is_expired(self, path):
        '''Check whether file is expired'''
        set_expiration_date = self.database["expiration-date"]
        set_expiration_time = set_expiration_date * 24 * 60 * 60
        now_time = self.get_now_time()
        file_mtime = os.path.getmtime(path)
        if now_time - set_expiration_time > file_mtime:
            return True
        return False

    @staticmethod
    def get_now_time():
        '''Get now time from computer'''
        now_date = datetime.datetime.now()
        now_time = int(time.mktime(now_date.timetuple()))
        return now_time

    def run_cleaner(self, file_list):
        '''Run clean mode'''
        keep_num = self.database["keep-file"]
        not_expired_num = self.get_not_expired_number(file_list)
        total_num = len(file_list)
        if not_expired_num > keep_num:
            print("Run del_expired_file method.")
            self.del_expired_file(file_list)
        elif total_num > keep_num:
            print("Run del_excess_file method.")
            self.del_excess_file(file_list)
        else:
            print("No cleaner is needed.")

    @staticmethod
    def get_not_expired_number(file_list):
        '''Get expired number for clean mode'''
        not_expired_num = 0
        for file_dict in file_list:
            if not file_dict["is_expired"]:
                not_expired_num = not_expired_num + 1
        return not_expired_num

    @staticmethod
    def del_expired_file(file_list):
        '''Remove expired file'''
        for file_dict in file_list:
            if file_dict["is_expired"]:
                os.remove(file_dict["path"])

    def del_excess_file(self, file_list):
        '''Remove excess file'''
        file_list = self.sort_file(file_list)
        keep_num = self.database["keep-file"]
        for file_dict in file_list[keep_num:]:
            os.remove(file_dict["path"])

    @staticmethod
    def sort_file(file_list, sort_type="mtime"):
        '''Sort file'''
        files = file_list
        for i in range(len(files)-1):
            no_change = True
            for j in range(len(files)-1-i):
                if files[j][sort_type] < files[j+1][sort_type]:
                    no_change = False
                    files[j], files[j+1] = files[j+1], files[j]
            if no_change:
                break
        return files

    def parser_local_ppt(self, path):
        '''Collect PowerPoint files from local path'''
        all_file = self.collect_all_local_files(path)
        ppt_path_pool = []
        for _file in all_file:
            _format = _file.split('.')[-1]
            if self.is_ppt_format(_format):
                if self.not_main_file(_file):
                    ppt_path_pool.append("%s" % (_file))
        return ppt_path_pool

    @staticmethod
    def collect_all_local_files(path):
        '''Collect files with all format from local path'''
        all_file = os.listdir(path)
        return all_file

    @staticmethod
    def is_ppt_format(file_format):
        '''Filter PowerPoint files'''
        ppt_format = 'ppt'
        if file_format.find(ppt_format) != -1:
            return True
        return False

    @staticmethod
    def not_main_file(filename):
        '''filter main filename'''
        main_filename = "main-slide"
        if filename.find(main_filename) != -1:
            return False
        return True

if __name__ == '__main__':
    Cleaner()
