from flask_appbuilder import BaseView, expose
from config import UPLOAD_FOLDER
from pathlib import Path
from flask import  render_template, abort
from . import appbuilder
from datetime import datetime
from werkzeug.utils import safe_join 

class FilesListing(BaseView):

    def convert_datetimes(self, timestamps):
        dd = datetime.utcfromtimestamp(timestamps)
        formated_date = dd.strftime('%Y-%m-%d %H:%M:%S')
        return formated_date
    
    # this function is used to call the parsing
    # do the parsing and save into database
    def execute_parsing(self, reqPath):

        return 'linda'
    
    # this function will help navigates through directories
    def navigate_directory(self):
        return 'linda directory'


    @expose('/listfiles/<path:reqPath>', defaults={'reqPath': ''})
    def listfiles(self, reqPath):

        # def convert_datetimes(self, timestamps):
        #     dd = datetime.utcfromtimestamp(timestamps)
        #     formated_date = dd.strftime('%Y-%m-%d %H:%M:%S')
        #     return formated_date

        # in
        init_path = Path(UPLOAD_FOLDER)

        abs_path = safe_join(UPLOAD_FOLDER, reqPath)

        if not Path(abs_path).exists():
            return abort(404)

        files_and_dir = init_path.iterdir()

        # create a button that will call a funtion
        # for navigate through directory if the path element is 
        # a directory or execute parsing an saving if it's a file
        # file_button = self.execute_parsing() if directory_entry.is_file() else self.navigate_directory()

        # list of dictionnary containing file or dir name
        # and the last time of modification
        files_and_dir2 = [
            {
                "filename" : file.name, 
                "file_last_modified" : self.convert_datetimes(file.stat().st_mtime),
                "button" : self.execute_parsing() if file.is_file() else self.navigate_directory()
            } for file in  files_and_dir
            ]
        
        parent_folder = Path(abs_path).relative_to(init_path).parent[0]


        return render_template(
            'folder_content.html', appbuilder=appbuilder, 
            files_and_di=files_and_dir2, parent_path=parent_folder
            )

appbuilder.add_view(FilesListing, 'Files To Be Parsed', 
    href='/fileslisting/listfiles', icon='fa-folder', category='Files')




